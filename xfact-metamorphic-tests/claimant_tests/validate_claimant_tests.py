from ..utils import translate_claim, detect_language
import requests
from bs4 import BeautifulSoup
import random


def get_ifcn_brazil_sources():
    url = "https://ifcncodeofprinciples.poynter.org/signatories"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        entries = soup.find_all("div", class_="signatory-list-item")
        brazil_sources = []

        for entry in entries:
            location = entry.find("div", class_="signatory-location")
            name = entry.find("div", class_="signatory-name")
            if location and "Brazil" in location.text:
                brazil_sources.append(name.text.strip())

        return brazil_sources if brazil_sources else None
    except Exception:
        return None


def set_true_claimant(row):
    row_out = row.copy()

    original_lang = detect_language(
        str(row.get("claimant") or row.get("claim") or ""))
    sources = get_ifcn_brazil_sources()
    if sources:
        base = f"Informação verificada por {random.choice(sources)}"
    else:
        base = "Informação proveniente de uma fonte considerada confiável segundo padrões jornalísticos"
    if original_lang != 'pt':
        row_out["claimant"] = translate_claim(base, dest_lang=original_lang)
    else:
        row_out["claimant"] = base
    return row_out


def set_false_claimant(row):
    row_out = row.copy()
    original_lang = detect_language(
        str(row.get("claimant") or row.get("claim") or ""))
    base = "informação gerada por um blog desconhecido."
    if original_lang != 'pt':
        row_out["claimant"] = translate_claim(base, dest_lang=original_lang)
    else:
        row_out["claimant"] = base
    return row_out


def remove_claimant(row):
    row_out = row.copy()
    row_out["claimant"] = None
    return row_out
