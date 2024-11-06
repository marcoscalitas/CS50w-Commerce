from django.urls import path

from . import views
    
app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
    # Auth
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup_view, name="signup"),
    # Listing
    path("add_listing", views.add_listing, name="add_listing"),
    path("listing/<int:id>", views.handle_listing_details, name="listing_details"),
    path("listing/edit/<int:id>", views.edit_listing, name="edit_listing"),
    path("listing/close/<int:id>", views.close_listing, name="close_listing"),
    # Category
    path("categories", views.get_categories, name="categories"),
    path("categories/<str:category>", views.get_listing_by_category, name="get_listing_by_category"),
    # Watchlist
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/add/<int:id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist/remove/<int:id>",views.remove_from_watchlist ,name="remove_from_watchlist"),
    # Bid
    path("bid/add/<int:id>", views.add_bid, name="add_bid"),
    # Comments
    path("comment/add/<int:id>", views.add_comment, name="add_comment"),
    path("comment/edit/<int:id>", views.edit_comment, name="edit_comment"),
    path("comment/delete/<int:id>", views.delete_comment, name="delete_comment"),
]
