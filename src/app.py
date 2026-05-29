
from api_medicamento import exibir_info_medicamento
from db import (
    adicionar_remedio_db,
    carregar_dados,
    marcar_tomado_db,
    remover_remedio_db,
    resetar_dia_db,
)

VERSION = "2.0.0"


# ── Funções de negócio puras (sem I/O) ────────────────────────────────────────
# Mantidas para compatibilidade com os testes unitários existentes.


def adicionar_remedio(remedios: list, nome: str, horario: str) -> dict:
    """Valida e adiciona um remédio à lista em memória (usado nos testes unitários)."""
    if not nome or not nome.strip():
        raise ValueError("O nome do remédio não pode ser vazio.")
    if not horario or not horario.strip():
        raise ValueError("O horário não pode ser vazio.")
    remedio = {"nome": nome.strip(), "horario": horario.strip(), "tomado": False}
    remedios.append(remedio)
    return remedio


def marcar_tomado(remedios: list, indice: int) -> dict:
    """Marca um remédio da lista em memória como tomado (usado nos testes unitários)."""
    if indice < 0 or indice >= len(remedios):
        raise IndexError("Índice inválido.")
    remedios[indice]["tomado"] = True
    return remedios[indice]


def remover_remedio(remedios: list, indice: int) -> dict:
    """Remove um remédio da lista em memória (usado nos testes unitários)."""
    if indice < 0 or indice >= len(remedios):
        raise IndexError("Índice inválido.")
    return remedios.pop(indice)


def resetar_dia(remedios: list) -> None:
    """Reseta todos os remédios da lista em memória (usado nos testes unitários)."""
    for r in remedios:
        r["tomado"] = False


def listar_remedios(remedios: list) -> None:
    """Imprime a lista de remédios formatada no terminal."""
    if not remedios:
        print("Nenhum remédio cadastrado.")
        return
    print("\n--- Lista de Remédios ---")
    for i, r in enumerate(remedios):
        status = "✅ Tomado" if r["tomado"] else "⬜ Pendente"
        print(f"[{i}] {r['nome']} — {r['horario']} — {status}")
    print("-------------------------\n")


# ── Menu principal (usa o banco de dados Supabase) ────────────────────────────


def menu() -> None:
    print(f"\n💊 Remédio Check v{VERSION}")
    print("Seu lembrete diário de medicamentos")
    print("🗄️  Banco de dados: Supabase (PostgreSQL)\n")

    while True:
        print("1. Adicionar remédio")
        print("2. Listar remédios")
        print("3. Marcar como tomado")
        print("4. Remover remédio")
        print("5. Resetar dia")
        print("6. Buscar informações de um remédio (OpenFDA)")
        print("0. Sair")
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome do remédio: ")
            horario = input("Horário (ex: 08:00): ")
            try:
                # Reutiliza validação da função pura antes de gravar no banco
                tmp: list = []
                adicionar_remedio(tmp, nome, horario)
                adicionar_remedio_db(nome, horario)
                print("✅ Remédio adicionado no banco de dados!")
            except ValueError as e:
                print(f"Erro: {e}")
            except EnvironmentError as e:
                print(f"❌ Erro de configuração: {e}")

        elif opcao == "2":
            try:
                remedios = carregar_dados()
                listar_remedios(remedios)
            except EnvironmentError as e:
                print(f"❌ Erro de configuração: {e}")

        elif opcao == "3":
            try:
                remedios = carregar_dados()
                listar_remedios(remedios)
                if not remedios:
                    continue
                idx = int(input("Número do remédio: "))
                if idx < 0 or idx >= len(remedios):
                    raise IndexError("Índice inválido.")
                marcar_tomado_db(remedios[idx]["id"])
                print("✅ Marcado como tomado!")
            except (ValueError, IndexError) as e:
                print(f"Erro: {e}")
            except EnvironmentError as e:
                print(f"❌ Erro de configuração: {e}")

        elif opcao == "4":
            try:
                remedios = carregar_dados()
                listar_remedios(remedios)
                if not remedios:
                    continue
                idx = int(input("Número do remédio a remover: "))
                if idx < 0 or idx >= len(remedios):
                    raise IndexError("Índice inválido.")
                removido = remover_remedio_db(remedios[idx]["id"])
                print(f"🗑️  '{removido['nome']}' removido do banco de dados.")
            except (ValueError, IndexError) as e:
                print(f"Erro: {e}")
            except EnvironmentError as e:
                print(f"❌ Erro de configuração: {e}")

        elif opcao == "5":
            try:
                resetar_dia_db()
                print("🔄 Todos os remédios resetados para o novo dia!")
            except EnvironmentError as e:
                print(f"❌ Erro de configuração: {e}")

        elif opcao == "6":
            nome = input("Nome do remédio para buscar (preferencialmente em inglês): ")
            exibir_info_medicamento(nome)

        elif opcao == "0":
            print("Até logo! Cuide-se. 💊")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
