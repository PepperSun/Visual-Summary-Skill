#!/usr/bin/env python3
"""Basic text extraction helper for visual-summary.

Usage:
  python scripts/extract_text.py input_file [output_txt]

Supports plain text and markdown directly. For DOCX it uses a zero-dependency
XML path first. For PDF it tries common local tools and installed libraries
when available. Extracted text is normalized to remove repeated boilerplate and
hard-wrapped lines before it is passed to the model. This is a fallback
extraction utility for intermediate normalized text only, not a final delivery
format. Use stronger native document tools when available.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET


DOCX_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
PAGE_NUMBER_RE = re.compile(
    r"^(?:page\s+)?\d+(?:\s*(?:/|of)\s*\d+)?$", re.IGNORECASE
)
MULTISPACE_RE = re.compile(r"[ \t]+")
BLANK_RUN_RE = re.compile(r"\n{3,}")
HYPHEN_WRAP_RE = re.compile(r"([A-Za-z])-\n([A-Za-z])")
LIST_MARKER_RE = re.compile(r"^(?:[-*•]\s+|\d+[.)]\s+)")


def extract_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _extract_docx_part(xml_bytes: bytes) -> list[str]:
    root = ET.fromstring(xml_bytes)
    paragraphs: list[str] = []
    for para in root.findall(".//w:p", DOCX_NS):
        chunks = []
        for node in para.iterfind(".//w:t", DOCX_NS):
            if node.text:
                chunks.append(node.text)
        text = "".join(chunks).strip()
        if text:
            paragraphs.append(text)
    return paragraphs


def extract_docx_with_stdlib(path: Path) -> str:
    xml_parts = [
        "word/document.xml",
        "word/footnotes.xml",
        "word/endnotes.xml",
    ]
    with ZipFile(path) as archive:
        names = set(archive.namelist())
        header_names = sorted(name for name in names if name.startswith("word/header"))
        footer_names = sorted(name for name in names if name.startswith("word/footer"))
        ordered_names = xml_parts + header_names + footer_names
        paragraphs: list[str] = []
        for name in ordered_names:
            if name not in names:
                continue
            paragraphs.extend(_extract_docx_part(archive.read(name)))
    text = "\n\n".join(paragraphs).strip()
    if not text:
        raise RuntimeError("DOCX file did not contain extractable text")
    return text


def extract_docx(path: Path) -> str:
    try:
        return extract_docx_with_stdlib(path)
    except Exception:
        pass
    try:
        import docx  # type: ignore
    except Exception as exc:
        raise RuntimeError(
            "DOCX extraction requires either the built-in XML path or python-docx"
        ) from exc
    doc = docx.Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def extract_pdf_with_pdftotext(path: Path) -> list[str]:
    command = shutil.which("pdftotext")
    if not command:
        raise RuntimeError("pdftotext not found")
    result = subprocess.run(
        [command, "-layout", str(path), "-"],
        capture_output=True,
        check=True,
        text=True,
    )
    return [page for page in result.stdout.split("\f") if page.strip()]


def extract_pdf_with_mutool(path: Path) -> list[str]:
    command = shutil.which("mutool")
    if not command:
        raise RuntimeError("mutool not found")
    result = subprocess.run(
        [command, "draw", "-F", "txt", "-o", "-", str(path)],
        capture_output=True,
        check=True,
        text=True,
    )
    return [page for page in result.stdout.split("\f") if page.strip()]


def extract_pdf_with_pdfplumber(path: Path) -> list[str]:
    import pdfplumber  # type: ignore

    chunks: list[str] = []
    with pdfplumber.open(str(path)) as pdf:
        for page in pdf.pages:
            chunks.append(page.extract_text() or "")
    return chunks


def extract_pdf_with_pypdf(path: Path) -> list[str]:
    from pypdf import PdfReader  # type: ignore

    reader = PdfReader(str(path))
    chunks: list[str] = []
    for page in reader.pages:
        chunks.append(page.extract_text() or "")
    return chunks


def _is_probable_heading(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if LIST_MARKER_RE.match(stripped) or "|" in stripped:
        return False
    if stripped.endswith((".", "!", "?", ";", ":", "。", "！", "？", "；", "：")):
        return False
    return len(stripped) <= 32


def _merge_wrapped_lines(text: str) -> str:
    merged: list[str] = []
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if not paragraph:
            return
        merged.append(" ".join(paragraph))
        paragraph = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            flush_paragraph()
            if merged and merged[-1] != "":
                merged.append("")
            continue
        if LIST_MARKER_RE.match(line) or "|" in line or _is_probable_heading(line):
            flush_paragraph()
            merged.append(line)
            continue
        paragraph.append(line)

    flush_paragraph()
    while merged and merged[-1] == "":
        merged.pop()
    return "\n".join(merged)


def _normalize_page(page: str) -> list[str]:
    page = page.replace("\r\n", "\n").replace("\r", "\n").replace("\xa0", " ")
    page = HYPHEN_WRAP_RE.sub(r"\1\2", page)
    lines = []
    for raw_line in page.splitlines():
        line = MULTISPACE_RE.sub(" ", raw_line).strip()
        if not line or PAGE_NUMBER_RE.match(line):
            continue
        lines.append(line)
    return lines


def _detect_repeated_boundary_lines(pages: list[list[str]]) -> set[str]:
    counts: dict[str, int] = {}
    for lines in pages:
        boundary_lines = lines[:2] + lines[-2:]
        seen = set()
        for line in boundary_lines:
            normalized = line.casefold()
            if normalized in seen:
                continue
            seen.add(normalized)
            if 3 <= len(line) <= 120 and not PAGE_NUMBER_RE.match(line):
                counts[normalized] = counts.get(normalized, 0) + 1
    threshold = 2 if len(pages) < 5 else 3
    return {line for line, count in counts.items() if count >= threshold}


def normalize_pages(pages: list[str]) -> str:
    structured_pages = [_normalize_page(page) for page in pages if page.strip()]
    repeated_boundary_lines = _detect_repeated_boundary_lines(structured_pages)
    normalized_pages: list[str] = []

    for lines in structured_pages:
        cleaned_lines = []
        total = len(lines)
        for index, line in enumerate(lines):
            normalized = line.casefold()
            is_boundary = index < 2 or index >= max(total - 2, 0)
            if is_boundary and normalized in repeated_boundary_lines:
                continue
            cleaned_lines.append(line)
        page_text = _merge_wrapped_lines("\n".join(cleaned_lines)).strip()
        if page_text:
            normalized_pages.append(page_text)

    text = "\n\n".join(normalized_pages).strip()
    return BLANK_RUN_RE.sub("\n\n", text)


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\xa0", " ")
    text = HYPHEN_WRAP_RE.sub(r"\1\2", text)
    text = MULTISPACE_RE.sub(" ", text)
    text = _merge_wrapped_lines(text)
    return BLANK_RUN_RE.sub("\n\n", text).strip()


def extract_pdf(path: Path) -> str:
    errors = []

    try:
        return normalize_pages(extract_pdf_with_pdftotext(path))
    except Exception as exc:
        errors.append(f"pdftotext failed: {exc}")

    try:
        return normalize_pages(extract_pdf_with_mutool(path))
    except Exception as exc:
        errors.append(f"mutool failed: {exc}")

    try:
        return normalize_pages(extract_pdf_with_pdfplumber(path))
    except Exception as exc:
        errors.append(f"pdfplumber failed: {exc}")

    try:
        return normalize_pages(extract_pdf_with_pypdf(path))
    except Exception as exc:
        errors.append(f"pypdf failed: {exc}")

    raise RuntimeError(
        "PDF extraction requires pdftotext, mutool, pdfplumber, or pypdf. "
        + " / ".join(errors)
    )


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"file not found: {path}", file=sys.stderr)
        return 1
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md", ".markdown"}:
        text = normalize_text(extract_txt(path))
    elif suffix == ".docx":
        text = normalize_text(extract_docx(path))
    elif suffix == ".pdf":
        text = extract_pdf(path)
    else:
        raise RuntimeError(f"unsupported file type: {suffix}")
    if len(sys.argv) == 3:
        Path(sys.argv[2]).write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
