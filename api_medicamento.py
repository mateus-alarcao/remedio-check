import json
import urllib.parse
import urllib.request

OPENFDA_URL = "https://api.fda.gov/drug/label.json"


def buscar_info_medicamento(nome: str) -> dict | None:
    """
    Consulta a API pública OpenFDA para buscar informações sobre um medicamento.

    Retorna um dicionário com campos relevantes ou None se não encontrar.
    """
    if not nome or not nome.strip():
        raise ValueError("O nome do medicamento não pode ser vazio.")

    params = urllib.parse.urlencode({
        "search": f'openfda.brand_name:"{nome.strip()}"',
        "limit": 1,
    })
    url = f"{OPENFDA_URL}?{params}"

    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception:
        return None

    resultados = data.get("results", [])
    if not resultados:
        return None

    resultado = resultados[0]
    openfda = resultado.get("openfda", {})

    return {
        "nome": openfda.get("brand_name", ["Não informado"])[0],
        "substancia": openfda.get("substance_name", ["Não informado"])[0],
        "fabricante": openfda.get("manufacturer_name", ["Não informado"])[0],
        "finalidade": resultado.get("indications_and_usage", ["Não informado"])[0][:300],
    }


def exibir_info_medicamento(nome: str) -> None:
    """Busca e exibe no terminal as informações do medicamento via OpenFDA."""
    print(f"\n🔍 Buscando informações sobre '{nome}' na base OpenFDA...")
    info = buscar_info_medicamento(nome)

    if info is None:
        print("⚠️  Medicamento não encontrado na base OpenFDA.")
        print("    (A base é americana; tente o nome em inglês, ex: 'aspirin', 'metformin')\n")
        return

    print("\n📋 Informações encontradas:")
    print(f"   Nome comercial : {info['nome']}")
    print(f"   Substância     : {info['substancia']}")
    print(f"   Fabricante     : {info['fabricante']}")
    print(f"   Indicação      : {info['finalidade']}")
    print()
