from django.shortcuts import render, redirect
from django.urls import reverse,reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Game, Review, Comment
from .forms import ReviewForm, CommentForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView


def home(request):
    featured_games = Game.objects.order_by('-rating_average')[:5]
    return render(request, 'home.html', {'featured_games': featured_games})

# GAME VIEWS
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

        valid_sort_fields = ['name', '-name', 'release_date', '-release_date', 'rating_average', '-rating_average']
        return queryset.order_by(sort if sort in valid_sort_fields else '-release_date')

    def get_paginate_by(self, queryset):
        return self.paginate_by

    def paginate_queryset(self, queryset, page_size):
        return super().paginate_queryset(queryset, page_size)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        valid_sort_fields = {
            'name': 'Name (A–Z)', '-name': 'Name (Z–A)', 'release_date': 'Oldest First',
            '-release_date': 'Newest First', 'rating_average': 'Lowest Rated', '-rating_average': 'Highest Rated'
        }
        if self.paginate_by:
            paginator, page, queryset, is_paginated = self.paginate_queryset(self.get_queryset(), self.paginate_by)
            context[self.context_object_name] = page

        querydict = self.request.GET.copy()
        if 'page' in querydict:
            querydict.pop('page')
        context.update({
            'genre_list': Game.objects.values_list('genre', flat=True).distinct(),
            'platform_list': Game.objects.values_list('platform', flat=True).distinct(),
            'current_sort': self.request.GET.get('sort', '-release_date'),
            'valid_sort_fields': valid_sort_fields,
            'current_search': self.request.GET.get('search', ''),
            'current_genre': self.request.GET.get('genre', ''),
            'current_platform': self.request.GET.get('platform', ''),
            'query_string': querydict.urlencode() if querydict else ''
        })
        return context

class GameDetailView(DetailView):
    model = Game
    template_name = 'game/game_details.html'
    context_object_name = 'found_game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.get_object()
        reviews = Review.objects.filter(game=game).order_by('-created_at').select_related('user')
        context['reviews_with_comments'] = [
            {'review': review, 'comments': Comment.objects.filter(review=review, parent__isnull=True).order_by('created_at').select_related('user')}
            for review in reviews
        ]
        return context

# REVIEW VIEWS
class ReviewListView(ListView):
    model = Review
    template_name = 'review/review_list.html'
    context_object_name = 'all_reviews'

    def get_queryset(self):
        return super().get_queryset().select_related('game', 'user').order_by('-created_at')

class ReviewDetailView(DetailView):
    model = Review
    template_name = 'review/review_detail.html'
    context_object_name = 'found_review'

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review/review_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.game = get_object_or_404(Game, pk=self.kwargs['game_id'])
        if Review.objects.filter(user=self.request.user, game=form.instance.game).exists():
            form.add_error(None, "You have already reviewed this game.")
            return self.form_invalid(form)
        response = super().form_valid(form)
        messages.success(self.request, "Review created successfully!")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game'] = get_object_or_404(Game, pk=self.kwargs['game_id'])
        return context

    def get_success_url(self):
        return reverse('game_detail', kwargs={'pk': self.kwargs['game_id']})

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review/review_form.html'

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game'] = self.get_object().game
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Review updated successfully!")
        return response

    def get_success_url(self):
        return reverse('game_detail', kwargs={'pk': self.object.game.pk})

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'review/review_confirm_delete.html'

    def test_func(self):
        return self.get_object().user == self.request.user

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, "Review deleted successfully!")
        return response

    def get_success_url(self):
        return reverse('game_detail', kwargs={'pk': self.object.game.pk})


# COMMENT VIEWS
class CommentListView(ListView):
    model = Comment
    template_name = 'comment/comment_list.html'
    context_object_name = 'all_comments'

    def get_queryset(self):
        return super().get_queryset().select_related('review', 'user').order_by('-created_at')

class CommentDetailView(DetailView):
    model = Comment
    template_name = 'comment/comment_detail.html'
    context_object_name = 'found_comment'

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment/comment_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        parent_id = self.request.POST.get('parent_id')
        if parent_id:
            form.instance.parent = get_object_or_404(Comment, pk=parent_id)
        response = super().form_valid(form)
        messages.success(self.request, "Comment created successfully!")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review'] = get_object_or_404(Review, pk=self.kwargs['review_id'])
        parent_id = self.request.GET.get('parent_id')
        if parent_id:
            context['parent_comment'] = get_object_or_404(Comment, pk=parent_id)
        return context

    def get_success_url(self):
        return reverse('game_detail', kwargs={'pk': self.object.review.game.pk})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment/comment_form.html'

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review'] = self.get_object().review
        return context

    def get_success_url(self):
        return reverse('game_detail', kwargs={'pk': self.object.review.game.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment/comment_confirm_delete.html'

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_success_url(self):
        return reverse('game_detail', kwargs={'pk': self.object.review.game.pk})
    


class SignUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, "Account created successfully! You can now log in.")
        return super().form_valid(form)