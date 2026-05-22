import json
import os
import shutil
import subprocess
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_MYGIT_DIR = os.path.join(BASE_DIR, "mygit")
COMMITS_DIR = os.path.join(BASE_MYGIT_DIR, "commits")
ADDED_DIR = os.path.join(BASE_MYGIT_DIR, "added")
LOG_FILE = os.path.join(BASE_MYGIT_DIR, "log.txt")
REPOS_FILE = os.path.join(BASE_MYGIT_DIR, "repositories.json")
PULL_LOG_FILE = os.path.join(BASE_MYGIT_DIR, "pull_log.txt")
REPO_BASE_DIR = "/run/media/breno-cunha/00C61FD2C61FC6B6/Repository local"


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def init_mygit():
    os.makedirs(BASE_MYGIT_DIR, exist_ok=True)
    os.makedirs(COMMITS_DIR, exist_ok=True)
    os.makedirs(ADDED_DIR, exist_ok=True)

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as file:
            file.write("Historico do Gitpy\n")
            file.write("==================\n\n")

    if not os.path.exists(PULL_LOG_FILE):
        with open(PULL_LOG_FILE, "w", encoding="utf-8") as file:
            file.write("Historico de Pulls\n")
            file.write("==================\n\n")

    if not os.path.exists(REPOS_FILE):
        with open(REPOS_FILE, "w", encoding="utf-8") as file:
            file.write("{}")

    write_log("Sistema mygit inicializado.")
    print("Estrutura mygit criada com sucesso.")


def get_repo_name(path: str):
    return os.path.basename(path)


def ensure_repo_base_dir():
    os.makedirs(REPO_BASE_DIR, exist_ok=True)
    return REPO_BASE_DIR


def load_repositories():
    if not os.path.exists(REPOS_FILE):
        return {}

    with open(REPOS_FILE, "r", encoding="utf-8") as file:
        content = file.read().strip()
        if not content:
            return {}
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {}


def save_repositories(repos: dict):
    os.makedirs(BASE_MYGIT_DIR, exist_ok=True)

    with open(REPOS_FILE, "w", encoding="utf-8") as file:
        json.dump(repos, file, ensure_ascii=False, indent=2)


def register_repository(repo_name: str, repo_path: str):
    init_mygit()

    repos = load_repositories()

    repos[repo_name] = {
        "name": repo_name,
        "path": repo_path,
        "last_pull": now()
    }

    save_repositories(repos)
    return repos


def write_log(message: str):
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"[{now()}] {message}\n")


def write_pull_log(repo_name: str, commit_name: str):
    with open(PULL_LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"[{now()}] repo={repo_name} commit={commit_name}\n")


def run_git_command(command: list[str], cwd: str | None = None):
    try:
        result = subprocess.run(
            command,
            text=True,
            capture_output=True,
            cwd=cwd
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
    write_log("Executou gitpy status.")

    if not os.path.isdir(BASE_MYGIT_DIR):
        print("Nenhum mygit encontrado. Execute: gitpy init")
        return

    print(f"mygit: {BASE_MYGIT_DIR}")
    if os.path.isdir(ADDED_DIR):
        added_files = sorted(os.listdir(ADDED_DIR))
        print(f"added: {len(added_files)}")
        for name in added_files:
            print(f"- {name}")
    else:
        print("added: 0")

    if os.path.isdir(COMMITS_DIR):
        commits = sorted(os.listdir(COMMITS_DIR))
        print(f"commits: {len(commits)}")
        for name in commits[-5:]:
            print(f"- {name}")
    else:
        print("commits: 0")

    if os.path.exists(LOG_FILE):
        print(f"log: {LOG_FILE}")
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            lines = [line.rstrip() for line in file.readlines() if line.strip()]
        if lines:
            print("ultimos logs:")
            for line in lines[-5:]:
                print(f"- {line}")




def git_commit(message: str):
    init_mygit()

    write_log(f"Iniciando commit: {message}")

    added_files = sorted(os.listdir(ADDED_DIR)) if os.path.isdir(ADDED_DIR) else []
    if not added_files:
        print("Nenhum arquivo adicionado. Use: gitpy add <arquivo>")
        write_log("Commit cancelado: nenhum arquivo adicionado.")
        return

    commit_dir = os.path.join(COMMITS_DIR, f"commit_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    os.makedirs(commit_dir, exist_ok=True)

    for name in added_files:
        source_path = os.path.join(ADDED_DIR, name)
        dest_path = os.path.join(commit_dir, name)
        shutil.move(source_path, dest_path)

    save_commit_record(message, commit_dir)
    write_log(f"Commit registrado com sucesso: {message}")


def save_commit_record(message: str, commit_dir: str):
    commit_file = os.path.join(commit_dir, "info.txt")

    with open(commit_file, "w", encoding="utf-8") as file:
        file.write("Registro de Commit - Gitpy\n")
        file.write("==========================\n\n")
        file.write(f"Data: {now()}\n")
        file.write(f"Mensagem: {message}\n")

    write_log(f"Registro de commit salvo em: {commit_file}")


def get_current_branch():
    return "mygit"


def show_log():
    if not os.path.isdir(COMMITS_DIR):
        print("Nenhum commit encontrado. Execute primeiro:")
        print("gitpy commit -m \"mensagem\"")
        return

    commits = sorted(os.listdir(COMMITS_DIR))
    if not commits:
        print("Nenhum commit encontrado.")
        return

    for commit_name in commits:
        commit_path = os.path.join(COMMITS_DIR, commit_name)
        if not os.path.isdir(commit_path):
            continue
        print(f"{commit_name}:")
        for filename in sorted(os.listdir(commit_path)):
            print(f"- {filename}")


def get_logs(limit: int = 200):
    if not os.path.exists(PULL_LOG_FILE):
        return []

    with open(PULL_LOG_FILE, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]

    formatted = []
    for line in lines[-limit:]:
        if line.startswith("[") and "repo=" in line and "commit=" in line:
            timestamp, rest = line.split("]", 1)
            repo_name = ""
            commit_name = ""
            for part in rest.strip().split():
                if part.startswith("repo="):
                    repo_name = part.replace("repo=", "")
                if part.startswith("commit="):
                    commit_name = part.replace("commit=", "")

            message = commit_name
            info_path = os.path.join(REPO_BASE_DIR, repo_name, commit_name, "info.txt")
            if os.path.exists(info_path):
                with open(info_path, "r", encoding="utf-8") as info_file:
                    for info_line in info_file:
                        if info_line.startswith("Mensagem:"):
                            message = info_line.replace("Mensagem:", "").strip()
                            break

            formatted.append(f"{timestamp}] repo={repo_name} mensagem={message}")
        else:
            formatted.append(line)

    return formatted


def get_commit_history(limit: int = 20, repo_path: str | None = None):
    if repo_path:
        git_dir = os.path.join(repo_path, ".git")
        if not os.path.isdir(git_dir):
            commits = []
            for name in sorted(os.listdir(repo_path)):
                commit_path = os.path.join(repo_path, name)
                if not os.path.isdir(commit_path):
                    continue
                info_path = os.path.join(commit_path, "info.txt")
                if not os.path.exists(info_path):
                    continue
                message = "(sem mensagem)"
                date_value = datetime.fromtimestamp(os.stat(info_path).st_mtime).strftime("%Y-%m-%d")
                with open(info_path, "r", encoding="utf-8") as file:
                    for line in file:
                        if line.startswith("Mensagem:"):
                            message = line.replace("Mensagem:", "").strip()
                        if line.startswith("Data:"):
                            date_value = line.replace("Data:", "").strip().split(" ")[0]
                commits.append({
                    "hash": name,
                    "author": "gitpy",
                    "date": date_value,
                    "message": message
                })
            return commits

    result = subprocess.run(
        [
            "git",
            "log",
            f"-n{limit}",
            "--date=short",
            "--pretty=format:%h|%an|%ad|%s"
        ],
        text=True,
        capture_output=True,
        cwd=repo_path
    )

    if result.returncode != 0:
        return []

    commits = []
    for line in result.stdout.splitlines():
        parts = line.split("|", 3)
        if len(parts) != 4:
            continue
        hash_value, author, date, message = parts
        commits.append({
            "hash": hash_value,
            "author": author,
            "date": date,
            "message": message
        })

    return commits


def create_pull_repository(repo_name: str):
    base_dir = ensure_repo_base_dir()
    repo_path = os.path.join(base_dir, repo_name)
    os.makedirs(repo_path, exist_ok=True)

    register_repository(repo_name, repo_path)
    write_log(f"Repositorio criado: {repo_name} em {repo_path}.")
    return {
        "name": repo_name,
        "path": repo_path,
        "warning": None
    }


def open_interface():
    import webbrowser

    webbrowser.open("http://127.0.0.1:8000/")


def git_pull_remote():
    write_log("Iniciando git pull remoto do Gitpy.")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    result = run_git_command(["git", "pull"], cwd=base_dir)

    if result and result.returncode == 0:
        write_log("git pull remoto executado com sucesso.")
        return {
            "success": True,
            "output": result.stdout
        }

    error_output = result.stderr if result else "Erro ao executar git pull."
    write_log(f"Erro ao executar git pull remoto: {error_output}")
    return {
        "success": False,
        "output": error_output
    }

def git_pull(repo_name: str | None = None, create_if_missing: bool = False):
    init_mygit()
    write_log("Iniciando gitpy pull (exporta commit).")

    if not os.path.isdir(COMMITS_DIR):
        return {
            "success": False,
            "output": "Nenhum commit encontrado."
        }

    commits = sorted([name for name in os.listdir(COMMITS_DIR) if name.startswith("commit_")])
    if not commits:
        return {
            "success": False,
            "output": "Nenhum commit encontrado."
        }

    latest_commit = commits[-1]
    source_path = os.path.join(COMMITS_DIR, latest_commit)

    ensure_repo_base_dir()

    if not repo_name:
        return {
            "success": False,
            "output": "Nome do repositorio nao informado."
        }

    repo_path = os.path.join(REPO_BASE_DIR, repo_name)
    if not os.path.exists(repo_path):
        if not create_if_missing:
            return {
                "success": False,
                "output": "Repositorio nao encontrado.",
                "needs_create": True
            }
        create_pull_repository(repo_name)

    target_path = os.path.join(repo_path, latest_commit)
    if os.path.exists(target_path):
        suffix = 1
        while os.path.exists(f"{target_path}_{suffix}"):
            suffix += 1
        target_path = f"{target_path}_{suffix}"

    shutil.copytree(source_path, target_path)
    register_repository(repo_name, repo_path)
    write_pull_log(repo_name, os.path.basename(target_path))

    write_log("gitpy pull executado com sucesso.")
    return {
        "success": True,
        "output": f"Commit exportado: {os.path.basename(target_path)}",
        "repository": {
            "name": repo_name,
            "path": repo_path,
            "warning": None
        }
    }


def git_add(message: str):
    init_mygit()

    if not message.strip():
        print("Mensagem vazia.")
        write_log("Falha ao adicionar arquivo: mensagem vazia.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"added_{timestamp}.txt"
    dest_path = os.path.join(ADDED_DIR, filename)

    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(message.strip() + "\n")

    write_log(f"Arquivo adicionado: {filename}")
    print(f"Arquivo criado: {filename}")


def start_server(port: int = 8000, background: bool = False):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    manage_path = os.path.join(base_dir, "manage.py")
    if not os.path.exists(manage_path):
        print("manage.py nao encontrado. Execute a partir do projeto Gitpy.")
        return

    write_log("Iniciando servidor Django.")
    command = [
        "python3",
        manage_path,
        "runserver",
        str(port)
    ]

    if background:
        subprocess.Popen(
            command,
            cwd=base_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"Servidor iniciado em background na porta {port}.")
        return

    subprocess.run(command, cwd=base_dir)