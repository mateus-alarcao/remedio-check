"""
test_db.py — Testes de integração da camada de banco de dados (Supabase).

Usa unittest.mock para simular o cliente Supabase, garantindo que os testes
rodem sem conexão real com a internet ou banco de dados configurado.
"""

from unittest.mock import MagicMock

from db import (
    adicionar_remedio_db,
    carregar_dados,
    marcar_tomado_db,
    remover_remedio_db,
    resetar_dia_db,
)

# ── Helper: cria um mock do cliente Supabase ──────────────────────────────────


def _make_client(data: list) -> MagicMock:
    """
    Cria um MagicMock que simula o cliente Supabase.

    Todas as cadeias de chamadas terminam com .execute() retornando
    um objeto cujo atributo .data contém os dados fornecidos.
    """
    mock = MagicMock()
    mock_response = MagicMock()
    mock_response.data = data

    # SELECT → .table().select().order().execute()
    mock.table.return_value.select.return_value.order.return_value.execute.return_value = (
        mock_response
    )
    # INSERT → .table().insert().execute()
    mock.table.return_value.insert.return_value.execute.return_value = mock_response
    # UPDATE eq → .table().update().eq().execute()
    mock.table.return_value.update.return_value.eq.return_value.execute.return_value = (
        mock_response
    )
    # UPDATE neq (resetar_dia) → .table().update().neq().execute()
    mock.table.return_value.update.return_value.neq.return_value.execute.return_value = (
        mock_response
    )
    # DELETE → .table().delete().eq().execute()
    mock.table.return_value.delete.return_value.eq.return_value.execute.return_value = (
        mock_response
    )

    return mock


# ── Testes: carregar_dados ────────────────────────────────────────────────────


class TestCarregarDados:
    def test_retorna_lista_de_remedios(self):
        dados = [{"id": 1, "nome": "Aspirina", "horario": "08:00", "tomado": False}]
        client = _make_client(dados)
        resultado = carregar_dados(client=client)
        assert resultado == dados

    def test_retorna_lista_vazia_quando_banco_vazio(self):
        client = _make_client([])
        resultado = carregar_dados(client=client)
        assert resultado == []

    def test_retorna_multiplos_remedios(self):
        dados = [
            {"id": 1, "nome": "Paracetamol", "horario": "08:00", "tomado": False},
            {"id": 2, "nome": "Ibuprofeno", "horario": "14:00", "tomado": True},
        ]
        client = _make_client(dados)
        resultado = carregar_dados(client=client)
        assert len(resultado) == 2
        assert resultado[0]["nome"] == "Paracetamol"
        assert resultado[1]["tomado"] is True


# ── Testes: adicionar_remedio_db ──────────────────────────────────────────────


class TestAdicionarRemedioDB:
    def test_insere_remedio_e_retorna_registro(self):
        novo = {"id": 1, "nome": "Metformina", "horario": "12:00", "tomado": False}
        client = _make_client([novo])
        resultado = adicionar_remedio_db("Metformina", "12:00", client=client)
        assert resultado["nome"] == "Metformina"
        assert resultado["horario"] == "12:00"
        assert resultado["tomado"] is False

    def test_chama_table_correta(self):
        client = _make_client([{"id": 1, "nome": "X", "horario": "08:00", "tomado": False}])
        adicionar_remedio_db("X", "08:00", client=client)
        client.table.assert_called_with("remedios")

    def test_nome_e_horario_sao_enviados_sem_espacos(self):
        dados = [{"id": 1, "nome": "Vitamina C", "horario": "07:00", "tomado": False}]
        client = _make_client(dados)
        adicionar_remedio_db("  Vitamina C  ", "  07:00  ", client=client)
        insert_call_args = client.table.return_value.insert.call_args[0][0]
        assert insert_call_args["nome"] == "Vitamina C"
        assert insert_call_args["horario"] == "07:00"
# ── Testes: marcar_tomado_db ──────────────────────────────────────────────────


class TestMarcarTomadoDB:
    def test_marca_remedio_como_tomado(self):
        atualizado = {"id": 1, "nome": "Aspirina", "horario": "08:00", "tomado": True}
        client = _make_client([atualizado])
        resultado = marcar_tomado_db(1, client=client)
        assert resultado["tomado"] is True

    def test_chama_update_com_tomado_true(self):
        client = _make_client([{"id": 2, "nome": "X", "horario": "08:00", "tomado": True}])
        marcar_tomado_db(2, client=client)
        update_call_args = client.table.return_value.update.call_args[0][0]
        assert update_call_args == {"tomado": True}


# ── Testes: remover_remedio_db ────────────────────────────────────────────────


class TestRemoverRemedioDB:
    def test_remove_remedio_e_retorna_registro(self):
        removido = {"id": 3, "nome": "Ômega 3", "horario": "12:00", "tomado": False}
        client = _make_client([removido])
        resultado = remover_remedio_db(3, client=client)
        assert resultado["nome"] == "Ômega 3"
        assert resultado["id"] == 3

    def test_chama_delete_com_id_correto(self):
        client = _make_client([{"id": 5, "nome": "X", "horario": "08:00", "tomado": False}])
        remover_remedio_db(5, client=client)
        eq_call_args = client.table.return_value.delete.return_value.eq.call_args
        assert eq_call_args[0] == ("id", 5)


# ── Testes: resetar_dia_db ────────────────────────────────────────────────────


class TestResetarDiaDB:
    def test_reseta_todos_remedios(self):
        client = _make_client([])
        # Não deve lançar exceção
        resetar_dia_db(client=client)

    def test_chama_update_com_tomado_false(self):
        client = _make_client([])
        resetar_dia_db(client=client)
        update_call_args = client.table.return_value.update.call_args[0][0]
        assert update_call_args == {"tomado": False}
