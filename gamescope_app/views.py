from django.shortcuts import render,redirect
from django.urls import reverse
from django.urls import reverse_lazy
from .models import Game,Review,Comment
from .forms import GameForm ,ReviewForm,CommentForm
from django.contrib.auth.forms import UserCreationForm #form to create  new user
from django.contrib.auth.models import User # built in User model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# GAME VIEWS
# --------------------------------------------------------------------

class GameListView(ListView):
    model = Game
    template_name = 'game/game_list.html'
    context_object_name = 'all_games'
    ordering = ['-release_date']
    paginate_by = 12

class GameDetailView(DeleteView):
    model:Game
    template_name='game/game_details.html'
    context_object_name='found_game'




# REVIEWS VIEWS
# --------------------------------------------------------------------
class ReviewListView(ListView):
    model:Game
    template_name='game/game_list.html'
    context_object_name='all_games'

class ReviewDetailView(DeleteView):
    model:Game
    template_name='game/game_details.html'
    context_object_name='found_game'


class ReviewCreateView(CreateView):
    model:Game
    form_class=GameForm
    template_name='game/game_form.html'
    success_url=reverse_lazy('game_list')


class ReviewUpdateView(UpdateView):
    model:Game
    form_class=GameForm
    template_name='game/game_form.html'
    success_url=reverse_lazy('game_list')


class ReviewDeleteView(DeleteView):
    model:Game
    success_url=reverse_lazy('game_list')

# COMMENT VIEWS
# --------------------------------------------------------------------

class CommentListView(ListView):
    model:Game
    template_name='game/game_list.html'
    context_object_name='all_games'

class CommentDetailView(DeleteView):
    model:Game
    template_name='game/game_details.html'
    context_object_name='found_game'


class CommentCreateView(CreateView):
    model:Game
    form_class=GameForm
    template_name='game/game_form.html'
    success_url=reverse_lazy('game_list')


class CommentUpdateView(UpdateView):
    model:Game
    form_class=GameForm
    template_name='game/game_form.html'
    success_url=reverse_lazy('game_list')


class CommentDeleteView(DeleteView):
    model:Game
    success_url=reverse_lazy('game_list')