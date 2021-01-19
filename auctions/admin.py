from django.contrib import admin
from .models import Listing, Bid, Comment, Category, Watchlist
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Watchlist)
admin.site.register(User, UserAdmin)
