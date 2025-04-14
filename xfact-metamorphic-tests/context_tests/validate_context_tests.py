import random

GENERIC_SUPPORT = [
    "O evento foi confirmado por fontes oficiais.",
    "Relatórios confiáveis apontam a veracidade da informação.",
    "Declarações de especialistas corroboram o conteúdo mencionado.",
]

GENERIC_CONTRADICTION = [
    "Não há registros oficiais que comprovem essa alegação.",
    "A informação foi desmentida por autoridades competentes.",
    "Especialistas negaram a validade do conteúdo apresentado.",
]


def insert_supporting_evidence(data):
    modified_data = data.copy()
    modified_data["ctxs"].append(random.choice(GENERIC_SUPPORT))
    return modified_data


def insert_contradictory_evidence(data):
    modified_data = data.copy()
    insertion = random.choice(GENERIC_CONTRADICTION)
    modified_data["ctxs"].insert(random.randint(
        0, len(modified_data["ctxs"])), insertion)
    return modified_data


def remove_partial_context(data):
    modified_data = data.copy()
    if modified_data["ctxs"]:
        modified_data["ctxs"].pop(0)
    return modified_data


def remove_all_context(data):
    modified_data = data.copy()
    modified_data["ctxs"] = []
    return modified_data
