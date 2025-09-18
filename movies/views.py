from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Movie, Rating, Review, Wishlist, Reply, Like


# Create your views here.
@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect("movies.show", id=id)


@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect("movies.show", id=id)
    if request.method == "GET":
        template_data = {}
        template_data["title"] = "Edit Review"
        template_data["review"] = review
        return render(
            request, "movies/edit_review.html", {"template_data": template_data}
        )
    elif request.method == "POST" and request.POST["comment"] != "":
        review = Review.objects.get(id=review_id)
        review.comment = request.POST["comment"]
        review.save()
        return redirect("movies.show", id=id)
    else:
        return redirect("movies.show", id=id)


def index(request):
    search_term = request.GET.get("search")
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {}
    template_data["title"] = "Movies"
    template_data["movies"] = movies
    return render(request, "movies/index.html", {"template_data": template_data})


def show(request, id):
    movie = get_object_or_404(Movie, id=id)
    reviews = Review.objects.filter(movie=movie)
    wishlisted_movie_ids = []
    if request.user.is_authenticated:
        wishlisted_movie_ids = list(
            request.user.wishlists.values_list("movie_id", flat=True)
        )
    liked_movie_ids = []
    if request.user.is_authenticated:
        liked_movie_ids = list(
            request.user.liked_movies.values_list("movie_id", flat=True)
        )
    template_data = {
        "movie": movie,
        "reviews": reviews,
        "wishlisted_movie_ids": wishlisted_movie_ids,
        "liked_movie_ids": liked_movie_ids,
    }
    return render(
        request,
        "movies/show.html",
        {"template_data": template_data, "user": request.user},
    )


@login_required
def edit_rating(request, id, rating_id):
    review = get_object_or_404(Rating, id=rating_id)
    if request.user != review.user:
        return redirect("movies.show", id=id)
    elif request.method == "POST":
        review = Rating.objects.get(id=rating_id)
        review.stars = request.POST["stars"]
        review.save()
        return redirect("movies.show", id=id)
    else:
        return redirect("movies.show", id=id)


@login_required
def create_review(request, id):
    if request.method == "POST" and request.POST["comment"] != "":
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST["comment"]
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect("movies.show", id=id)
    else:
        return redirect("movies.show", id=id)


@login_required
def add_to_wishlist(request, id):
    movie = get_object_or_404(Movie, id=id)
    Wishlist.objects.get_or_create(user=request.user, movie=movie)
    return redirect("movies.show", id=id)


@login_required
def remove_from_wishlist(request, id):
    movie = get_object_or_404(Movie, id=id)
    Wishlist.objects.filter(user=request.user, movie=movie).delete()
    return redirect("movies.show", id=id)


@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related("movie")
    return render(request, "movies/wishlist.html", {"wishlist_items": wishlist_items})


@login_required
def toggle_like(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, movie_id=id)
    user = request.user
    if user in review.liked_by.all():
        review.liked_by.remove(user)
    else:
        review.liked_by.add(user)
    return redirect("movies.show", id=id)


@login_required
def add_reply(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, movie_id=id)
    if request.method == "POST":
        comment = request.POST.get("comment")
        if comment:
            Reply.objects.create(review=review, user=request.user, comment=comment)
    return redirect("movies.show", id=id)


@login_required
def like_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    Like.objects.get_or_create(user=request.user, movie=movie)
    return redirect("movies.show", id=id)


@login_required
def unlike_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    Like.objects.filter(user=request.user, movie=movie).delete()
    return redirect("movies.show", id=id)


@login_required
def liked_movies(request):
    liked = Movie.objects.filter(likes__user=request.user)
    return render(request, "movies/liked_movies.html", {"liked_movies": liked})


@login_required
def rate_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    if request.method == "POST":
        stars = request.POST.get("stars")
        if stars and stars.isdigit():
            stars = int(stars)
            if 1 <= stars <= 5:
                print(stars)
                rating, created = Rating.objects.get_or_create(
                    user=request.user,
                    movie=movie,
                    defaults={'stars': stars}  # This sets stars when creating
                )
                if not created:
                    rating.stars = stars
                    rating.save()
    return redirect("movies.show", id=id)
