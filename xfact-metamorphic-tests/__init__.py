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

from validate_metamorphic_tests import validate_truthfulness

data = pd.DataFrame({
    'question': ["O homem pisou na Lua em 1969?", "Did man walk on the moon in 1969?", "Segundo Bolsonaro, a vacina da COVID não funciona.",
                 "O Brasil ganhou a Copa do Mundo de 1958?", "O Brasil venceu a Copa do Mundo de 2002?", "O homem pisou na Lua em 1969?"],
    'answer': ["É verdade.", "Yes, he did.", "A vacina da COVID funciona.", "Sim, ganhou.", "Sim, venceu.", "É verdade."],
    'context': ["O homem pisou na Lua em 1969.", "Man walked on the moon in 1969.", 
                "O presidente Bolsonaro alegou em uma entrevista que a vacina não funciona, porém isso é um dado errado, visto que a eficácia da vacina foi comprovada nos estudos da Fundação Fiocruz.",
                "O Brasil conquistou sua primeira Copa do Mundo em 1958.", "O Brasil venceu a Copa do Mundo de 2002.", "O homem pisou na Lua em 1969."]
})

# Testes para validate_truthfulness

# Teste 1: alteration_change
test1 = validate_truthfulness(
    data=data,
    question="O homem pisou na Lua em 1969?",
    answer="É verdade.",
    context="O homem pisou na Lua em 1969.",
    alteration={"word": "1969", "new_word": "1970", "alteration_choice": "all"}
)

# Teste 2: validate_translation (inglês)
test2 = validate_truthfulness(
    data=data,
    question="Did man walk on the moon in 1969?",
    answer="Yes, he did.",
    context="Man walked on the moon in 1969.",
    language='en'
)

# Teste 3: validate_authority_change
test3 = validate_truthfulness(
    data=data,
    question="Segundo Bolsonaro, a vacina da COVID não funciona.",
    answer="A vacina da COVID funciona.",
    context="O presidente Bolsonaro alegou em uma entrevista que a vacina não funciona, porém isso é um dado errado, visto que a eficácia da vacina foi comprovada nos estudos da Fundação Fiocruz.",
    authority_change={"entity": "Bolsonaro", "new_entity": "Lula"}
)

# Teste 4: similar_word_change
test4 = validate_truthfulness(
    data=data,
    question="O Brasil ganhou a Copa do Mundo de 1958?",
    answer="Sim, ganhou.",
    context="O Brasil conquistou sua primeira Copa do Mundo em 1958.",
    similar_word={"old_word": "1958", "new_word": "1962", "alteration_choice": "all"}
)

# Teste 5: Todos os parâmetros
test5 = validate_truthfulness(
    data=data,
    question="O Brasil venceu a Copa do Mundo de 2002?",
    answer="Sim, venceu.",
    context="O Brasil venceu a Copa do Mundo de 2002.",
    alteration={"word": "2002", "new_word": "1998", "alteration_choice": "all"},
    similar_word={"old_word": "Brasil", "new_word": "Argentina", "alteration_choice": "all"},
    language='pt',
    authority_change={"entity": "Brasil", "new_entity": "Argentina"}
)

# Teste 6: Alteração de palavras similares com substituição de uma palavra aleatória
test6 = validate_truthfulness(
    data=data,
    question="O homem pisou na Lua em 1969?",
    answer="É verdade.",
    context="O homem pisou na Lua em 1969.",
    similar_word={"old_word": "pisou", "new_word": "não pisou", "alteration_choice": "random"}
)

# Teste 7: Alteração com `alteration_choice` set to `'set'`
test7 = validate_truthfulness(
    data=data,
    question="O homem pisou na Lua em 1969?",
    answer="É verdade.",
    context="O homem pisou na Lua em 1969.",
    alteration={"word": "1969", "new_word": "1970", "alteration_choice": "set", "num_words": 1}
)

# Teste 8: Linguagem em inglês para `validate_translation`
test8 = validate_truthfulness(
    data=data,
    question="Did man walk on the moon in 1969?",
    answer="Yes, he did.",
    context="Man walked on the moon in 1969.",
    language='en'
)

# Teste 9: Alteração de autoridade
test9 = validate_truthfulness(
    data=data,
    question="Segundo Bolsonaro, a vacina da COVID não funciona.",
    answer="A vacina da COVID funciona.",
    context="O presidente Bolsonaro alegou em uma entrevista que a vacina não funciona, porém isso é um dado errado, visto que a eficácia da vacina foi comprovada nos estudos da Fundação Fiocruz.",
    authority_change={"entity": "Bolsonaro", "new_entity": "Lula"}
)

# Teste 10: Teste com múltiplas mudanças
test10 = validate_truthfulness(
    data=data,
    question="O Brasil venceu a Copa do Mundo de 1994?",
    answer="Sim, venceu.",
    context="O Brasil venceu a Copa do Mundo de 1994.",
    alteration={"word": "1994", "new_word": "1986", "alteration_choice": "all"},
    similar_word={"old_word": "Copa do Mundo", "new_word": "Mundial", "alteration_choice": "all"},
    language='pt',
    authority_change={"entity": "Brasil", "new_entity": "Argentina"}
)

# Resultados dos testes
print("Testes para validate_truthfulness:")
print("Teste 1 (alteration_change):", test1)
print("Teste 2 (validate_translation):", test2)
print("Teste 3 (validate_authority_change):", test3)
print("Teste 4 (similar_word_change):", test4)
print("Teste 5 (Todos os parâmetros):", test5)
print("Teste 6 (Alteração de palavras similares com substituição de uma palavra aleatória):", test6)
print("Teste 7 (Alteração com 'set'):", test7)
print("Teste 8 (Linguagem em inglês para `validate_translation`):", test8)
print("Teste 9 (Alteração de autoridade):", test9)
print("Teste 10 (Teste com múltiplas mudanças):", test10)