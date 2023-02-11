from django.urls import path

from . import views

# if you decide to  add app_name here, then you have to refer to it in html: <a href="{% url 'encyclopedia:index' %}">Home</a>
# app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),    # placing "search" path turned out to be CRITICAL, since when it was below "<str:title>" path, search never got to be accessed and called.
    path("new_page", views.new_page, name="new_page"),
    path("edit_page", views.edit_page, name="edit_page"),
    path("save_edit", views.save_edit, name="save_edit"),
    path("<str:title>", views.display_contents, name="title")
]
