from django.contrib import admin
from django.urls import path, include
from payments import views  # Import your views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payments/', include('payments.urls')),  # Include your payments app URLs
    path('', views.homepage, name='homepage'),  # Root URL mapping to the homepage view
]
