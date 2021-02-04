from django.urls import path
from testing_user import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view())
]
