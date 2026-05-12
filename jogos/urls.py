from django.urls import path
from .views import LoginView, JogosListCreateView, JogoDetailView

urlpatterns = [
    path('login', LoginView.as_view()),
    path('jogos', JogosListCreateView.as_view()),
    path('jogos/<int:id>', JogoDetailView.as_view()),
]