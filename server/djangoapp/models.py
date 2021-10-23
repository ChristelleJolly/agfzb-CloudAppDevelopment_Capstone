from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    dealer_id = models.IntegerField()

    SEDAN = 'sedan'
    COUPE = 'coupe'
    SUV = 'suv'
    WAGON = 'wagon'
    OTHER_TYPE = 'other_type'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (COUPE, 'Coupe'),
        (SUV, 'SUV'),
        (WAGON, 'Station Wagon'),
        (OTHER_TYPE, 'Other')
    ]
    type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES
    )

    year = models.DateField()

    def __str__(self):
        return self.name


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer():

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip code
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview():

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, id, sentiment=None):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.id = id
        self.sentiment = sentiment
        
    def __str__(self):
        return "Review: " + self.review
