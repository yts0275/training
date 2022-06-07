from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    score = models.IntegerField()


class Comment(models.Model):
    content = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)