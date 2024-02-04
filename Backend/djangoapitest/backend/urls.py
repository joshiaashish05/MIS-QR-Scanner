# urls.py
from django.urls import path
from backend import views


urlpatterns = [
    path('home/',views.home),
    path('login/',views.LoginView.as_view()),
    path('logout/',views.LogoutView.as_view()),
    path('plant/<str:plantid>/', views.PlantDataView.as_view()),
    path('plant/', views.AllPlants.as_view()),
    path('plant/<str:plantid>/storedlocations/', views.PlantStoredLocations.as_view()),
    path('plant/<str:plantid>/storedlocations/<str:storedid>/materials/', views.MaterialDataView.as_view()),
    path('plant/<str:plantid>/storedlocations/<str:storedid>/materials/<str:material_number>/',
         views.MaterialDetailByNumber.as_view()),
    path('plant/<int:plantid>/storedlocations/<int:storedid>/materials/<int:materialid>/check-material-history/', views.CheckMaterialHistoryList.as_view(), name='check-material-history-list'),
]
