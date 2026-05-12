# 💊 Remédio Check

![CI](https://github.com/mateus-alarcao/remedio-check/actions/workflows/ci.yml/badge.svg)

> 🚀 **Deploy:** aplicação CLI — execute localmente seguindo as instruções abaixo.
> Para execução sem instalação: `docker run --rm -it $(docker build -q .)` *(veja seção Docker)*

---

## 📋 Problema Real

Muitas pessoas, especialmente idosos e pacientes com doenças crônicas, têm dificuldade em lembrar quais medicamentos já tomaram no dia. Esquecer ou tomar remédios em duplicata pode causar sérios riscos à saúde.

## 💡 Proposta da Solução

O Remédio Check é uma aplicação de linha de comando (CLI) que permite cadastrar medicamentos com horários, marcar quais já foram tomados no dia e resetar a lista para o próximo dia. A partir da **v1.1.0**, também consulta a base pública **OpenFDA** para exibir informações técnicas sobre medicamentos.

## 👥 Público-alvo

- Idosos
- Cuidadores
- Qualquer pessoa que queira controlar sua rotina de medicamentos

---

## ✅ Funcionalidades

- Adicionar remédio com nome e horário
- Listar todos os remédios e seus status
- Marcar remédio como tomado
- Remover remédio da lista
- Resetar o status de todos para um novo dia
- Dados salvos localmente em arquivo JSON
- **[NOVO] Buscar informações de um remédio via API OpenFDA** (nome comercial, substância, fabricante, indicação)

---

## 🔗 Integração com API Externa

A aplicação consome a **[OpenFDA Drug Label API](https://open.fda.gov/apis/drug/label/)** — uma API pública, gratuita e sem necessidade de chave de acesso, mantida pelo FDA (Food and Drug Administration dos EUA).

**O que ela retorna:**
- Nome comercial do medicamento
- Substância ativa
- Fabricante
- Indicação de uso (resumida em até 300 caracteres)

**Como usar (opção 6 do menu):**
```
6. Buscar informações de um remédio (OpenFDA)
Nome do remédio para buscar (preferencialmente em inglês): aspirin

📋 Informações encontradas:
   Nome comercial : Aspirin
   Substância     : ASPIRIN
   Fabricante     : Bayer HealthCare LLC
   Indicação      : Temporarily relieves minor aches and pains...
```

> ⚠️ A base OpenFDA é americana. Use o nome do princípio ativo em inglês para melhores resultados (ex: `metformin`, `aspirin`, `omeprazole`).

---

## 🛠️ Tecnologias

- Python 3.9+
- urllib (stdlib — sem dependências externas para a API)
- pytest (testes automatizados — unitários e de integração)
- ruff (linting)
- GitHub Actions (CI)

---

## ⚙️ Instalação

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

## ▶️ Execução

```bash
python src/app.py
```

Exemplo de uso:

```
💊 Remédio Check v1.1.0
Seu lembrete diário de medicamentos

1. Adicionar remédio
2. Listar remédios
3. Marcar como tomado
4. Remover remédio
5. Resetar dia
6. Buscar informações de um remédio (OpenFDA)
0. Sair
```

---

## 🐳 Deploy via Docker (execução sem instalação local)

```bash
# Build da imagem
docker build -t remedio-check .

# Execução interativa
docker run --rm -it remedio-check
```

Dockerfile incluído no repositório.

---

## 🧪 Rodando os Testes

```bash
pytest
```

Saída esperada:

```
collected 18 items
tests/test_app.py ...........                  11 passed
tests/test_integracao.py .......               7 passed
```

Os testes de integração utilizam **mock** — não precisam de conexão com a internet para rodar.

---

## 🔍 Rodando o Lint

```bash
ruff check src/ tests/
```

Saída esperada: nenhum erro ou aviso.

---

## 📁 Estrutura do Projeto

```
remedio-check/
├── src/
│   ├── app.py                  # Aplicação principal (CLI)
│   └── api_medicamento.py      # Integração com a API OpenFDA
├── tests/
│   ├── test_app.py             # Testes unitários
│   └── test_integracao.py      # Testes de integração (com mock)
├── .github/
│   └── workflows/
│       └── ci.yml              # Pipeline CI/CD
├── Dockerfile                  # Para execução via container
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## 📌 Versão

`1.1.0`

---

## 👤 Autor

Mateus Alarcão

---

## 🔗 Repositório

[https://github.com/mateus-alarcao/remedio-check](https://github.com/mateus-alarcao/remedio-check)
