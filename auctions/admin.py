from django.contrib import admin
from .models import User, Category, Listing, Bid, Comment


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_active")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_active")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "edited_at")
    search_fields = ("name",)
    ordering = ("name",)


class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "price",
        "is_active",
        "category",
        "user",
        "created_at",
        "edited_at",
    )
    list_filter = ("is_active", "category")
    search_fields = ("title", "category__name")
    ordering = ("-created_at",)


class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "listing", "created_at", "edited_at")
    list_filter = ("listing", "user")
    search_fields = ("user__username", "listing__title")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "content", "listing", "created_at", "edited_at")
    list_filter = ("listing", "author")
    search_fields = ("content", "author__username")


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
