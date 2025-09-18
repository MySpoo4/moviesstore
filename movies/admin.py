from django.contrib import admin
from .models import Like, Movie, Reply, Review, Wishlist, Rating


class MovieAdmin(admin.ModelAdmin):
    ordering = ["name"]
    search_fields = ["name"]


admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(Wishlist)
admin.site.register(Reply)
admin.site.register(Like)
admin.site.register(Rating)
