from django.urls import path
from .views import Register,Login,CurrentUser,Logout,UserList,DeleteUser,UpdateUser



urlpatterns = [
    path("register/", Register.as_view(),name="register"),
    path("login/", Login.as_view(),name="login"),
    path("logout/", Logout.as_view(),name="logout"),
    path("me/", CurrentUser.as_view(), name="current-user"),
    # path("user-list/", UserList.as_view(), name="user-list"),
    # path("users/<int:id>/", UpdateUser.as_view(), name="UserUpdate"),
    # path("users/<int:id>/delete", DeleteUser.as_view(), name="user-list"),

]