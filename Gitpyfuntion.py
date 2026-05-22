import os
import subprocess
from datetime import datetime


MYGIT_DIR = "mygit"
COMMITS_DIR = os.path.join(MYGIT_DIR, "commits")
LOG_FILE = os.path.join(MYGIT_DIR, "log.txt")


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def init_mygit():
    os.makedirs(COMMITS_DIR, exist_ok=True)

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as file:
            file.write("Histórico do Gitpy\n")
            file.write("==================\n\n")

    write_log("Sistema mygit inicializado.")
    print("Estrutura mygit criada com sucesso.")


def write_log(message: str):
    os.makedirs(COMMITS_DIR, exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"[{now()}] {message}\n")


def run_git_command(command: list[str]):
    try:
        result = subprocess.run(
            command,
            text=True,
            capture_output=True
        )

        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(result.stderr)

        return result

    except FileNotFoundError:
        print("Erro: Git não encontrado. Verifique se o Git está instalado.")
        write_log("Erro: Git não encontrado.")
        return None


def git_status():
    write_log("Executou git status.")
    run_git_command(["git", "status"])


def list_branches():
    write_log("Listou branches.")
    run_git_command(["git", "branch"])


def create_branch(branch_name: str):
    write_log(f"Tentou criar branch: {branch_name}")
    result = run_git_command(["git", "checkout", "-b", branch_name])

    if result and result.returncode == 0:
        write_log(f"Branch criada com sucesso: {branch_name}")


def switch_branch(branch_name: str):
    write_log(f"Tentou trocar para branch: {branch_name}")
    result = run_git_command(["git", "checkout", branch_name])

    if result and result.returncode == 0:
        write_log(f"Branch alterada com sucesso: {branch_name}")


def git_commit(message: str):
    init_mygit()

    write_log(f"Iniciando commit: {message}")

    add_result = run_git_command(["git", "add", "."])

    if not add_result or add_result.returncode != 0:
        write_log("Erro ao executar git add.")
        return

    commit_result = run_git_command(["git", "commit", "-m", message])

    if commit_result and commit_result.returncode == 0:
        write_log(f"Commit criado com sucesso: {message}")
        save_commit_record(message)
    else:
        write_log(f"Falha ao criar commit: {message}")


def save_commit_record(message: str):
    commit_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    commit_file = os.path.join(COMMITS_DIR, f"commit_{commit_id}.txt")

    current_branch = get_current_branch()

    with open(commit_file, "w", encoding="utf-8") as file:
        file.write("Registro de Commit - Gitpy\n")
        file.write("==========================\n\n")
        file.write(f"Data: {now()}\n")
        file.write(f"Branch: {current_branch}\n")
        file.write(f"Mensagem: {message}\n")

    write_log(f"Registro de commit salvo em: {commit_file}")


def get_current_branch():
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        text=True,
        capture_output=True
    )

    if result.returncode == 0:
        return result.stdout.strip()

    return "branch desconhecida"


def show_log():
    if not os.path.exists(LOG_FILE):
        print("Nenhum log encontrado. Execute primeiro:")
        print("python Gitpy.py init")
        return

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        print(file.read())