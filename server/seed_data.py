from datetime import date

from django.contrib.auth.models import User

from djangoapp.models import CarMake, CarModel, Dealer, Review


# Test user for cURL authentication
user, created = User.objects.get_or_create(
    username="testuser"
)

if created:
    user.set_password("testpass123")
    user.first_name = "Test"
    user.last_name = "User"
    user.email = "testuser@example.com"
    user.save()


# Car makes and models
cars = {
    "Toyota": [
        ("Camry", "SEDAN"),
        ("RAV4", "SUV"),
    ],
    "Honda": [
        ("Civic", "SEDAN"),
        ("CR-V", "SUV"),
    ],
    "Ford": [
        ("F-150", "TRUCK"),
        ("Mustang", "COUPE"),
    ],
    "Chevrolet": [
        ("Silverado", "TRUCK"),
        ("Malibu", "SEDAN"),
    ],
    "BMW": [
        ("3 Series", "SEDAN"),
        ("X5", "SUV"),
    ],
}


for make_name, models in cars.items():
    make, _ = CarMake.objects.get_or_create(
        name=make_name,
        defaults={
            "description": f"{make_name} automobile manufacturer"
        }
    )

    for model_name, car_type in models:
        CarModel.objects.get_or_create(
            car_make=make,
            name=model_name,
            type=car_type,
            year=2023,
        )


# Dealers
dealers = [
    {
        "name": "Best Motors Inc",
        "address": "123 Main Street",
        "city": "Boston",
        "state": "Massachusetts",
        "zip": "02101",
        "phone": "(617) 555-0100",
        "email": "info@bestmotors.com",
        "website": "https://www.bestmotors.com",
        "short_desc": "Your trusted car dealer in Boston",
        "full_desc": (
            "Best Motors Inc has been serving the Boston area "
            "with quality vehicles and excellent customer service."
        ),
    },
    {
        "name": "Elite Auto Sales",
        "address": "456 Oak Avenue",
        "city": "Kansas City",
        "state": "Kansas",
        "zip": "66101",
        "phone": "(913) 555-0200",
        "email": "sales@eliteauto.com",
        "website": "https://www.eliteauto.com",
        "short_desc": "Premium vehicles and exceptional service",
        "full_desc": (
            "Elite Auto Sales specializes in premium vehicles "
            "with a focus on customer satisfaction."
        ),
    },
    {
        "name": "Quality Cars",
        "address": "789 Pine Road",
        "city": "Wichita",
        "state": "Kansas",
        "zip": "67202",
        "phone": "(316) 555-0300",
        "email": "contact@qualitycars.com",
        "website": "https://www.qualitycars.com",
        "short_desc": "Quality vehicles at affordable prices",
        "full_desc": (
            "Quality Cars provides dependable vehicles at "
            "prices designed to fit different budgets."
        ),
    },
    {
        "name": "West Coast Motors",
        "address": "200 Market Street",
        "city": "Los Angeles",
        "state": "California",
        "zip": "90012",
        "phone": "(213) 555-0400",
        "email": "info@westcoastmotors.com",
        "website": "https://www.westcoastmotors.com",
        "short_desc": "A wide selection of quality vehicles",
        "full_desc": (
            "West Coast Motors offers a broad range of cars "
            "and a customer-focused buying experience."
        ),
    },
    {
        "name": "Midwest Auto Group",
        "address": "50 Michigan Avenue",
        "city": "Chicago",
        "state": "Illinois",
        "zip": "60601",
        "phone": "(312) 555-0500",
        "email": "sales@midwestauto.com",
        "website": "https://www.midwestauto.com",
        "short_desc": "Trusted vehicles and professional service",
        "full_desc": (
            "Midwest Auto Group helps customers find reliable "
            "vehicles backed by knowledgeable staff."
        ),
    },
]


for dealer_data in dealers:
    dealer, _ = Dealer.objects.get_or_create(
        name=dealer_data["name"],
        defaults=dealer_data,
    )


# Reviews for dealer 1
dealer = Dealer.objects.get(name="Best Motors Inc")

if not Review.objects.filter(dealer=dealer).exists():
    Review.objects.create(
        dealer=dealer,
        customer=user,
        purchase=True,
        purchase_date=date(2024, 1, 15),
        car_make="Toyota",
        car_model="Camry",
        car_year=2023,
        review_text="Fantastic services and great customer support!",
        sentiment="positive",
    )

print("Seed data loaded successfully.")
print("Login: testuser / testpass123")
print("Dealers:", Dealer.objects.count())
print("Car makes:", CarMake.objects.count())
print("Car models:", CarModel.objects.count())
print("Reviews:", Review.objects.count())
