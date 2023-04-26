from django.shortcuts import render

# Create your views here.

def BusesDashboard(request):
    return render(request,"BusDashBoard/Dashboard.html")


def eletricalDashBoard(request):
    return render(request,"BusDashBoard/electrical_dasboard.html")

    
def fuelDashBoard(request):
    return render(request,"BusDashBoard/fuel_dashboard.html")