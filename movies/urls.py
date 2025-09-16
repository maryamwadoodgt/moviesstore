from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='movies.index'),
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/review/create/', views.create_review, name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='movies.delete_review'),
    # NEW CODE, unsure about the first line after this
    path("", views.movie_list, name="movie_list"),
    path("hidden-movies/", views.hidden_movies, name="hidden_movies"),
    path("hide/<int:movie_id>/", views.hide_movie, name="hide_movie"),
    path("unhide/<int:movie_id>/", views.unhide_movie, name="unhide_movie"),
]