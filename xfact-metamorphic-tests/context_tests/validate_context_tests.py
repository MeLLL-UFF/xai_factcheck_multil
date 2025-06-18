from ..utils import row_to_ctxs, ctxs_to_row, translate_claim, detect_language

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


def get_ctx_language(ctxs):
    """Detecta o idioma da primeira evidência não vazia."""
    for ctx in ctxs:
        if ctx and str(ctx).strip():
            return detect_language(ctx)
    return 'pt'


def insert_supporting_evidence(row):
    data = row_to_ctxs(row)
    lang = get_ctx_language(data["ctxs"])
    phrase = GENERIC_SUPPORT[0]
    if lang != 'pt':
        phrase = translate_claim(phrase, dest_lang=lang)
    data["ctxs"].append(phrase)
    return ctxs_to_row(data)


def insert_contradictory_evidence(row):
    data = row_to_ctxs(row)
    lang = get_ctx_language(data["ctxs"])
    phrase = GENERIC_CONTRADICTION[0]
    if lang != 'pt':
        phrase = translate_claim(phrase, dest_lang=lang)
    data["ctxs"].append(phrase)
    return ctxs_to_row(data)


def remove_partial_context(row):
    data = row_to_ctxs(row)
    if data["ctxs"]:
        data["ctxs"].pop(0)
    return ctxs_to_row(data)


def remove_all_context(row):
    data = row_to_ctxs(row)
    data["ctxs"] = []
    return ctxs_to_row(data)
