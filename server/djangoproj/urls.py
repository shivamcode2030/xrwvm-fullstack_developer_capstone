from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from djangoapp import views


urlpatterns = [
    path("admin/", admin.site.urls),

    path("djangoapp/", include("djangoapp.urls")),

    # Compatibility API endpoints
    path("api/login/", views.login_user),
    path("api/logout/", views.logout_user),
    path("api/register/", views.registration),

    path("api/dealers/", views.get_dealerships),
    path(
        "api/dealers/<int:dealer_id>/",
        views.get_dealer_details
    ),
    path(
        "api/dealers/state/<str:state>/",
        views.get_dealerships,
    ),

    path(
        "api/reviews/dealer/<int:dealer_id>/",
        views.get_dealer_reviews
    ),

    # Original capstone-style endpoints
    path(
        "fetchDealers",
        views.get_dealerships
    ),
    path(
        "fetchDealers/<str:state>",
        views.get_dealerships
    ),
    path(
        "fetchDealer/<int:dealer_id>",
        views.get_dealer_details
    ),

    # Sentiment endpoint
    path(
        "analyze/<path:review_text>",
        views.analyze_review
    ),

    path(
        "",
        TemplateView.as_view(
            template_name="Home.html"
        )
    ),
] + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)
