from django.contrib import admin
from compliance import views
from django.urls import path, include
from compliance import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('compliance.urls')),
    path('checks/', views.ComplianceCheckView.as_view()),
    path('', include('compliance.urls')),
]
