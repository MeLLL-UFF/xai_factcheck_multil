from utils import translate_back_to_original, translate_claim
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


def set_true_claimant(data):
    modified_data = data.copy()
    sources = get_ifcn_brazil_sources()

    if sources:
        chosen_source = random.choice(sources)
        modified_data["claimant"] = f"Informação verificada por {chosen_source}"
    else:
        modified_data["claimant"] = "Informação proveniente de uma fonte considerada confiável segundo padrões jornalísticos"

    return modified_data


def set_false_claimant(data):
    modified_data = data.copy()
    modified_claimant = "informação gerada por um blog desconhecido."
    modified_data["claimant"] = translate_back_to_original(
        modified_claimant, 'auto')

    return modified_data


def remove_claimant(data):
    modified_data = data.copy()
    modified_data["claimant"] = "None"

    return modified_data