from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django import forms
from .models import Listing, Bid, Comment, Category, Watchlist
from .models import User


class CreateListingForm(forms.Form):
    item_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Item Name', max_length=64)
    item_description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'style': "width:100%;", 'class':'form-control'}),
                                       max_length=128)
    price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}),label='Price')
    category = forms.ModelChoiceField(queryset=Category.objects.order_by('category_title').all(), to_field_name='category_title')
    img_url = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}), label='Image URL:',required=False)


class CreateCommentForm(forms.Form):
    title = forms.CharField(label="Title", max_length=64)
    name = forms.CharField(label="Name", max_length=32)
    comment = forms.CharField(widget=forms.Textarea(attrs={'style': "width:100%;"}), label="Comment", max_length=1024)


class CreateBidForm(forms.Form):
    bid_price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label=False)


def index(request):

    listings = Listing.objects.filter(is_open=True)
    # watchlist_count = Watchlist.objects.filter(request.user.id).count()
    return render(request, "auctions/index.html", {
        "listings": listings,
    })


def closed(request):

    listings = Listing.objects.filter(is_open=False)
    # watchlist_count = Watchlist.objects.filter(request.user.id).count()
    return render(request, "auctions/closed.html", {
        "listings": listings,
    })


def categories(request):
    category = Category.objects.order_by('category_title')

    return render(request, "auctions/categories.html", {
        "categories": category
    })


def category_get(request, category_param):
    c = Category.objects.get(category_title=category_param)
    listing = Listing.objects.order_by('item_title').filter(category__category_title__contains=category_param)
    return render(request, "auctions/categories.html", {
        "category": c,
        "listings": listing
    })

@login_required(login_url="/login")
def watchlist(request):
    user = User.objects.get(username=request.user)
    wl = user.watchlist.all()
    print(wl)
    return render(request, "auctions/watchlist.html", {
        "watchlist": wl
    })


@login_required(login_url="/login")
def mylistings(request):
    user = User.objects.get(username=request.user)
    listings = user.listing.all()
    print(listings)
    return render(request, "auctions/mylistings.html", {
        "listings": listings
    })


@login_required(login_url="/login")
def comment(request, item_id):
    current_item = Listing.objects.get(id=item_id)
    if request.method == "POST":
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            name = form.cleaned_data['name']
            _comment = form.cleaned_data['comment']
            new_comment = Comment(listing=current_item, title=title, name=name, comment=_comment)
            new_comment.save()
            return HttpResponseRedirect(reverse(item, kwargs={"item_id": item_id}))
        else:
            return render(request, "auctions/item.html", {
                "comment": form
            })
    return HttpResponseRedirect(reverse("index"))


def item(request, item_id):
    current_item = Listing.objects.get(id=item_id)
    current_bid = Bid.objects.filter(listing=item_id).last()
    comments = Comment.objects.filter(listing=item_id)

    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        if 'Close' in request.POST:
            current_item.is_open = False
            try:
                win_user = User.objects.get(username=current_bid.user_id)
                current_item.winner = win_user
            except AttributeError:
                print("Ok")
                current_item.winner = current_item.owner
                print(current_item.is_open)
            current_item.save()
            return HttpResponseRedirect(reverse(item, kwargs={"item_id": item_id}))
        if 'Delete' in request.POST:
            user.watchlist.filter(listing=current_item).delete()
            return HttpResponseRedirect(reverse('watchlist'))
        if 'DeleteListing' in request.POST:
            user.listing.filter(id=item_id).delete()
            return HttpResponseRedirect(reverse('mylistings'))
        if 'Watchlist' in request.POST:
            if not user.watchlist.filter(listing=current_item):
                wl = Watchlist(user=user, listing=current_item)
                wl.save()
            else:
                user.watchlist.filter(listing=current_item).delete()
            return HttpResponseRedirect(reverse(item, kwargs={"item_id": item_id}))
        form = CreateBidForm(request.POST)
        if form.is_valid():
            bid_price = form.cleaned_data['bid_price']
            if (bid_price <= current_bid.user_bid) or (bid_price == current_item.price) and not (user == current_item.owner):
                return render(request, "auctions/item.html", {
                    "item": current_item,
                    "success": 0,
                    "form": form,
                    "is_open": current_item.is_open,
                    "bid": current_bid,
                    "comments": comments
                })
            elif user == current_item.owner:

                return render(request, "auctions/item.html", {
                    "item": current_item,
                    "success": 2,
                    "form": form,
                    "is_open": current_item.is_open,
                    "bid": current_bid,
                    "comments": comments
                })
            elif current_item.is_open:
                new_bid = Bid(listing=current_item, user_bid=bid_price, user_id=request.user.username)
                new_bid.save()
                return HttpResponseRedirect(reverse('item', kwargs={"item_id": item_id}))
                # return render(request, "auctions/item.html", {
                #     "item": current_item,
                #     "success": 1,
                #     "form": form,
                #     "is_open": current_item.is_open,
                #     "bid": current_bid,
                #     "comments": comments
                # })
        else:
            return render(request, "auctions/item.html", {
                "form": form
            })
    else:
        form = CreateBidForm()
        comment_form = CreateCommentForm()
        return render(request, "auctions/item.html", {
            "item": current_item,
            "form": form,
            "is_open": current_item.is_open,
            "comment": comment_form,
            "bid": current_bid,
            "comments": comments
        })


@login_required(login_url="/login")
def create(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        form = CreateListingForm(request.POST)
        if form.is_valid():
            item_title = form.cleaned_data['item_title']
            item_description = form.cleaned_data['item_description']
            price = form.cleaned_data['price']
            category = form.cleaned_data['category']
            img_url = form.cleaned_data['img_url']
            new_item = Listing(owner=user, item_title=item_title, item_description=item_description, price=price, category=category, img_url=img_url)
            new_item.save()
            start_bid = Bid(listing=new_item, user_id=request.user.username)
            start_bid.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })
    else:
        form = CreateListingForm()
    return render(request, "auctions/create.html", {
        "form": form
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
