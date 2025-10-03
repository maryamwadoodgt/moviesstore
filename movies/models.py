from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    is_hidden = models.BooleanField(default=False)  # NEW FIELD
    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name


class Petition(models.Model):
    """A petition requesting that a movie be added to the catalog."""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.title}"

    def yes_count(self):
        return self.votes.filter(choice=True).count()


class PetitionVote(models.Model):
    """A vote by a user on a petition. choice=True means affirmative (yes)."""
    id = models.AutoField(primary_key=True)
    petition = models.ForeignKey(Petition, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.BooleanField(default=True)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('petition', 'user')

    def __str__(self):
        return f"Vote {self.id} - petition {self.petition_id} by {self.user_id}"