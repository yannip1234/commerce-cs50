from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category_title = models.CharField(max_length=64)
    category_desc = models.CharField(max_length=1024)

    def __str__(self):
        return f"{self.category_title}"


class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", blank=True, null=True)
    is_open = models.BooleanField(default=True)
    item_title = models.CharField(max_length=64)
    item_description = models.CharField(max_length=1024)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listing_category")
    img_url = models.URLField(blank=True)

    def __str__(self):
        return f"ID: {self.id} Title: {self.item_title} Category: {self.category}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist_listing")


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_listing")
    title = models.CharField(max_length=64)
    name = models.CharField(max_length=32)
    date = models.DateField(auto_now=True)
    comment = models.CharField(max_length=1024)


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing")
    user_bid = models.DecimalField(decimal_places=2, null=True, max_digits=10, default=0.0)
    user_id = models.CharField(max_length=64)

    def __str__(self):
        return "%s %s" % (self.user_bid, self.user_id)

