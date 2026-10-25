from django.contrib import admin
from .models import CarMake, CarModel, Dealer, Review


class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    inlines = [CarModelInline]


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("name", "car_make", "type", "year")
    list_filter = ("car_make", "type", "year")
    search_fields = ("name", "car_make__name")


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "state", "phone", "email")
    list_filter = ("state", "city")
    search_fields = ("name", "city", "state")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("customer", "dealer", "sentiment", "created_at")
    list_filter = ("sentiment", "purchase")
    search_fields = ("customer__username", "dealer__name", "review_text")
