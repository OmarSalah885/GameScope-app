from django.shortcuts import render,redirect
from django.urls import reverse
from django.urls import reverse_lazy
from .models import Game,Review,Comment
from .forms import GameForm ,ReviewForm,CommentForm
from django.contrib.auth.forms import UserCreationForm #form to create  new user
from django.contrib.auth.models import User # built in User model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView



def home(request):
    featured_games = Game.objects.order_by('-rating_average')[:5]
    return render(request, 'home.html', {'featured_games': featured_games})


# GAME VIEWS
# --------------------------------------------------------------------



class GameListView(ListView):
    model = Game
    template_name = 'game/game_list.html'
    context_object_name = 'all_games'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        genre = self.request.GET.get('genre')
        platform = self.request.GET.get('platform')
        sort = self.request.GET.get('sort', '-release_date')

        if search:
            queryset = queryset.filter(name__icontains=search)
        if genre:
            queryset = queryset.filter(genre__iexact=genre)
        if platform:
            queryset = queryset.filter(platform__iexact=platform)

        valid_sort_fields = [
            'name', '-name', 'release_date', '-release_date',
            'rating_average', '-rating_average'
        ]
        if sort in valid_sort_fields:
            queryset = queryset.order_by(sort)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        valid_sort_fields = {
            'name': 'Name (A–Z)',
            '-name': 'Name (Z–A)',
            'release_date': 'Oldest First',
            '-release_date': 'Newest First',
            'rating_average': 'Lowest Rated',
            '-rating_average': 'Highest Rated',
        }

        context["genre_list"] = Game.objects.values_list('genre', flat=True).distinct()
        context["platform_list"] = Game.objects.values_list('platform', flat=True).distinct()
        context["current_sort"] = self.request.GET.get('sort', '-release_date')
        context["valid_sort_fields"] = valid_sort_fields

        
        context["current_search"] = self.request.GET.get('search', '')
        context["current_genre"] = self.request.GET.get('genre', '')
        context["current_platform"] = self.request.GET.get('platform', '')

        return context


class GameDetailView(DetailView):
    model = Game
    template_name = 'game/game_details.html'
    context_object_name = 'found_game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.get_object()
        reviews = Review.objects.filter(game=game).order_by('-created_at').select_related('user')

        reviews_with_comments = []
        for review in reviews:
            comments = Comment.objects.filter(review=review).order_by('created_at').select_related('user')
            reviews_with_comments.append({
                'review': review,
                'comments': comments
            })

        context["reviews_with_comments"] = reviews_with_comments
        return context





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