from django.urls import path
from . import views

urlpatterns = [
    path('availability/', views.submit_availability),
    path('optimize/', views.get_optimal_timeslot),
]