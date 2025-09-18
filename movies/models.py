from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to="movie_images/")

    # rating system
    def avg_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.stars for r in ratings) / ratings.count(), 1)
        return 0

    def rating_count(self):
        return self.ratings.count()

    def __str__(self):
        return f"{str(self.id)} - {self.name}"


class Rating(models.Model):
    # fix 1-5 rating later
    movie = models.ForeignKey(Movie, related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField()

    class Meta:
        unique_together = ("movie", "user")


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="liked_reviews", blank=True)

    def likes_count(self):
        return self.liked_by.count()

    def __str__(self):
        return str(self.id) + " - " + self.movie.name


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlists")
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="wishlisted_by"
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "movie")

    def __str__(self):
        return f"{self.user.username} wishes for {self.movie.name}"


class Reply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="replies")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.username} on review {self.review.id}"


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="liked_movies"
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="likes")
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "movie")

    def __str__(self):
        return f"{self.user.username} likes {self.movie.name}"
