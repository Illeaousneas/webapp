# compliance/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('checks/', views.ComplianceCheckView.as_view()), 
]



