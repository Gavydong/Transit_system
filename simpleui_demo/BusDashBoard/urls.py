
from django.contrib import admin
from django.urls import path,include


from BusDashBoard.views import BusesDashboard,eletricalDashBoard,fuelDashBoard


urlpatterns = [   
    path("", BusesDashboard, name="bus"),
    path("Electrical/",eletricalDashBoard),
    path("Fuel/",fuelDashBoard)
    
    
    
]
