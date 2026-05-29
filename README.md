# 💊 Remédio Check


> 🚀 **Deploy:** aplicação CLI — execute localmente seguindo as instruções abaixo.  
> Para execução sem instalação: `docker run --rm -it --env-file .env $(docker build -q .)` *(veja seção Docker)*

---

## 📋 Problema Real

Muitas pessoas, especialmente idosos e pacientes com doenças crônicas, têm dificuldade em lembrar quais medicamentos já tomaram no dia. Esquecer ou tomar remédios em duplicata pode causar sérios riscos à saúde.

## 💡 Proposta da Solução

O Remédio Check é uma aplicação de linha de comando (CLI) que permite cadastrar medicamentos com horários, marcar quais já foram tomados no dia e resetar a lista para o próximo dia.

A partir da **v2.0.0**, os dados são persistidos em um **banco de dados PostgreSQL real na nuvem** (Supabase), substituindo o antigo armazenamento em arquivo JSON. A aplicação também consulta a base pública **OpenFDA** para exibir informações técnicas sobre medicamentos.

---

## ✅ Funcionalidades

- Adicionar remédio com nome e horário
- Listar todos os remédios e seus status
- Marcar remédio como tomado
- Remover remédio da lista
- Resetar o status de todos para um novo dia
- **Dados persistidos em banco PostgreSQL na nuvem (Supabase)**
- **Buscar informações de um remédio via API OpenFDA** (nome comercial, substância, fabricante, indicação)

---

## 🛠️ Stack de Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.9+ |
| Banco de Dados | Supabase (PostgreSQL) |
| API Externa | OpenFDA Drug Label API |
| Testes | pytest (unitários + integração com mocks) |
| Lint | ruff |
| CI/CD | GitHub Actions |
| Container | Docker |

---

## ⚙️ Instalação e Configuração

```bash
# 1. Clone o repositório
git clone https://github.com/mateus-alarcao/remedio-check.git
cd remedio-check

# 2. (Opcional) Crie um ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com sua URL e chave do Supabase
```

Conteúdo do `.env`:
```
SUPABASE_URL=https://nxkrpxgefmjuwbyssvwm.supabase.co
SUPABASE_KEY=sb_publishable_Q1wNgX10KUzgfmsQbjG2Jg_5e3lk338
```

---

## ▶️ Execução

```bash
python src/app.py
```

Exemplo de uso:

```
💊 Remédio Check v2.0.0
Seu lembrete diário de medicamentos
🗄️  Banco de dados: Supabase (PostgreSQL)

1. Adicionar remédio
2. Listar remédios
3. Marcar como tomado
4. Remover remédio
5. Resetar dia
6. Buscar informações de um remédio (OpenFDA)
0. Sair
```

---

## 🐳 Deploy via Docker

```bash
# Build da imagem
docker build -t remedio-check .

# Execução interativa com variáveis de ambiente
docker run --rm -it --env-file .env remedio-check
```

---

## 🧪 Rodando os Testes

```bash
pytest --tb=short -v
```

Saída esperada:

```
collected 30 items

tests/test_app.py          ........... 11 passed
tests/test_integracao.py   ....... 7 passed
tests/test_db.py           ............ 12 passed
```

> Todos os testes usam **mocks** — não precisam de conexão real com o banco ou a internet.

---

## 🔍 Rodando o Lint

```bash
ruff check src/ tests/
```

Saída esperada: nenhum erro ou aviso.

---

## 🔗 Integração com API Externa — OpenFDA

A aplicação consome a **[OpenFDA Drug Label API](https://open.fda.gov/apis/drug/label/)** — pública, gratuita e sem necessidade de chave de acesso.

```
6. Buscar informações de um remédio (OpenFDA)
Nome do remédio (preferencialmente em inglês): aspirin

📋 Informações encontradas:
   Nome comercial : Aspirin
   Substância     : ASPIRIN
   Fabricante     : Bayer HealthCare LLC
   Indicação      : Temporarily relieves minor aches and pains...
```

> ⚠️ A base OpenFDA é americana. Use o nome do princípio ativo em inglês (ex: `metformin`, `aspirin`, `omeprazole`).


```

---

## 📁 Estrutura do Projeto

```
remedio-check/
├── src/
│   ├── app.py               # Aplicação principal (CLI)
│   ├── api_medicamento.py   # Integração com a API OpenFDA
│   └── db.py                # Camada de banco de dados (Supabase)
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Configuração do pytest (sys.path)
│   ├── test_app.py          # Testes unitários
│   ├── test_integracao.py   # Testes de integração (OpenFDA com mock)
│   └── test_db.py           # Testes de integração (Supabase com mock)
├── .github/
│   └── workflows/
│       └── ci.yml           # Pipeline CI/CD
├── setup.sql                # Script SQL para criar a tabela no Supabase
├── Dockerfile
├── .env.example             # Modelo de variáveis de ambiente
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## 📌 Versão

`2.0.0` — Integração com banco de dados Supabase (PostgreSQL)

---

## 🔗 Links

- **Repositório:** [https://github.com/mateus-alarcao/remedio-check](https://github.com/mateus-alarcao/remedio-check)
