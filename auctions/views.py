from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm, ListingForm, CommentForm, BidForm
from .models import User, Category, Listing, Bid, Comment
from django.shortcuts import get_object_or_404
from decimal import Decimal, InvalidOperation
from django.db import IntegrityError
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Max
from django.http import Http404
from decimal import Decimal
from . import util


TEMPLATE_INDEX = "index"
TEMPLATE_CLOSED_LISTINGS = "closed_listings"
TEMPLATE_LOGIN = "login"
TEMPLATE_SIGNUP = "signup"
TEMPLATE_ADD_LISTING = "add_listing"
TEMPLATE_EDIT_LISTING = "edit_listing"
TEMPLATE_LISTING_DETAILS = "listing_details"
TEMPLATE_CATEGORIES = "categories"
TEMPLATE_LISTING_BY_CATEGORY = "listing_by_category"
TEMPLATE_WATCHLIST = "watchlist"
TEMPLATE_ERROR_404 = "404"


def handle_listing_display_by_status(request, is_active):
    listings = Listing.objects.filter(is_active=is_active)
    total_listing = listings.count()

    for listing in listings:
        listing.is_new = util.is_new_listing(listing)

    page, total_listing_per_page = util.paginate_queryset(
        request, listings, per_page=12
    )
    has_more_than_twelve_listings = total_listing > total_listing_per_page

    context = {
        "page": page,
        "has_more_than_twelve_listings": has_more_than_twelve_listings,
    }

    template_name = TEMPLATE_INDEX if is_active else TEMPLATE_CLOSED_LISTINGS
    return util.render_template(request, template_name, context)


@require_http_methods(["GET"])
def index(request):
    return handle_listing_display_by_status(request, is_active=True)


@require_http_methods(["GET"])
def closed_listings(request):
    return handle_listing_display_by_status(request, is_active=False)


@require_http_methods(["GET", "POST"])
def login_view(request):
    context = {"hide_components": True}
    current_user = util.get_current_user(request)

    if current_user.is_authenticated:
        return util.redirect_to(TEMPLATE_INDEX)

    if request.method != "POST":
        context["form"] = LoginForm()
        return util.render_template(request, TEMPLATE_LOGIN, context)

    form = LoginForm(request.POST)
    context["form"] = form

    if not form.is_valid():
        return util.render_template(request, TEMPLATE_LOGIN, context)

    data = form.cleaned_data
    user = authenticate(request, username=data["username"], password=data["password"])

    if user is None:
        form.add_error(None, "Invalid username and/or password.")
        return util.render_template(request, TEMPLATE_LOGIN, context)

    login(request, user)
    messages.success(request, f"Welcome back {data["username"]}")
    return util.redirect_to(TEMPLATE_INDEX)


@require_http_methods(["GET"])
def logout_view(request):
    logout(request)
    return util.redirect_to(TEMPLATE_INDEX)


@require_http_methods(["GET", "POST"])
def signup_view(request):
    context = {"hide_components": True}

    if request.method != "POST":
        context["form"] = RegisterForm()
        return util.render_template(request, TEMPLATE_SIGNUP, context)

    form = RegisterForm(request.POST)
    context["form"] = form

    if not form.is_valid():
        return util.render_template(request, TEMPLATE_SIGNUP, context)

    try:
        data = form.cleaned_data
        new_user = User.objects.create_user(
            data["username"], data["email"], data["password"]
        )

        new_user.save()
        login(request, new_user)
        message = f"Registration successful! Welcome! {data["username"]}"
        messages.success(request, message)
        return util.redirect_to(TEMPLATE_INDEX)

    except IntegrityError:
        form.add_error(None, "Username already taken.")
        return util.render_template(request, TEMPLATE_SIGNUP, context)

    except Exception as e:
        form.add_error(None, f"An error occurred: {str(e)}")
        return util.render_template(request, TEMPLATE_SIGNUP, context)


@require_http_methods(["GET", "POST"])
@login_required
def add_listing(request):
    categories = Category.objects.all()
    context = {"categories": categories}

    if request.method != "POST":
        context["form"] = ListingForm()
        return util.render_template(request, TEMPLATE_ADD_LISTING, context)

    form = ListingForm(request.POST)
    context["form"] = form

    if not form.is_valid():
        return util.render_template(request, TEMPLATE_ADD_LISTING, context)

    data = form.cleaned_data
    current_user = util.get_current_user(request)
    category = get_object_or_404(Category, name=data["category"])

    try:
        new_listing = Listing(
            title=data["title"],
            description=data["description"],
            price=data["price"],
            image_url=data["image_url"],
            category=category,
            user=current_user,
        )
        
        new_listing.save()
        messages.success(request, "New listing created successfully")
        return util.redirect_to(TEMPLATE_INDEX)

    except IntegrityError:
        form.add_error(None, "An error occurred while saving the listing")
        return util.render_template(request, TEMPLATE_ADD_LISTING, context)


def get_highest_bid_amount(listing):
    return listing.bids.aggregate(Max("amount"))["amount__max"] or 0


def is_in_watchlist(user, listing):
    return user in listing.watchlist.all()


def get_all_paginated_comments(request, listing, per_page=4):
    comments = Comment.objects.filter(listing=listing)
    return [comments.count(), util.paginate_queryset(request, comments, per_page)]


def get_auction_winner(listing):
    listing = get_object_or_404(Listing, id=listing.id)
    highest_bid = listing.bids.order_by("-amount").first()

    if not highest_bid:
        return None

    return highest_bid.user


@require_http_methods(["GET"])
def handle_listing_details(request, id):
    current_user = util.get_current_user(request)
    listing = get_object_or_404(Listing, pk=id)

    total_comments, (page, total_comments_per_page) = get_all_paginated_comments(
        request, listing
    )
    has_more_than_four_comments = total_comments > total_comments_per_page

    context = {
        "listing": listing,
        "highest_bid_amount": get_highest_bid_amount(listing),
        "is_listing_in_watchlist": is_in_watchlist(current_user, listing),
        "is_listing_owner": util.is_owner(request, listing, "user"),
        "current_user": current_user,
        "auction_winner": get_auction_winner(listing),
        "page": page,
        "has_more_than_four_comments": has_more_than_four_comments,
        "bid_form": BidForm(),
        "comment_form": CommentForm(),
    }

    return util.render_template(request, TEMPLATE_LISTING_DETAILS, context)


@require_http_methods(["GET", "POST"])
@login_required
def edit_listing(request, id):
    listing = get_object_or_404(Listing, pk=id)
    context = {"listing": listing}

    if request.method != "POST":
        context["form"] = ListingForm(instance=listing)
        return util.render_template(request, TEMPLATE_EDIT_LISTING, context)

    form = ListingForm(request.POST, instance=listing)
    context["form"] = form

    if not form.is_valid():
        return util.render_template(request, TEMPLATE_EDIT_LISTING, context)

    form.save()
    messages.success(request, "Listing edited successfully")
    return util.redirect_to(TEMPLATE_LISTING_DETAILS, id)


@require_http_methods(["GET", "POST"])
@login_required
def close_listing(request, id):
    listing = get_object_or_404(Listing, pk=id)
    listing.is_active = False
    listing.save()

    return util.redirect_to(TEMPLATE_LISTING_DETAILS, id)


@require_http_methods(["GET"])
def get_categories(request):
    categories = Category.objects.all()
    total_categories = categories.count()

    page, total_categories_per_page = util.paginate_queryset(
        request, categories, per_page=9
    )
    has_more_than_nine_categories = total_categories > total_categories_per_page

    context = {
        "page": page,
        "has_more_than_nine_categories": has_more_than_nine_categories,
    }

    return util.render_template(request, TEMPLATE_CATEGORIES, context)


@require_http_methods(["GET"])
def get_listing_by_category(request, category):
    category = get_object_or_404(Category, name=category)
    listings = Listing.objects.filter(category=category)
    total_listings = listings.count()

    page, total_listings_per_page = util.paginate_queryset(request, listings, 12)
    has_more_than_twelve_listings = total_listings > total_listings_per_page

    context = {
        "page": page,
        "category": category,
        "has_more_than_twelve_listings": has_more_than_twelve_listings,
    }

    return util.render_template(request, TEMPLATE_LISTING_BY_CATEGORY, context)


def get_random_active_listings(count=4):
    active_listings = Listing.objects.filter(is_active=True).order_by("?")[:count]

    for active_listing in active_listings:
        active_listing.is_new = util.is_new_listing(active_listing)

    return active_listings


@require_http_methods(["GET"])
@login_required
def watchlist(request):
    current_user = util.get_current_user(request)
    listings = current_user.watchlist_listings.all()
    total_listings = listings.count()

    for listing in listings:
        listing.auction_winner = get_auction_winner(listing)
        listing.highest_bid_amount = get_highest_bid_amount(listing)

    recommended_listings = get_random_active_listings(count=4)
    is_watchlist_empty = not listings

    page, total_listings_per_page = util.paginate_queryset(
        request, listings, per_page=4
    )
    has_more_than_four_listings = total_listings > total_listings_per_page

    context = {
        "page": page,
        "is_watchlist_empty": is_watchlist_empty,
        "has_more_than_four_listings": has_more_than_four_listings,
        "recommended_listings": recommended_listings,
    }

    return util.render_template(request, TEMPLATE_WATCHLIST, context)


def toggle_watchlist(request, id, type):
    current_user = util.get_current_user(request)
    listing = get_object_or_404(Listing, pk=id)

    actions = {
        "add": lambda: listing.watchlist.add(current_user),
        "remove": lambda: listing.watchlist.remove(current_user),
    }

    if type not in actions:
        messages.error(request, "INVALID TYPE")
        return util.redirect_to(TEMPLATE_LISTING_DETAILS, id)

    actions[type]()

    if type == "remove":
        messages.success(request, "Listing removed from watchlist")
        url = request.META.get("HTTP_REFERER")
        if "watchlist" in url:
            return util.redirect_to(TEMPLATE_WATCHLIST)
        return util.redirect_to(TEMPLATE_LISTING_DETAILS, id)

    messages.success(request, "Listing added to watchlist")
    return util.redirect_to(TEMPLATE_LISTING_DETAILS, id)


@require_http_methods(["POST"])
@login_required
def add_to_watchlist(request, id):
    return toggle_watchlist(request, id, "add")


@require_http_methods(["POST"])
@login_required
def remove_from_watchlist(request, id):
    return toggle_watchlist(request, id, "remove")


def is_higher_than_last_amount(new_amount, last_amount):
    try:
        return Decimal(new_amount) > Decimal(last_amount)
    except (InvalidOperation, TypeError):
        return False


@require_http_methods(["POST"])
@login_required
def add_bid(request, id):
    current_user = util.get_current_user(request)
    amount = float(request.POST.get("amount"))
    listing = get_object_or_404(Listing, pk=id)
    listing_price = listing.price
    last_bid = get_highest_bid_amount(listing)
    error_message = "The bid must be greater than $"

    if not is_higher_than_last_amount(amount, last_bid):
        messages.warning(request, f"{error_message}{last_bid}")
        return util.redirect_to(TEMPLATE_LISTING_DETAILS, id)

    if not is_higher_than_last_amount(amount, listing_price):
        messages.warning(request, f"{error_message}{listing_price}")
        return util.redirect_to(TEMPLATE_LISTING_DETAILS, id)

    new_bid = Bid(user=current_user, amount=amount, listing=listing)
    new_bid.save()

    messages.success(request, "Bid added successfully")
    return util.redirect_to(TEMPLATE_LISTING_DETAILS, id)


@require_http_methods(["POST"])
@login_required
def add_comment(request, id):
    current_user = util.get_current_user(request)
    content = request.POST.get("content")
    listing = get_object_or_404(Listing, pk=id)

    new_comment = Comment.objects.create(
        author=current_user, content=content, listing=listing
    )

    new_comment.save()
    messages.success(request, "New comment created successfully")
    return util.redirect_to(TEMPLATE_LISTING_DETAILS, id)


def get_comment_by_id(id):
    comment = get_object_or_404(Comment, pk=id)
    listing_id = comment.listing.id

    return [comment, listing_id]


@require_http_methods(["POST"])
@login_required
def edit_comment(request, id):
    comment, listing_id = get_comment_by_id(id)
    new_content = request.POST.get("content")

    if not util.is_owner(request, comment, "author"):
        messages.warning(request, "You are not the owner of this comment")
        return util.redirect_to(TEMPLATE_LISTING_DETAILS, listing_id)

    if util.is_empty(new_content):
        messages.warning(request, "The comment cannot be empty.")
        return util.redirect_to(TEMPLATE_LISTING_DETAILS, listing_id)

    comment.content = new_content
    comment.save()
    messages.success(request, "Comment edited successfully.")
    return util.redirect_to(TEMPLATE_LISTING_DETAILS, listing_id)


@require_http_methods(["POST"])
@login_required
def delete_comment(request, id):
    comment, listing_id = get_comment_by_id(id)

    if not util.is_owner(request, comment, "author"):
        messages.warning(request, "You are not the owner of this comment")
        return util.redirect_to(TEMPLATE_LISTING_DETAILS, listing_id)

    comment.delete()
    messages.success(request, "Comment successfully deleted.")
    return util.redirect_to(TEMPLATE_LISTING_DETAILS, listing_id)


@require_http_methods(["GET"])
def costum_404(request, exception):
    return util.render_template(request, TEMPLATE_ERROR_404)
