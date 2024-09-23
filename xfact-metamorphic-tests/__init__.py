# pegar base de dados:
# necessita de informacao e evidencia V
# ver base que a Mariana e a Bruna catalogaram(fact-checking) V

# testes metamorficos
# automatizar testes em base de dados, atraves de parametros

# dificuldade com numeros e troca de caracteres(numeros) V
# traducao V 
# expressao (alteracao de entidade nomeada/ dominio da informacao/ apelo a autoridade) V
# trocar palavra (aleatoriamente/ uma apenas/ categoricamente) V
# testar testes juntos V
# remocao de documento (deixar para dps)

# criar os testes e depois aplicar os testes, se for treinar o modelo novamente. Falar com a Bruna.
#
import pandas as pd

from claim_tests import validate_claim_tests
from context_tests import validate_context_tests
data = pd.DataFrame({
    'question': ["O homem pisou na Lua em 1969?", "Did man walk on the moon in 1969?", "Segundo Bolsonaro, a vacina da COVID não funciona.",
                 "O Brasil ganhou a Copa do Mundo de 1958?", "O Brasil venceu a Copa do Mundo de 2002?", "O homem pisou na Lua em 1969?"],
    'answer': ["É verdade.", "Yes, he did.", "A vacina da COVID funciona.", "Sim, ganhou.", "Sim, venceu.", "É verdade."],
    'context': ["O homem pisou na Lua em 1969.", "Man walked on the moon in 1969.", 
                "O presidente Bolsonaro alegou em uma entrevista que a vacina não funciona, porém isso é um dado errado, visto que a eficácia da vacina foi comprovada nos estudos da Fundação Fiocruz.",
                "O Brasil conquistou sua primeira Copa do Mundo em 1958.", "O Brasil venceu a Copa do Mundo de 2002.", "O homem pisou na Lua em 1969."]
})

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
    executar 1/3 da base = 1.127 noticias

"""
documents = "zeroshot.tsv data/3 com aleatoriedade na hora de pegar os valores"

"""for document of documents:
    executar todos os testes (claim, claimant, label, evidences, claimDate, revDate)

"""   
# Validar os testes
validation_claim_results = validate_claim_tests(original_claim, expected_outcome)
validation__context_results = validate_context_tests(data, original_claim, expected_outcome)
# Exibir os resultados da validação
for test_name, result in validation_claim_results.items():
    print(f"{test_name}: {result}")

for test_name, result in validation__context_results.items():
    print(f"{test_name}: {result}")