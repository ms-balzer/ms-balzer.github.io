#!/usr/bin/env python3
"""
fetch_pubmed.py (stdlib-only)

Generates:
- data/pubmed.json
- content/publications/pmid-<PMID>/index.md (bundle)
- citation exports: cite.bib, cite.ris, cite.enw per bundle

No third-party deps: uses urllib + json + xml.etree only.

PDFs:
- If you manually place "paper.pdf" into the bundle directory
  content/publications/pmid-<PMID>/paper.pdf
  then pubmed.json will include pdf_url and the detail page front matter includes pdf_url.
"""

import argparse
import datetime
import html
import json
import os
import re
import time
from typing import Any, Dict, List
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET


# -----------------------------
# Config
# -----------------------------
NCBI_EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
NCBI_SLEEP_SECONDS = 0.34

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

DATA_DIR = os.path.join(SITE_ROOT, "data")
CONTENT_DIR = os.path.join(SITE_ROOT, "content")
DETAIL_ROOT = os.path.join(CONTENT_DIR, "publications")

PUBMED_JSON_PATH = os.path.join(DATA_DIR, "pubmed.json")

DETAIL_PREFIX = "pmid-"
BUNDLE_PDF_NAME = "paper.pdf"


# -----------------------------
# YAML helpers
# -----------------------------
def yaml_quote(s: str) -> str:
    s = (s or "").replace("\\", "\\\\").replace('"', '\\"')
    return f"\"{s}\""


def yaml_list(items: List[str], indent: int = 2) -> str:
    pad = " " * indent
    return "\n".join([f"{pad}- {yaml_quote(x)}" for x in items])


# -----------------------------
# Citation helpers
# -----------------------------
def make_bibtex(pmid: str, title: str, authors: List[str], journal: str, year: str,
               volume: str, issue: str, pages: str, doi: str) -> str:
    key = f"pmid{pmid}"
    author_str = " and ".join(authors) if authors else ""
    fields = {
        "title": title,
        "author": author_str,
        "journal": journal,
        "year": year,
        "volume": volume,
        "number": issue,
        "pages": pages,
        "doi": doi,
        "pmid": pmid,
    }
    lines = [f"@article{{{key},"]
    for k, v in fields.items():
        if v:
            v_escaped = v.replace("{", "\\{").replace("}", "\\}")
            lines.append(f"  {k} = {{{v_escaped}}},")
    if lines[-1].endswith(","):
        lines[-1] = lines[-1].rstrip(",")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def make_ris(pmid: str, title: str, authors: List[str], journal: str, year: str,
             volume: str, issue: str, pages: str, doi: str) -> str:
    lines = ["TY  - JOUR"]
    if title:
        lines.append(f"TI  - {title}")
    for a in authors or []:
        lines.append(f"AU  - {a}")
    if journal:
        lines.append(f"JO  - {journal}")
    if year:
        lines.append(f"PY  - {year}")
    if volume:
        lines.append(f"VL  - {volume}")
    if issue:
        lines.append(f"IS  - {issue}")
    if pages:
        lines.append(f"SP  - {pages}")
    if doi:
        lines.append(f"DO  - {doi}")
    if pmid:
        lines.append(f"ID  - {pmid}")
    lines.append("ER  -")
    lines.append("")
    return "\n".join(lines)


def make_endnote_enw(pmid: str, title: str, authors: List[str], journal: str, year: str,
                     volume: str, issue: str, pages: str, doi: str) -> str:
    lines = ["%0 Journal Article"]
    for a in authors or []:
        lines.append(f"%A {a}")
    if title:
        lines.append(f"%T {title}")
    if journal:
        lines.append(f"%J {journal}")
    if year:
        lines.append(f"%D {year}")
    if volume:
        lines.append(f"%V {volume}")
    if issue:
        lines.append(f"%N {issue}")
    if pages:
        lines.append(f"%P {pages}")
    if doi:
        lines.append(f"%R {doi}")
    if pmid:
        lines.append(f"%M {pmid}")
    lines.append("")
    return "\n".join(lines)


# -----------------------------
# HTTP helpers (stdlib)
# -----------------------------
def http_get(url: str, params: Dict[str, str], timeout: int = 60) -> str:
    qs = urlencode(params)
    full = f"{url}?{qs}"
    req = Request(
        full,
        headers={
            "User-Agent": "balzerlab-wowchemy-pubmed-fetch/1.0"
        },
        method="GET",
    )
    with urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    return data.decode("utf-8", errors="replace")


def esearch(term: str, retmax: int = 200) -> List[str]:
    url = f"{NCBI_EUTILS_BASE}esearch.fcgi"
    txt = http_get(
        url,
        {"db": "pubmed", "term": term, "retmode": "json", "retmax": str(retmax)},
    )
    data = json.loads(txt)
    idlist = data.get("esearchresult", {}).get("idlist", []) or []
    return [str(x) for x in idlist]


def esummary(pmids: List[str]) -> Dict[str, Any]:
    url = f"{NCBI_EUTILS_BASE}esummary.fcgi"
    txt = http_get(url, {"db": "pubmed", "id": ",".join(pmids), "retmode": "json"})
    return json.loads(txt)


def efetch_abstract(pmid: str) -> str:
    url = f"{NCBI_EUTILS_BASE}efetch.fcgi"
    txt = http_get(url, {"db": "pubmed", "id": pmid, "retmode": "xml"})
    root = ET.fromstring(txt)

    parts: List[str] = []
    for abst in root.findall(".//Abstract/AbstractText"):
        label = (abst.attrib.get("Label") or "").strip()
        t = "".join(abst.itertext()).strip()
        t = html.unescape(t)
        if not t:
            continue
        parts.append(f"{label}: {t}" if label else t)

    return "\n\n".join(parts).strip()


# -----------------------------
# Main
# -----------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch PubMed records and write Hugo content + data (stdlib-only)."
    )

    parser.add_argument(
        "--term",
        default="(Balzer MS[Author]) OR (S Balzer M[Author])",
        help="PubMed search term"
    )

    parser.add_argument(
        "--retmax",
        type=int,
        default=200,
        help="Max records to fetch."
    )

    args = parser.parse_args()

    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(DETAIL_ROOT, exist_ok=True)

    generated_at = datetime.datetime.now().isoformat(timespec="seconds")

    print("Searching PubMed...")
    uids = esearch(args.term, retmax=args.retmax)
    time.sleep(NCBI_SLEEP_SECONDS)

    if not uids:
        out = {"generated_at": generated_at, "count": 0, "items": []}
        with open(PUBMED_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
        print(f"Wrote {PUBMED_JSON_PATH} with 0 items.")
        return

    print(f"Found {len(uids)} PubMed IDs. Fetching summaries...")

    items: List[Dict[str, Any]] = []

    batch_size = 200
    for batch_start in range(0, len(uids), batch_size):
        batch = uids[batch_start:batch_start + batch_size]
        payload = esummary(batch)
        time.sleep(NCBI_SLEEP_SECONDS)

        result = payload.get("result", {}) or {}
        uids_in_result = result.get("uids", []) or []

        for idx, pmid in enumerate(uids_in_result, start=batch_start + 1):
            item = result.get(pmid, {}) or {}

            title = (item.get("title") or "").strip().rstrip(".")
            journal = (item.get("fulljournalname") or "").strip()
            pubdate_text = (item.get("pubdate") or "").strip()

            year = ""
            if pubdate_text:
                year = (pubdate_text.split(" ")[0] or "").strip()

            volume = (item.get("volume") or "").strip()
            issue = (item.get("issue") or "").strip()
            pages = (item.get("pages") or "").strip()

            authors: List[str] = []
            for a in item.get("authors", []) or []:
                name = (a.get("name") or "").strip()
                if name:
                    authors.append(name)

            doi = ""
            for article_id in item.get("articleids", []) or []:
                if (article_id.get("idtype") or "") == "doi":
                    doi = (article_id.get("value") or "").strip()
                    break

            pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            doi_url = f"https://doi.org/{doi}" if doi else ""

            print(f"[{idx}/{len(uids)}] Fetching abstract for PMID {pmid}...")
            abstract = efetch_abstract(pmid)
            time.sleep(NCBI_SLEEP_SECONDS)

            # Internal detail pages (bundle)
            detail_slug = f"{DETAIL_PREFIX}{pmid}"
            detail_rel_url = f"/publications/{detail_slug}/"

            detail_dir = os.path.join(DETAIL_ROOT, detail_slug)
            os.makedirs(detail_dir, exist_ok=True)

            # Optional bundle PDF
            pdf_url = ""
            bundle_pdf_path = os.path.join(detail_dir, BUNDLE_PDF_NAME)
            if os.path.exists(bundle_pdf_path):
                pdf_url = f"/publications/{detail_slug}/{BUNDLE_PDF_NAME}"

            # Citation exports in bundle
            with open(os.path.join(detail_dir, "cite.bib"), "w", encoding="utf-8") as f:
                f.write(make_bibtex(pmid, title, authors, journal, year, volume, issue, pages, doi))

            with open(os.path.join(detail_dir, "cite.ris"), "w", encoding="utf-8") as f:
                f.write(make_ris(pmid, title, authors, journal, year, volume, issue, pages, doi))

            with open(os.path.join(detail_dir, "cite.enw"), "w", encoding="utf-8") as f:
                f.write(make_endnote_enw(pmid, title, authors, journal, year, volume, issue, pages, doi))

            # Front matter
            detail_index = os.path.join(detail_dir, "index.md")
            fm_title = title if title else f"PMID {pmid}"

            fm_lines: List[str] = ["---"]
            fm_lines.append(f"title: {yaml_quote(fm_title)}")
            fm_lines.append(f"type: {yaml_quote('publications')}")
            fm_lines.append(f"pmid: {yaml_quote(pmid)}")

            if doi:
                fm_lines.append(f"doi: {yaml_quote(doi)}")
            if journal:
                fm_lines.append(f"journal: {yaml_quote(journal)}")
            if pubdate_text:
                fm_lines.append(f"pubdate_text: {yaml_quote(pubdate_text)}")
            if volume:
                fm_lines.append(f"volume: {yaml_quote(volume)}")
            if issue:
                fm_lines.append(f"issue: {yaml_quote(issue)}")
            if pages:
                fm_lines.append(f"pages: {yaml_quote(pages)}")

            fm_lines.append(f"pubmed_url: {yaml_quote(pubmed_url)}")
            if doi_url:
                fm_lines.append(f"doi_url: {yaml_quote(doi_url)}")
            if pdf_url:
                fm_lines.append(f"pdf_url: {yaml_quote(pdf_url)}")
            if abstract:
                fm_lines.append(f"abstract: {yaml_quote(abstract)}")

            fm_lines.append(f"generated_at: {yaml_quote(generated_at)}")

            if authors:
                fm_lines.append("authors:")
                fm_lines.append(yaml_list(authors))

            fm_lines.append("---")
            fm_lines.append("")
            fm_lines.append("")

            with open(detail_index, "w", encoding="utf-8") as f:
                f.write("\n".join(fm_lines))

            items.append(
                {
                    "pmid": pmid,
                    "title": title,
                    "authors": authors,
                    "journal": journal,
                    "pubdate_text": pubdate_text,
                    "year": year,
                    "volume": volume,
                    "issue": issue,
                    "pages": pages,
                    "doi": doi,
                    "pubmed_url": pubmed_url,
                    "doi_url": doi_url,
                    "detail_url": detail_rel_url,
                    "pdf_url": pdf_url,
                }
            )

    out = {"generated_at": generated_at, "count": len(items), "items": items}
    with open(PUBMED_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"Wrote {PUBMED_JSON_PATH} with {len(items)} items.")
    print(f"Wrote {len(items)} detail bundles under {DETAIL_ROOT}.")


if __name__ == "__main__":
    main()
