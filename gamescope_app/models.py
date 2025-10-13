from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    number_of_players = models.IntegerField()
    platform = models.CharField(max_length=50)
    release_date = models.DateField()
    downloads = models.IntegerField(null=True, blank=True)
    rating_average = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    tags = models.TextField(null=True, blank=True)
    developer = models.CharField(max_length=100, null=True, blank=True)
    cover_image = models.ImageField(upload_to='games/covers/', null=True, blank=True, help_text='Upload a cover image for the game (e.g., poster).')
    created_at = models.DateTimeField(auto_now_add=True)   
    updated_at = models.DateTimeField(auto_now=True)   
    
    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rating = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s review of {self.game.name} ({self.rating}/5)"

class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.review.game.name}"