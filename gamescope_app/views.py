from django.shortcuts import render,redirect
from django.urls import reverse
from django.urls import reverse_lazy
from .models import Game,Review,Comment
# from .forms import GamesForm ,DlcForm
from django.contrib.auth.forms import UserCreationForm #form to create  new user
from django.contrib.auth.models import User # built in User model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.
class GameListView(ListView):
    model:Game
    template_name=''