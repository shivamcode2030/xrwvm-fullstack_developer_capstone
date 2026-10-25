from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views


app_name = "djangoapp"

urlpatterns = [
    # Authentication
    path("login", views.login_user, name="login"),
    path("login/", views.login_user),

    path("logout", views.logout_user, name="logout"),
    path("logout/", views.logout_user),

    path("register", views.registration, name="register"),
    path("register/", views.registration),

    # Dealerships
    path(
        "get_dealers/",
        views.get_dealerships_django,
        name="get_dealers"
    ),
    path(
        "get_dealers/<str:state>",
        views.get_dealerships_django,
        name="get_dealers_by_state"
    ),

    path(
        "dealer/<int:dealer_id>",
        views.get_dealer_details_django,
        name="dealer_details"
    ),

    # Reviews
    path(
        "reviews/dealer/<int:dealer_id>",
        views.get_dealer_reviews_django,
        name="dealer_reviews"
    ),
    path(
        "add_review",
        views.add_review,
        name="add_review"
    ),

    # Cars
    path(
        "get_cars",
        views.get_cars,
        name="get_cars"
    ),

    # Sentiment
    path(
        "analyze_review/<path:review_text>",
        views.analyze_review,
        name="analyze_review"
    ),
    path(
        "analyze_review",
        views.analyze_review_post,
        name="analyze_review_post"
    ),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
