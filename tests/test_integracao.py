"""
Testes de integração — valida o fluxo de comunicação com a API OpenFDA.

Utiliza unittest.mock para simular as respostas HTTP, garantindo que
os testes rodem sem dependência de conexão real com a internet.
"""

import json
from unittest.mock import MagicMock, patch

import pytest
from src.api_medicamento import buscar_info_medicamento

# ── Resposta simulada da API OpenFDA ─────────────────────────────────────────

RESPOSTA_OPENFDA_VALIDA = {
    "results": [
        {
            "openfda": {
                "brand_name": ["Aspirin"],
                "substance_name": ["ASPIRIN"],
                "manufacturer_name": ["Bayer HealthCare LLC"],
            },
            "indications_and_usage": [
                "Temporarily relieves minor aches and pains due to headache, "
                "toothache, backache, menstrual cramps, the common cold, "
                "muscle aches and pains, and minor arthritis pain."
            ],
        }
    ]
}

RESPOSTA_OPENFDA_VAZIA = {"results": []}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _mock_urlopen(payload: dict):
    """Cria um mock de urllib.request.urlopen que retorna `payload` como JSON."""
    conteudo = json.dumps(payload).encode("utf-8")
    mock_response = MagicMock()
    mock_response.read.return_value = conteudo
    mock_response.__enter__ = lambda s: s
    mock_response.__exit__ = MagicMock(return_value=False)
    return mock_response


# ── Testes ────────────────────────────────────────────────────────────────────

class TestBuscarInfoMedicamento:
    """Testes de integração para buscar_info_medicamento (com mock HTTP)."""

    def test_retorna_dados_corretos_quando_api_encontra_medicamento(self):
        """Quando a API retorna um resultado, os campos devem ser mapeados corretamente."""
        with patch("src.api_medicamento.urllib.request.urlopen") as mock_open:
            mock_open.return_value = _mock_urlopen(RESPOSTA_OPENFDA_VALIDA)

            resultado = buscar_info_medicamento("aspirin")

        assert resultado is not None
        assert resultado["nome"] == "Aspirin"
        assert resultado["substancia"] == "ASPIRIN"
        assert resultado["fabricante"] == "Bayer HealthCare LLC"
        assert "aches and pains" in resultado["finalidade"]

    def test_retorna_none_quando_medicamento_nao_encontrado(self):
        """Quando a API retorna lista vazia, a função deve retornar None."""
        with patch("src.api_medicamento.urllib.request.urlopen") as mock_open:
            mock_open.return_value = _mock_urlopen(RESPOSTA_OPENFDA_VAZIA)

            resultado = buscar_info_medicamento("xyzinexistente")

        assert resultado is None

    def test_retorna_none_quando_api_falha(self):
        """Quando a requisição HTTP lança exceção, a função deve retornar None."""
        with patch("src.api_medicamento.urllib.request.urlopen", side_effect=Exception("timeout")):
            resultado = buscar_info_medicamento("aspirin")

        assert resultado is None

    def test_url_montada_com_nome_correto(self):
        """Garante que a URL enviada à API contém o nome buscado."""
        with patch("src.api_medicamento.urllib.request.urlopen") as mock_open:
            mock_open.return_value = _mock_urlopen(RESPOSTA_OPENFDA_VAZIA)

            buscar_info_medicamento("metformin")

            url_chamada = mock_open.call_args[0][0]
            assert "metformin" in url_chamada

    def test_nome_vazio_lanca_value_error(self):
        """Nome vazio deve lançar ValueError antes mesmo de chamar a API."""
        with pytest.raises(ValueError):
            buscar_info_medicamento("")

    def test_nome_apenas_espacos_lanca_value_error(self):
        """Nome com apenas espaços deve lançar ValueError."""
        with pytest.raises(ValueError):
            buscar_info_medicamento("   ")

    def test_finalidade_truncada_em_300_caracteres(self):
        """O campo finalidade deve ser truncado em até 300 caracteres."""
        texto_longo = "A" * 500
        payload = {
            "results": [
                {
                    "openfda": {
                        "brand_name": ["TestDrug"],
                        "substance_name": ["TESTDRUG"],
                        "manufacturer_name": ["Lab X"],
                    },
                    "indications_and_usage": [texto_longo],
                }
            ]
        }
        with patch("src.api_medicamento.urllib.request.urlopen") as mock_open:
            mock_open.return_value = _mock_urlopen(payload)
            resultado = buscar_info_medicamento("testdrug")

        assert len(resultado["finalidade"]) <= 300
