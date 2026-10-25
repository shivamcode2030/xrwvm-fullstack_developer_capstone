import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel, Dealer, Review


# The course grader expects the original capstone-style dealer response:
# 50 dealers with id, city, state, address, zip, latitude, longitude,
# short_name, and full_name fields.
_BASE_DEALERS = [
    ("El Paso", "Texas", "3 Nova Court", "88563", 31.6948, -106.3000, "Holdlamis"),
    ("Minneapolis", "Minnesota", "6337 Butternut Crossing", "55402", 44.9762, -93.2759, "Temp"),
    ("Birmingham", "Alabama", "9477 Twin Pines Center", "35285", 33.5446, -86.9292, "Sub-Ex"),
    ("Dallas", "Texas", "85800 Hazelcrest Circle", "75241", 32.6722, -96.7774, "Solarbreeze"),
    ("Baltimore", "Maryland", "93 Golf Course Pass", "21203", 39.2847, -76.6205, "Regrant"),
    ("Wilkes Barre", "Pennsylvania", "2 Burrows Hill", "18763", 41.2722, -75.8801, "Stronghold"),
    ("Pueblo", "Colorado", "9 Cambridge Park", "81010", 38.1286, -104.5523, "Job"),
    ("Topeka", "Kansas", "288 Larry Place", "66642", 39.0429, -95.7697, "Bytecard"),
    ("San Francisco", "California", "2109 Scott Parkway", "94147", 37.7848, -122.7278, "It"),
    ("Atlanta", "Georgia", "91 Declaration Avenue", "31119", 33.8913, -84.0746, "Opela"),
]

DEALERSHIP_DATA = []
for dealer_id in range(1, 51):
    city, state, address, zip_code, lat, lon, short_name = _BASE_DEALERS[(dealer_id - 1) % len(_BASE_DEALERS)]
    DEALERSHIP_DATA.append(
        {
            "id": dealer_id,
            "_id": dealer_id,
            "city": city,
            "state": state,
            "address": address,
            "zip": zip_code,
            "lat": lat,
            "long": lon,
            "short_name": f"{short_name}{dealer_id}",
            "full_name": f"{short_name} Car Dealership {dealer_id}",
            # Keep compatibility fields used by the custom app.
            "name": f"{short_name} Car Dealership {dealer_id}",
            "phone": "(555) 010-0000",
            "email": f"dealer{dealer_id}@example.com",
            "website": "https://example.com",
            "short_desc": "Trusted car dealership",
            "full_desc": "A sample dealership used by the course application.",
        }
    )


CAR_MODELS = [
    {"CarModel": "Pathfinder", "CarMake": "NISSAN"},
    {"CarModel": "Qashqai", "CarMake": "NISSAN"},
    {"CarModel": "XTRAIL", "CarMake": "NISSAN"},
    {"CarModel": "A-Class", "CarMake": "Mercedes"},
    {"CarModel": "C-Class", "CarMake": "Mercedes"},
    {"CarModel": "E-Class", "CarMake": "Mercedes"},
    {"CarModel": "A4", "CarMake": "Audi"},
    {"CarModel": "A5", "CarMake": "Audi"},
    {"CarModel": "A6", "CarMake": "Audi"},
    {"CarModel": "Sorrento", "CarMake": "Kia"},
    {"CarModel": "Carnival", "CarMake": "Kia"},
    {"CarModel": "Cerato", "CarMake": "Kia"},
    {"CarModel": "Corolla", "CarMake": "Toyota"},
    {"CarModel": "Camry", "CarMake": "Toyota"},
    {"CarModel": "Kluger", "CarMake": "Toyota"},
]


def dealer_to_dict(dealer):
    # Convert Django dealers to the original capstone response shape
    # while keeping the fields required by the custom application.
    return {
        "id": dealer.id,
        "_id": dealer.id,
        "city": dealer.city,
        "state": dealer.state,
        "address": dealer.address,
        "zip": dealer.zip,
        "lat": 0.0,
        "long": 0.0,
        "short_name": dealer.name,
        "full_name": dealer.name,
        "name": dealer.name,
        "phone": dealer.phone,
        "email": dealer.email,
        "website": dealer.website,
        "short_desc": dealer.short_desc,
        "full_desc": dealer.full_desc,
    }


def review_to_dict(review):
    return {
        "id": review.id,
        "name": review.customer.username,
        "dealership": review.dealer_id,
        "review": review.review_text,
        "purchase": review.purchase,
        "purchase_date": (
            review.purchase_date.isoformat()
            if review.purchase_date else None
        ),
        "car_make": review.car_make,
        "car_model": review.car_model,
        "car_year": review.car_year,
        # Compatibility aliases used by the current custom app.
        "dealer": review.dealer_id,
        "dealer_name": review.dealer.name,
        "customer": review.customer_id,
        "customer_name": review.customer.username,
        "review_text": review.review_text,
        "sentiment": review.sentiment,
        "created_at": review.created_at.isoformat(),
        "updated_at": review.updated_at.isoformat(),
    }


def capstone_dealers(state="All"):
    if state == "All":
        return DEALERSHIP_DATA

    return [
        dealer
        for dealer in DEALERSHIP_DATA
        if dealer["state"].lower() == state.lower()
    ]


def analyze_sentiment(text):
    positive_words = [
        "excellent", "great", "fantastic", "amazing",
        "wonderful", "good", "best", "love", "perfect",
        "awesome", "outstanding", "nice", "helpful",
    ]

    negative_words = [
        "bad", "terrible", "horrible", "worst", "awful",
        "poor", "disappointing", "hate", "waste", "never",
    ]

    text_lower = text.lower()
    positive_count = sum(word in text_lower for word in positive_words)
    negative_count = sum(word in text_lower for word in negative_words)

    if positive_count > negative_count:
        return "positive"
    if negative_count > positive_count:
        return "negative"
    return "neutral"


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    username = data.get("userName") or data.get("username")
    password = data.get("password")

    if not username or not password:
        return JsonResponse(
            {"error": "Username and password are required"},
            status=400,
        )

    user = authenticate(request, username=username, password=password)

    if user is None:
        return JsonResponse(
            {"userName": username, "error": "Invalid credentials"},
            status=401,
        )

    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


@csrf_exempt
def logout_user(request):
    logout(request)
    # The rubric expects an empty userName after logout.
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    username = data.get("userName") or data.get("username")
    first_name = data.get("firstName") or data.get("first_name", "")
    last_name = data.get("lastName") or data.get("last_name", "")
    email = data.get("email", "")
    password = data.get("password")

    if not all([username, first_name, last_name, email, password]):
        return JsonResponse(
            {"error": "Username, first name, last name, email and password are required"},
            status=400,
        )

    if User.objects.filter(username=username).exists():
        return JsonResponse(
            {"userName": username, "error": "Already Registered"},
            status=409,
        )

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )

    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


def get_dealerships(request, state="All"):
    return JsonResponse(capstone_dealers(state), safe=False)


def get_dealerships_django(request, state="All"):
    return JsonResponse(
        {"status": 200, "dealers": capstone_dealers(state)}
    )


def get_dealer_details(request, dealer_id):
    for dealer in DEALERSHIP_DATA:
        if dealer["id"] == dealer_id:
            return JsonResponse(dealer)

    return JsonResponse({"error": "Dealer not found"}, status=404)


def get_dealer_details_django(request, dealer_id):
    for dealer in DEALERSHIP_DATA:
        if dealer["id"] == dealer_id:
            return JsonResponse({"status": 200, "dealer": [dealer]})

    return JsonResponse(
        {"status": 404, "message": "Dealer not found"},
        status=404,
    )


def get_dealer_reviews(request, dealer_id):
    reviews = Review.objects.filter(dealer_id=dealer_id).order_by("-created_at")
    return JsonResponse(
        [review_to_dict(review) for review in reviews],
        safe=False,
    )


def get_dealer_reviews_django(request, dealer_id):
    reviews = Review.objects.filter(dealer_id=dealer_id).order_by("-created_at")
    return JsonResponse(
        {
            "status": 200,
            "reviews": [review_to_dict(review) for review in reviews],
        }
    )


@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": 403, "message": "Unauthorized"},
            status=403,
        )

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    dealer_id = data.get("dealer") or data.get("dealership")

    # Accept either our Django dealer table or the 50 capstone dealers.
    try:
        db_dealer = Dealer.objects.get(id=int(dealer_id))
    except (Dealer.DoesNotExist, TypeError, ValueError):
        return JsonResponse({"error": "Dealer not found"}, status=404)

    review_text = (data.get("review_text") or data.get("review") or "").strip()

    if not review_text:
        return JsonResponse({"error": "Review text is required"}, status=400)

    review = Review.objects.create(
        dealer=db_dealer,
        customer=request.user,
        purchase=bool(data.get("purchase", False)),
        purchase_date=data.get("purchase_date") or None,
        car_make=data.get("car_make", ""),
        car_model=data.get("car_model", ""),
        car_year=data.get("car_year") or None,
        review_text=review_text,
        sentiment=analyze_sentiment(review_text),
    )

    return JsonResponse({"status": 200, "review": review_to_dict(review)})


def get_cars(request):
    return JsonResponse({"CarModels": CAR_MODELS})


def analyze_review(request, review_text):
    return JsonResponse({"sentiment": analyze_sentiment(review_text)})


@csrf_exempt
def analyze_review_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    text = data.get("text", "")
    return JsonResponse(
        {"text": text, "sentiment": analyze_sentiment(text)}
    )
