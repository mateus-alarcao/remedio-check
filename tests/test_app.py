
import pytest
from src.app import adicionar_remedio, marcar_tomado, remover_remedio, resetar_dia


def test_adicionar_remedio_valido():
    remedios = []
    remedio = adicionar_remedio(remedios, "Paracetamol", "08:00")
    assert len(remedios) == 1
    assert remedio["nome"] == "Paracetamol"
    assert remedio["horario"] == "08:00"
    assert remedio["tomado"] is False


def test_adicionar_varios_remedios():
    remedios = []
    adicionar_remedio(remedios, "Vitamina C", "07:00")
    adicionar_remedio(remedios, "Ômega 3", "12:00")
    assert len(remedios) == 2


def test_adicionar_nome_vazio_gera_erro():
    remedios = []
    with pytest.raises(ValueError):
        adicionar_remedio(remedios, "", "08:00")


def test_adicionar_horario_vazio_gera_erro():
    remedios = []
    with pytest.raises(ValueError):
        adicionar_remedio(remedios, "Dipirona", "")


def test_adicionar_nome_apenas_espacos():
    remedios = []
    with pytest.raises(ValueError):
        adicionar_remedio(remedios, "   ", "08:00")



def test_marcar_tomado():
    remedios = []
    adicionar_remedio(remedios, "Ibuprofeno", "09:00")
    marcar_tomado(remedios, 0)
    assert remedios[0]["tomado"] is True


def test_marcar_tomado_indice_invalido():
    remedios = []
    adicionar_remedio(remedios, "Aspirina", "10:00")
    with pytest.raises(IndexError):
        marcar_tomado(remedios, 5)


def test_marcar_tomado_indice_negativo():
    remedios = []
    adicionar_remedio(remedios, "Aspirina", "10:00")
    with pytest.raises(IndexError):
        marcar_tomado(remedios, -1)



def test_remover_remedio():
    remedios = []
    adicionar_remedio(remedios, "Metformina", "08:00")
    removido = remover_remedio(remedios, 0)
    assert removido["nome"] == "Metformina"
    assert len(remedios) == 0


def test_remover_indice_invalido():
    remedios = []
    with pytest.raises(IndexError):
        remover_remedio(remedios, 0)



def test_resetar_dia():
    remedios = []
    adicionar_remedio(remedios, "Vitamina D", "07:00")
    adicionar_remedio(remedios, "Ferro", "12:00")
    marcar_tomado(remedios, 0)
    marcar_tomado(remedios, 1)
    resetar_dia(remedios)
    assert all(r["tomado"] is False for r in remedios)
