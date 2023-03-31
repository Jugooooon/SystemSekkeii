from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name = "index"),
    path('login/', views.MyLoginView.as_view(), name="login"),
    path('logout/', views.MyLogoutView.as_view(), name="logout"),
    path('index2/',views.index2, name="index2"),
    path('state/',views.StateView, name = "state"),
    path('search/',views.Search,name='search'),
    path('shirahama1f/',views.CheckIn,name='shirahama1f'),
    path('shirahama2f/',views.CheckIn2,name='shirahama2f'),
    path('makeMaps/',views.MakeMaps,name='makeMaps'),
    path('rooms/',views.RoomsView.as_view(), name='rooms'),
    path('showMap/',views.ShowMap,name='showMap'),
    path('addImage/',views.MakeImages,name='addImage'),
    path('test', views.test, name='test'),
]