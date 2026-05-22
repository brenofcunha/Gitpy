from django.urls import path

from .views import commits_view, logs_view, pull_view, repositories_view

urlpatterns = [
	path("api/pull", pull_view, name="gitpy-pull"),
	path("api/repositories", repositories_view, name="gitpy-repositories"),
	path(
		"api/repositories/<str:repo_name>/commits",
		commits_view,
		name="gitpy-commits"
	),
	path("api/logs", logs_view, name="gitpy-logs"),
]
