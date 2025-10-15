from django.contrib import admin
from .models import Game, Review, Comment
from django.utils.safestring import mark_safe

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'genre', 'platform', 'release_date', 'cover_image_preview']
    list_filter = ['genre', 'platform', 'release_date']
    search_fields = ['name', 'description', 'developer']
    fields = [
        'name', 'description', 'genre', 'number_of_players', 'platform',
        'release_date', 'downloads', 'rating_average', 'tags', 'developer',
        'cover_image'
    ]

    def cover_image_preview(self, obj):
        if obj.cover_image:
            return mark_safe(f'<img src="{obj.cover_image.url}" style="max-width: 100px; max-height: 100px;" />')
        return "No Image"
    cover_image_preview.short_description = 'Cover Image'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['game', 'user', 'rating', 'created_at']
    list_filter = ['game', 'rating', 'created_at']
    search_fields = ['game__name', 'user__username', 'content']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['review', 'user', 'created_at']
    list_filter = ['review', 'created_at']
    search_fields = ['review__game__name', 'user__username', 'text']