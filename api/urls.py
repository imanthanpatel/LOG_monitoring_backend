from django.urls import path
from accounts.views import Logout,UserList,DeleteUser,UpdateUser


urlpatterns= [
        path("user-list/", UserList.as_view(), name="user-list"),
        path("users/<int:id>/", UpdateUser.as_view(), name="UserUpdate"),
        path("users/<int:id>/delete", DeleteUser.as_view(), name="user-delete"),

]