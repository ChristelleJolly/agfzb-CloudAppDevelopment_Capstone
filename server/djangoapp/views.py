from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import get_object_or_404
from datetime import datetime
import logging
import json
from dotenv import load_dotenv
import os
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from .models import CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    load_dotenv()

    if request.method == "GET":
        url = os.getenv("API_DEALERSHIP_URL")
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        
        context={"dealership_list":dealerships}
        
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    load_dotenv()

    if request.method == "GET":
        url = os.getenv("API_REVIEW_URL")
        reviews = get_dealer_reviews_from_cf(url, dealerid=dealer_id)

        context = {"review_list":reviews, "dealer_id":dealer_id}
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    print("add_review")
    load_dotenv()

    if request.method == "GET":
        if request.user.is_authenticated:
            context = {}
            context["dealer_id"] = dealer_id
            cars = CarModel.objects.filter(dealer_id=dealer_id).all()
            context["cars"]=cars

            return render(request, 'djangoapp/add_review.html', context)
            
        else:
            raise Exception("User should be authenticated to submit a review")

    elif request.method == "POST":
        if request.user.is_authenticated:
            url = os.getenv("API_REVIEW_URL")

            car = get_object_or_404(CarModel, id=request.POST["car"])
            name = "Anonymous"
            if request.user.first_name or request.user.last_name:
                name = request.user.first_name + " " + request.user.last_name

            post_data = {
                "name": name,
                "dealership": dealer_id,
                "review": request.POST["content"],
                "purchase": "purchasecheck" in request.POST,
                "purchase_date": request.POST["purchasedate"],
                "car_make": car.car_make.name,
                "car_model": car.name,
                "car_year": car.year.strftime("%Y"),
            }
            review = post_request(url, post_data)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            raise Exception("User should be authenticated to submit a review")

