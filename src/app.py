from dotenv import load_dotenv
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

load_dotenv()
from api_medicamento import exibir_info_medicamento  # noqa: E402
from db import (  # noqa: E402
    adicionar_remedio_db,
    carregar_dados,
    marcar_tomado_db,
    remover_remedio_db,
    resetar_dia_db,
)

VERSION = "2.0.0"
console = Console()


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
        console.print(
            Panel(
                "Nenhum remédio cadastrado.",
                title="Remédios",
                border_style="yellow",
                box=box.ROUNDED,
            )
        )
        return

    tabela = Table(
        title=f"Remédios cadastrados ({len(remedios)})",
        box=box.SIMPLE_HEAVY,
        header_style="bold cyan",
        show_lines=False,
    )
    tabela.add_column("Nº", justify="right", style="cyan", no_wrap=True)
    tabela.add_column("Horário", style="magenta", no_wrap=True)
    tabela.add_column("Status", no_wrap=True)
    tabela.add_column("Remédio", style="bold")

    for i, r in enumerate(remedios):
        status = "[green]Tomado[/green]" if r["tomado"] else "[yellow]Pendente[/yellow]"
        tabela.add_row(str(i), r["horario"], status, r["nome"])

    console.print()
    console.print(tabela)
    console.print()


def imprimir_menu_principal() -> None:
    """Exibe as opções do menu principal."""
    titulo = Text()
    titulo.append("Remédio Check", style="bold cyan")
    titulo.append(f" v{VERSION}", style="cyan")

    console.print()
    console.print(
        Panel(
            Text("Controle diário de medicamentos\nSupabase • PostgreSQL", justify="center"),
            title=titulo,
            border_style="cyan",
            box=box.DOUBLE,
            padding=(1, 4),
        )
    )

    menu_tabela = Table.grid(padding=(0, 2))
    menu_tabela.add_column(style="bold cyan", no_wrap=True)
    menu_tabela.add_column()
    menu_tabela.add_row("[1]", "Adicionar remédio")
    menu_tabela.add_row("[2]", "Listar remédios")
    menu_tabela.add_row("[3]", "Marcar como tomado")
    menu_tabela.add_row("[4]", "Remover remédio")
    menu_tabela.add_row("", "")
    menu_tabela.add_row("[5]", "Resetar dia")
    menu_tabela.add_row("", "")
    menu_tabela.add_row("[6]", "Buscar informações no OpenFDA")
    menu_tabela.add_row("", "")
    menu_tabela.add_row("[0]", "Sair")

    console.print(
        Panel(
            menu_tabela,
            title="Menu principal",
            border_style="blue",
            box=box.ROUNDED,
            padding=(1, 2),
        )
    )


# ── Menu principal (usa o banco de dados Supabase) ────────────────────────────


def menu() -> None:
    print("\nSeu lembrete diário de medicamentos")

    while True:
        imprimir_menu_principal()
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
