from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from djangoapp import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("djangoapp/", include("djangoapp.urls")),

    # Compatibility authentication endpoints.
    path("api/login/", views.login_user),
    path("api/logout/", views.logout_user),
    path("api/register/", views.registration),

    # Original capstone-style dealer/review endpoints.
    path("fetchDealers", views.get_dealerships),
    path("fetchDealers/<str:state>", views.get_dealerships),
    path("fetchDealer/<int:dealer_id>", views.get_dealer_details),
    path("fetchReviews/dealer/<int:dealer_id>", views.get_dealer_reviews),

    # API aliases.
    path("api/dealers/", views.get_dealerships),
    path("api/dealers/<int:dealer_id>/", views.get_dealer_details),
    path("api/dealers/state/<str:state>/", views.get_dealerships),
    path(
        "api/reviews/dealer/<int:dealer_id>/",
        views.get_dealer_reviews,
    ),

    path("analyze/<path:review_text>", views.analyze_review),
    path("about", TemplateView.as_view(template_name="About.html")),
    path("contact", TemplateView.as_view(template_name="Contact.html")),

    path("", TemplateView.as_view(template_name="Home.html")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
