from django.urls import include, path

from interface.views import index_view

urlpatterns = [
    path("", index_view, name="gitpy-index"),
    path("", include("interface.urls")),
]
