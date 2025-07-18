

from django.urls import path

from movie_review import views


urlpatterns=[
    path("registration_page/",views.registration_page,name="registration_page"),
    path("add_user/",views.add_user,name="add_user"),
    path("login_page/",views.login_page,name="login_page"),
    path("login/",views.login,name="login"),
    path("add_movie_page/",views.add_movies_page,name="add_movie_page"),
    path("add_movie/",views.add_movie,name="add_movie"),
    path("movie_details_page/<int:id>/",views.movie_details_page,name="movie_details_page"),
    path("add_like/",views.add_like,name="add_like"),
    path("add_dislike/",views.add_dislike,name="add_dislike"),
    path("add_rating/",views.add_rating,name="add_rating"),
    path("view_liked_movie_page/",views.view_liked_movies_page,name="view_liked_movie_page"),
    path("add_review/<int:id>/",views.add_review,name="add_review"),
    path("view_movies_page/",views.view_movies_page,name="view_movies_page"),
    path("delete_movie/<int:id>/",views.delete_movie,name="delete_movie"),
    path("home_page/",views.home_page,name="home_page"),
    path("search_movie/",views.search_movie,name="search_movie"),
    path("view_search_result_page/<str:search>/",views.view_search_result_page,name="view_search_result_page"),
    path("add_or_remove_save/",views.add_or_remove_save,name="add_or_remove_save"),
    path("check_json_response/",views.check_json_response,name="check_json_response"),
    path("view_user_profile_page/<int:id>/",views.view_user_profile_page,name="view_user_profile_page"),
    path("view_user_rated_movie_page/<int:id>/",views.view_user_rated_movie_page,name="view_user_rated_movie_page"),
    path("view_user_liked_movie/<int:id>/",views.view_user_liked_movie,name="view_user_liked_movie"),
    path("view_latest_movie_page/",views.view_latest_movie_page,name="view_latest_movie_page"),
    path("view_profile_page/",views.view_profile_page,name="view_profile_page"),
    path("logout/",views.logout,name="logout"),
    path("forget_password/",views.forget_password,name="forget_password"),
    path("change_password_page/<int:id>/<str:token>/",views.change_password_page,name="change_password_page"),
    path("change_password/<int:id>/<str:secret>/",views.change_password,name="change_password"),

    

]