import googlemaps
import os
from dotenv import load_dotenv

from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from movies.models import Movie, MoviePurchaseLocation
from .utils import calculate_cart_total
from .models import Order, Item
from django.contrib.auth.decorators import login_required

load_dotenv()  

MAPS_API_KEY = os.environ.get("MAPS_API_KEY")
gmaps = googlemaps.Client(key=MAPS_API_KEY)


def index(request):
    cart_total = 0
    movies_in_cart = []
    cart = request.session.get("cart", {})
    movie_ids = list(cart.keys())
    if movie_ids != []:
        movies_in_cart = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart, movies_in_cart)

    template_data = {}
    template_data["title"] = "Cart"
    template_data["movies_in_cart"] = movies_in_cart
    template_data["cart_total"] = cart_total
    return render(request, "cart/index.html", {"template_data": template_data})


def add(request, id):
    get_object_or_404(Movie, id=id)
    cart = request.session.get("cart", {})
    cart[id] = request.POST["quantity"]
    request.session["cart"] = cart
    return redirect("cart.index")


def add_to_cart(request, id):
    get_object_or_404(Movie, id=id)
    cart = request.session.get("cart", {})
    cart[id] = request.POST["quantity"]
    request.session["cart"] = cart
    return redirect("cart.index")


def clear(request):
    request.session["cart"] = {}
    return redirect("cart.index")


@login_required
def purchase(request):
    cart = request.session.get("cart", {})
    movie_ids = list(cart.keys())
    if movie_ids == []:
        return redirect("cart.index")

    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)

    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()

    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.id)]
        item.save()

    user_state = request.session.get('user_state')
    if user_state and user_state != 'Unknown':
        for movie in movies_in_cart:
            quantity = int(cart[str(movie.id)])
            
            try:
                movie_purchase_location = MoviePurchaseLocation.objects.get(
                    movie=movie, 
                    state=user_state
                )
                movie_purchase_location.times_purchased += quantity
                movie_purchase_location.save()
                print(f"Updated MoviePurchaseLocation: {movie.name} in {user_state} - now {movie_purchase_location.times_purchased} times")
            except MoviePurchaseLocation.DoesNotExist:
                movie_purchase_location = MoviePurchaseLocation(
                    movie=movie,
                    state=user_state,
                    times_purchased=quantity
                )
                movie_purchase_location.save()
                print(f"Created new MoviePurchaseLocation: {movie.name} in {user_state} - {quantity} times")

    request.session["cart"] = {}
    template_data = {}
    template_data["title"] = "Purchase confirmation"
    template_data["order_id"] = order.id
    return render(request, "cart/purchase.html", {"template_data": template_data})


@require_http_methods(["POST"])
def save_location(request):
    """
    Handle geolocation coordinates from JavaScript in cart
    """
    if request.method == 'POST':
        try:
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            
            if latitude and longitude:
                print(f"Cart User Location - Latitude: {latitude}, Longitude: {longitude}")
                reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))
                state = 'Unknown'
                if reverse_geocode_result:
                    for result in reverse_geocode_result:
                        for comp in result.get("address_components", []):
                            if "administrative_area_level_1" in comp.get("types", []):
                                state = comp.get("long_name", "Unknown")
                                break
                        if state != 'Unknown':
                            break
                print(f"State: {state}")
                
                request.session['user_state'] = state
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Location and state saved successfully',
                    'latitude': latitude,
                    'longitude': longitude,
                    'state': state
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Missing latitude or longitude data'
                }, status=400)
        except Exception as e:
            print(f"Error processing location in cart: {e}")
            return JsonResponse({
                'status': 'error',
                'message': 'Error processing location data'
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)
