from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Game, Review, Comment
from .forms import ReviewForm, CommentForm

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
        else:
            queryset = queryset.order_by('-release_date')  # Default ordering

        print(f"Queryset count: {queryset.count()}")  # Debug line
        return queryset

    def get_paginate_by(self, queryset):
        print(f"get_paginate_by returned: {self.paginate_by}")
        return self.paginate_by

    def paginate_queryset(self, queryset, page_size):
        print(f"paginate_queryset called with page_size={page_size}")
        paginator, page, queryset, is_paginated = super().paginate_queryset(queryset, page_size)
        print(f"paginate_queryset returned: paginator={type(paginator)}, page={type(page)}, is_paginated={is_paginated}")
        return paginator, page, queryset, is_paginated

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

        # Explicitly set paginated object if pagination is enabled
        if self.paginate_by:
            paginator, page, queryset, is_paginated = self.paginate_queryset(self.get_queryset(), self.paginate_by)
            context[self.context_object_name] = page

        context["genre_list"] = Game.objects.values_list('genre', flat=True).distinct()
        context["platform_list"] = Game.objects.values_list('platform', flat=True).distinct()
        context["current_sort"] = self.request.GET.get('sort', '-release_date')
        context["valid_sort_fields"] = valid_sort_fields
        context["current_search"] = self.request.GET.get('search', '')
        context["current_genre"] = self.request.GET.get('genre', '')
        context["current_platform"] = self.request.GET.get('platform', '')

        # Prepare query string without 'page'
        querydict = self.request.GET.copy()
        querydict.pop('page', None)
        context["query_string"] = querydict.urlencode()

        # Debug pagination info
        print(f"Paginate by: {self.paginate_by}")
        print(f"Context['all_games'] type: {type(context['all_games'])}")
        try:
            print(f"Paginator count: {context['all_games'].paginator.count}")
            print(f"Has next: {context['all_games'].has_next()}")
            print(f"Has previous: {context['all_games'].has_previous()}")
            print(f"Current page: {context['all_games'].number}")
            print(f"Total pages: {context['all_games'].paginator.num_pages}")
        except AttributeError as e:
            print(f"Error accessing pagination attributes: {e}")

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
            comments = Comment.objects.filter(review=review, parent__isnull=True).order_by('created_at').select_related('user')
            reviews_with_comments.append({
                'review': review,
                'comments': comments
            })

        context["reviews_with_comments"] = reviews_with_comments
        return context

# REVIEW VIEWS
# --------------------------------------------------------------------
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
        form.instance.game = Game.objects.get(pk=self.kwargs['game_id'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game'] = Game.objects.get(pk=self.kwargs['game_id'])
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

    def get_success_url(self):
        return reverse('game_detail', kwargs={'pk': self.object.game.pk})

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'review/review_confirm_delete.html'

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_success_url(self):
        return reverse('game_detail', kwargs={'pk': self.object.game.pk})

# COMMENT VIEWS
# --------------------------------------------------------------------
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
        form.instance.review = Review.objects.get(pk=self.kwargs['review_id'])
        parent_id = self.request.POST.get('parent_id')
        if parent_id:
            form.instance.parent = Comment.objects.get(pk=parent_id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review'] = Review.objects.get(pk=self.kwargs['review_id'])
        parent_id = self.request.GET.get('parent_id')
        if parent_id:
            context['parent_comment'] = Comment.objects.get(pk=parent_id)
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