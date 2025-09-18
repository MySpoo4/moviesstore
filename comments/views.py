from django.shortcuts import render
from movies.models import Review
from django.db.models import Count


def index(request):
    reviews = Review.objects.annotate(num_likes=Count("liked_by")).order_by(
        "-num_likes"
    )
    template_data = {}
    template_data["title"] = "Comments Home"
    template_data["reviews"] = reviews
    return render(request, "comments/index.html", {"template_data": template_data})
