from django.urls import path
from . import views

urlpatterns =[
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.registerpage,name="register"),
    path('',views.home , name="home"),
    path('room/<str:pk>/',views.room ,name="room"),
    path('createroom/',views.createRoom,name="createroom"),
    path('updateroom/<str:pk>/',views.updateRoom,name="updateroom"),
    path('deleteroom/<str:pk>/',views.deleteRoom,name="deleteroom"),
    path('delete-message/<str:pk>/',views.deleteMessage,name="delete-message"),
    path('profile/<str:pk>/',views.userprofile,name="user-profile"),
    
    path('update-user/',views.updateuser,name="updateuser"),
    path('topics/',views.topicsPage,name="topics"),
    path('activity/',views.activityPage,name="activity"),
  

]


