import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from Gitpyfuntion import (
    get_commit_history,
    get_logs,
    git_pull,
    load_repositories,
)


def index_view(request):
    return render(request, "index.html")


@csrf_exempt
def pull_view(request):
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "output": "Método não permitido."},
            status=405
        )

    payload = json.loads(request.body or "{}")
    repo_name = payload.get("repo_name")
    create_if_missing = bool(payload.get("create_if_missing"))
    result = git_pull(repo_name=repo_name, create_if_missing=create_if_missing)

    return JsonResponse(result)


def repositories_view(request):
    if request.method != "GET":
        return JsonResponse(
            {"success": False, "output": "Método não permitido."},
            status=405
        )

    repos = load_repositories()
    return JsonResponse({
        "success": True,
        "repositories": list(repos.values())
    })


def commits_view(request, repo_name: str):
    if request.method != "GET":
        return JsonResponse(
            {"success": False, "output": "Método não permitido."},
            status=405
        )

    repos = load_repositories()
    repo = repos.get(repo_name)
    if not repo:
        return JsonResponse(
            {"success": False, "output": "Repositório não encontrado."},
            status=404
        )

    commits = get_commit_history(repo_path=repo["path"])
    return JsonResponse({
        "success": True,
        "commits": commits
    })


def logs_view(request):
    if request.method != "GET":
        return JsonResponse(
            {"success": False, "output": "Método não permitido."},
            status=405
        )

    return JsonResponse({
        "success": True,
        "logs": get_logs()
    })