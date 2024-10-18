from django.urls import path
from . import views

urlpatterns = [
    path('stk_push/', views.stk_push, name='stk_push'),
    path('callback/', views.mpesa_callback, name='mpesa_callback'),
]
