import json
import os

from api_medicamento import exibir_info_medicamento

VERSION = "1.1.0"
DATA_FILE = "remedios.json"


def carregar_dados() -> list:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def salvar_dados(remedios: list) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(remedios, f, ensure_ascii=False, indent=2)


def adicionar_remedio(remedios: list, nome: str, horario: str) -> dict:
    if not nome or not nome.strip():
        raise ValueError("O nome do remédio não pode ser vazio.")
    if not horario or not horario.strip():
        raise ValueError("O horário não pode ser vazio.")
    remedio = {"nome": nome.strip(), "horario": horario.strip(), "tomado": False}
    remedios.append(remedio)
    return remedio


def marcar_tomado(remedios: list, indice: int) -> dict:
    if indice < 0 or indice >= len(remedios):
        raise IndexError("Índice inválido.")
    remedios[indice]["tomado"] = True
    return remedios[indice]


def remover_remedio(remedios: list, indice: int) -> dict:
    if indice < 0 or indice >= len(remedios):
        raise IndexError("Índice inválido.")
    return remedios.pop(indice)


def listar_remedios(remedios: list) -> None:
    if not remedios:
        print("Nenhum remédio cadastrado.")
        return
    print("\n--- Lista de Remédios ---")
    for i, r in enumerate(remedios):
        status = "✅ Tomado" if r["tomado"] else "⬜ Pendente"
        print(f"[{i}] {r['nome']} — {r['horario']} — {status}")
    print("-------------------------\n")


def resetar_dia(remedios: list) -> None:
    for r in remedios:
        r["tomado"] = False


def menu() -> None:
    print(f"\n💊 Remédio Check v{VERSION}")
    print("Seu lembrete diário de medicamentos\n")
    remedios = carregar_dados()

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
                adicionar_remedio(remedios, nome, horario)
                salvar_dados(remedios)
                print("✅ Remédio adicionado!")
            except ValueError as e:
                print(f"Erro: {e}")

        elif opcao == "2":
            listar_remedios(remedios)

        elif opcao == "3":
            listar_remedios(remedios)
            try:
                idx = int(input("Número do remédio: "))
                marcar_tomado(remedios, idx)
                salvar_dados(remedios)
                print("✅ Marcado como tomado!")
            except (ValueError, IndexError) as e:
                print(f"Erro: {e}")

        elif opcao == "4":
            listar_remedios(remedios)
            try:
                idx = int(input("Número do remédio a remover: "))
                removido = remover_remedio(remedios, idx)
                salvar_dados(remedios)
                print(f"🗑️ '{removido['nome']}' removido.")
            except (ValueError, IndexError) as e:
                print(f"Erro: {e}")

        elif opcao == "5":
            resetar_dia(remedios)
            salvar_dados(remedios)
            print("🔄 Todos os remédios resetados para o novo dia!")

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
