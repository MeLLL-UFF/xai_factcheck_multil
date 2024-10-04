# dificuldade com numeros e troca de caracteres(numeros) V
# remoção de contexto, adição de contexto, adição de contexto falso em relação ao resultado esperado
# adição de contexto falso, adição de contexto negativo
# alteracao de claim por sinônimo, negação da claim, remoção de palavras, alteração de contexto para pergunta
# traducao V 
# expressao (alteracao de entidade nomeada/ dominio da informacao/ apelo a autoridade) V
# trocar palavra (aleatoriamente/ uma apenas/ categoricamente) V
# testar testes juntos V

# criar os testes e depois aplicar os testes, se for treinar o modelo novamente. Falar com a Bruna.

import pandas as pd

from claim_tests import validate_claim_tests
from context_tests import validate_context_tests
from claimant_tests import validate_claimant_tests
from date_tests import validate_date_tests

"""
    - Idioma: string
    - Site:  string
    - Evidências: []
    - Links: [] --> nao vamos usar pois pode permitir que modelos que possuem acesso a internet acessem.
    - Data da alegação: string
    - Data da revisão: string
    - Reclamante: string
    - Alegação: string
"""

original_claim = "Os EUA compraram 90% do suprimento global de remdesivir."
expected_outcome = True  # O resultado esperado do claim original
"""
    executar 1/3 da base = 270 dados

"""
documents = "zeroshot.tsv data/3 com aleatoriedade na hora de pegar os valores"

"""for document of documents:
    executar todos os testes (claim, claimant, label, evidences, claimDate, revDate)

"""   

data = []
# Validar os testes
validation_claim_results = validate_claim_tests(data, original_claim, expected_outcome)
validation__context_results = validate_context_tests(data, original_claim, expected_outcome)
validation__claimant_results = validate_claimant_tests(data, original_claim, expected_outcome)
validation__date_results = validate_date_tests(data, original_claim, expected_outcome)

# Exibir os resultados da validação
for test_name, result in validation_claim_results.items():
    print(f"{test_name}: {result}")

for test_name, result in validation__context_results.items():
    print(f"{test_name}: {result}")

for test_name, result in validation__claimant_results.items():
    print(f"{test_name}: {result}")

for test_name, result in validation__date_results.items():
    print(f"{test_name}: {result}")