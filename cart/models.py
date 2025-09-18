from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class OrderStatus(models.TextChoices):
        ORDER_PROCESSING = "P", _("Order Processing")
        SHIPPING = "S", _("Shipping")
        DELIVERED = "D", _("Delivered")

    status = models.CharField(
        max_length=1,
        choices=OrderStatus.choices,
        default=OrderStatus.ORDER_PROCESSING,
    )

    def __str__(self):
        return str(self.id) + " - " + self.user.username

    # def get_order_status(self) -> OrderStatus:
    #     # Get value from choices enum
    #     return self.OrderStatus(self.status)


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + " - " + self.movie.name


# Create your models here.
