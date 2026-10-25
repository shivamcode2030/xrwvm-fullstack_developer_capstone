from datetime import datetime
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel, Dealer, Review


def dealer_to_dict(dealer):
    return {
        "id": dealer.id,
        "_id": dealer.id,
        "name": dealer.name,
        "address": dealer.address,
        "city": dealer.city,
        "state": dealer.state,
        "zip": dealer.zip,
        "phone": dealer.phone,
        "email": dealer.email,
        "website": dealer.website,
        "short_desc": dealer.short_desc,
        "full_desc": dealer.full_desc,
    }


def review_to_dict(review):
    return {
        "id": review.id,
        "dealer": review.dealer_id,
        "dealer_name": review.dealer.name,
        "customer": review.customer_id,
        "customer_name": review.customer.username,
        "purchase": review.purchase,
        "purchase_date": (
            review.purchase_date.isoformat()
            if review.purchase_date else None
        ),
        "car_make": review.car_make,
        "car_model": review.car_model,
        "car_year": review.car_year,
        "review_text": review.review_text,
        "sentiment": review.sentiment,
        "created_at": review.created_at.isoformat(),
        "updated_at": review.updated_at.isoformat(),
    }


def analyze_sentiment(text):
    positive_words = [
        "excellent", "great", "fantastic", "amazing",
        "wonderful", "good", "best", "love", "perfect",
        "awesome", "outstanding", "nice", "helpful"
    ]

    negative_words = [
        "bad", "terrible", "horrible", "worst", "awful",
        "poor", "disappointing", "hate", "waste", "never"
    ]

    text_lower = text.lower()

    positive_count = sum(
        word in text_lower for word in positive_words
    )
    negative_count = sum(
        word in text_lower for word in negative_words
    )

    if positive_count > negative_count:
        return "positive"

    if negative_count > positive_count:
        return "negative"

    return "neutral"


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST request required"},
            status=405
        )

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    username = data.get("userName") or data.get("username")
    password = data.get("password")

    if not username or not password:
        return JsonResponse(
            {"error": "Username and password are required"},
            status=400
        )

    user = authenticate(
        request,
        username=username,
        password=password
    )

    if user is None:
        return JsonResponse(
            {
                "userName": username,
                "error": "Invalid credentials"
            },
            status=401
        )

    login(request, user)

    return JsonResponse({
        "userName": username,
        "status": "Authenticated",
    })


@csrf_exempt
def logout_user(request):
    username = request.user.username if request.user.is_authenticated else ""

    logout(request)

    return JsonResponse({
        "userName": username
    })


@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST request required"},
            status=405
        )

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    username = data.get("userName") or data.get("username")
    first_name = data.get("firstName") or data.get("first_name", "")
    last_name = data.get("lastName") or data.get("last_name", "")
    email = data.get("email", "")
    password = data.get("password")

    if not all([username, first_name, last_name, email, password]):
        return JsonResponse(
            {
                "error": (
                    "Username, first name, last name, "
                    "email and password are required"
                )
            },
            status=400
        )

    if User.objects.filter(username=username).exists():
        return JsonResponse({
            "userName": username,
            "error": "Already Registered"
        }, status=409)

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )

    login(request, user)

    return JsonResponse({
        "userName": username,
        "status": "Authenticated",
    })


def get_dealerships(request, state="All"):
    if state == "All":
        dealers = Dealer.objects.all()
    else:
        dealers = Dealer.objects.filter(
            state__iexact=state
        )

    return JsonResponse([
        dealer_to_dict(dealer)
        for dealer in dealers
    ], safe=False)


def get_dealerships_django(request, state="All"):
    if state == "All":
        dealers = Dealer.objects.all()
    else:
        dealers = Dealer.objects.filter(
            state__iexact=state
        )

    return JsonResponse({
        "status": 200,
        "dealers": [
            dealer_to_dict(dealer)
            for dealer in dealers
        ]
    })


def get_dealer_details(request, dealer_id):
    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse(
            {"error": "Dealer not found"},
            status=404
        )

    return JsonResponse(dealer_to_dict(dealer))


def get_dealer_details_django(request, dealer_id):
    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse(
            {"status": 404, "message": "Dealer not found"},
            status=404
        )

    return JsonResponse({
        "status": 200,
        "dealer": dealer_to_dict(dealer)
    })


def get_dealer_reviews(request, dealer_id):
    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse(
            {"error": "Dealer not found"},
            status=404
        )

    reviews = Review.objects.filter(
        dealer=dealer
    ).order_by("-created_at")

    return JsonResponse([
        review_to_dict(review)
        for review in reviews
    ], safe=False)


def get_dealer_reviews_django(request, dealer_id):
    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse(
            {"status": 404, "message": "Dealer not found"},
            status=404
        )

    reviews = Review.objects.filter(
        dealer=dealer
    ).order_by("-created_at")

    return JsonResponse({
        "status": 200,
        "reviews": [
            review_to_dict(review)
            for review in reviews
        ]
    })


@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST request required"},
            status=405
        )

    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": 403, "message": "Unauthorized"},
            status=403
        )

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    dealer_id = data.get("dealer")

    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse(
            {"error": "Dealer not found"},
            status=404
        )

    review_text = data.get("review_text", "").strip()

    if not review_text:
        return JsonResponse(
            {"error": "Review text is required"},
            status=400
        )

    purchase_date = data.get("purchase_date") or None

    review = Review.objects.create(
        dealer=dealer,
        customer=request.user,
        purchase=bool(data.get("purchase", False)),
        purchase_date=purchase_date,
        car_make=data.get("car_make", ""),
        car_model=data.get("car_model", ""),
        car_year=data.get("car_year") or None,
        review_text=review_text,
        sentiment=analyze_sentiment(review_text),
    )

    return JsonResponse({
        "status": 200,
        "review": review_to_dict(review)
    })


def get_cars(request):
    car_models = CarModel.objects.select_related("car_make")

    cars = [
        {
            "CarMake": car_model.car_make.name,
            "CarModel": car_model.name
        }
        for car_model in car_models
    ]

    return JsonResponse(cars, safe=False)


def analyze_review(request, review_text):
    return JsonResponse({
        "sentiment": analyze_sentiment(review_text)
    })


@csrf_exempt
def analyze_review_post(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST request required"},
            status=405
        )

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    text = data.get("text", "")

    return JsonResponse({
        "text": text,
        "sentiment": analyze_sentiment(text)
    })
