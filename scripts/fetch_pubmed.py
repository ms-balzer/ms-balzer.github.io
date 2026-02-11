#!/usr/bin/env python3

import json
import os
import time
import urllib.parse
import urllib.request

# ==========================
# CONFIGURATION
# ==========================

QUERY = "(Balzer MS) OR (S Balzer M)"
RETMAX = 200  # number of publications to fetch
NCBI_TOOL = "balzer-lab-website"
NCBI_EMAIL = "michael-soeren.balzer@charite.de"  # recommended by NCBI


# ==========================
# HELPER FUNCTIONS
# ==========================

def fetch_url(url):
    with urllib.request.urlopen(url) as response:
        return response.read().decode("utf-8")


def main():
    print("Fetching PubMed data...")

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    # --------------------------
    # 1) ESearch: get PMIDs
    # --------------------------

    term = urllib.parse.quote(QUERY)

    esearch_url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        f"?db=pubmed"
        f"&term={term}"
        f"&retmode=json"
        f"&retmax={RETMAX}"
        f"&sort=date"
        f"&tool={NCBI_TOOL}"
        f"&email={NCBI_EMAIL}"
    )

    print("Running ESearch...")
    esearch_data = json.loads(fetch_url(esearch_url))

    pmids = esearch_data.get("esearchresult", {}).get("idlist", [])

    if not pmids:
        print("No publications found.")
        return

    print(f"Found {len(pmids)} publications.")

    # --------------------------
    # 2) ESummary: get metadata
    # --------------------------

    id_string = ",".join(pmids)

    esummary_url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        f"?db=pubmed"
        f"&id={id_string}"
        f"&retmode=json"
        f"&tool={NCBI_TOOL}"
        f"&email={NCBI_EMAIL}"
    )

    print("Running ESummary...")
    summary_data = json.loads(fetch_url(esummary_url))

    # --------------------------
    # 3) Normalize output
    # --------------------------

    publications = []

    for pmid in pmids:
        item = summary_data.get("result", {}).get(pmid, {})

        if not item:
            continue

        title = (item.get("title") or "").rstrip(".")
        source = item.get("source") or ""
        pubdate = item.get("pubdate") or ""
        volume = item.get("volume") or ""
        issue = item.get("issue") or ""
        pages = item.get("pages") or ""

        # Extract authors
        authors = []
        for a in item.get("authors", []):
            name = a.get("name")
            if name:
                authors.append(name)

        # Extract DOI
        doi = ""
        for article_id in item.get("articleids", []):
            if article_id.get("idtype") == "doi":
                doi = article_id.get("value", "")
                break

        publications.append({
            "pmid": pmid,
            "title": title,
            "authors": authors,
            "journal": source,
            "pubdate": pubdate,
            "volume": volume,
            "issue": issue,
            "pages": pages,
            "doi": doi,
            "pubmed_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "doi_url": f"https://doi.org/{doi}" if doi else ""
        })

    # --------------------------
    # 4) Write JSON file
    # --------------------------

    output = {
        "query": QUERY,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "count": len(publications),
        "items": publications
    }

    with open("data/pubmed.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("Successfully wrote data/pubmed.json")
    print(f"{len(publications)} publications saved.")


if __name__ == "__main__":
    main()
