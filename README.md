#  Remédio Check

![CI](https://github.com/mateus-alarcao/remedio-check/actions/workflows/ci.yml/badge.svg)

---

##  Problema Real

Muitas pessoas, especialmente idosos e pacientes com doenças crônicas, têm dificuldade em lembrar quais medicamentos já tomaram no dia. Esquecer ou tomar remédios em duplicata pode causar sérios riscos à saúde.

##  Proposta da Solução

O Remédio Check é uma aplicação de linha de comando (CLI) que permite cadastrar medicamentos com horários, marcar quais já foram tomados no dia e resetar a lista para o próximo dia — tudo de forma simples e sem necessidade de internet.

##  Público-alvo

- Idosos;
- Cuidadores;
- Qualquer pessoa que queira controlar sua rotina de medicamentos

---

##  Funcionalidades

- Adicionar remédio com nome e horário
- Listar todos os remédios e seus status
- Marcar remédio como tomado
- Remover remédio da lista
- Resetar o status de todos para um novo dia
- Dados salvos localmente em arquivo JSON

---

##  Tecnologias

- Python 3.9+
- pytest (testes automatizados)
- ruff (linting)
- GitHub Actions (CI)

---

##  Instalação

```bash
# Clone o repositório
git clone https://github.com/mateus-alarcao/remedio-check.git
cd remedio-check

# (Opcional) Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências de desenvolvimento
pip install -r requirements.txt
```

---

##  Execução

```bash
python src/app.py
```

Exemplo de uso:

```
 Remédio Check v1.0.0
Seu lembrete diário de medicamentos

1. Adicionar remédio
2. Listar remédios
3. Marcar como tomado
4. Remover remédio
5. Resetar dia
0. Sair
```

---

##  Rodando os Testes

```bash
pytest
```

Saída esperada:

```
collected 11 items
tests/test_app.py ...........  11 passed
```

---

##  Rodando o Lint

```bash
ruff check src/ tests/
```

Saída esperada: nenhum erro ou aviso.

---

##  Versão

`1.0.0`

---

##  Autor

Mateus Alarcão

---

##  Repositório

[https://github.com/mateus-alarcao/remedio-check](https://github.com/mateus-alarcao/remedio-check)
