import argparse
import sys

from Gitpyfuntion import (
    init_mygit,
    git_status,
    git_commit,
    git_add,
    show_log,
    git_pull,
    open_interface,
    start_server
)


def main():
    if "-help" in sys.argv:
        sys.argv = [arg for arg in sys.argv if arg != "-help"]
        sys.argv.insert(1, "--help")

    parser = argparse.ArgumentParser(
        prog="gitpy",
        description="Bem-vindo ao Gitpy, uma implementação simplificada do Git em Python!"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    init_parser = subparsers.add_parser(
        "init",
        help="Cria a estrutura interna mygit e inicia o servidor"
    )

    init_parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Porta do servidor Django (padrao: 8000)"
    )

    subparsers.add_parser(
        "status",
        help="Mostra o que tem no mygit ativo"
    )

    commit_parser = subparsers.add_parser(
        "commit",
        help="Registra um commit dentro do mygit ativo"
    )

    commit_parser.add_argument(
        "-m",
        "--message",
        required=True,
        help="Mensagem do commit"
    )

    add_parser = subparsers.add_parser(
        "add",
        help="Cria um arquivo .txt dentro do mygit com a mensagem"
    )

    add_parser.add_argument(
        "message",
        help="Mensagem para gravar no arquivo"
    )

    subparsers.add_parser(
        "log",
        help="Mostra o histórico salvo em mygit/log.txt"
    )

    pull_parser = subparsers.add_parser(
        "pull",
        help="Exporta o ultimo commit para o repository informado"
    )

    pull_parser.add_argument(
        "-t",
        "--target",
        required=True,
        help="Nome do repository de destino"
    )

    subparsers.add_parser(
        "interface",
        help="Abre a interface grafica do Gitpy"
    )

    args = parser.parse_args()

    if args.command == "init":
        init_mygit()
        start_server(port=args.port, background=True)

    elif args.command == "status":
        git_status()

    elif args.command == "commit":
        git_commit(args.message)

    elif args.command == "add":
        git_add(args.message)

    elif args.command == "log":
        show_log()

    elif args.command == "pull":
        git_pull(repo_name=args.target, create_if_missing=True)

    elif args.command == "interface":
        open_interface()
if __name__ == "__main__":
    main()
   
