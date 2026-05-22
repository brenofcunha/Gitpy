import argparse

from Gitpyfuntion import (
    init_mygit,
    git_status,
    list_branches,
    create_branch,
    switch_branch,
    git_commit,
    show_log,
)


def main():
    parser = argparse.ArgumentParser(
        prog="gitpy",
        description="Bem-vindo ao Gitpy, uma implementação simplificada do Git em Python!"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    subparsers.add_parser(
        "init",
        help="Cria a estrutura interna mygit/"
    )

    subparsers.add_parser(
        "status",
        help="Mostra o status do Git"
    )

    branch_parser = subparsers.add_parser(
        "branch",
        help="Gerencia branches"
    )

    branch_group = branch_parser.add_mutually_exclusive_group(required=True)

    branch_group.add_argument(
        "--list",
        action="store_true",
        help="Lista branches"
    )

    branch_group.add_argument(
        "--create",
        type=str,
        help="Cria uma nova branch"
    )

    branch_group.add_argument(
        "--switch",
        type=str,
        help="Troca para uma branch existente"
    )

    commit_parser = subparsers.add_parser(
        "commit",
        help="Adiciona arquivos e cria um commit"
    )

    commit_parser.add_argument(
        "-m",
        "--message",
        required=True,
        help="Mensagem do commit"
    )

    subparsers.add_parser(
        "log",
        help="Mostra o histórico salvo em mygit/log.txt"
    )

    args = parser.parse_args()

    if args.command == "init":
        init_mygit()

    elif args.command == "status":
        git_status()

    elif args.command == "branch":
        if args.list:
            list_branches()
        elif args.create:
            create_branch(args.create)
        elif args.switch:
            switch_branch(args.switch)

    elif args.command == "commit":
        git_commit(args.message)

    elif args.command == "log":
        show_log()


if __name__ == "__main__":
    main()
   
