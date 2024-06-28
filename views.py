from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm

def index(request):
    api_url = 'your_unique_api_url_here'  # Use your unique API endpoint
    error_message = ''
    notification = ''
    notification_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city_name = form.cleaned_data['name']
            city_exists = City.objects.filter(name=new_city_name).exists()

            if not city_exists:
                response = requests.get(api_url.format(new_city_name)).json()

                if response['cod'] == 200:  # Successful API response
                    form.save()
                    notification = 'City added successfully!'
                    notification_class = 'is-success'
                else:
                    error_message = 'City does not exist!'
            else:
                error_message = 'City already exists!'

            if error_message:
                notification = error_message
                notification_class = 'is-danger'

    form = CityForm()
    cities = City.objects.all()
    weather_details = []

    for city in cities:
        response = requests.get(api_url.format(city.name)).json()
        city_weather = {
            'city': city.name,
            'temperature': response['main']['temp'],
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
        }
        weather_details.append(city_weather)

    context = {
        'weather_data': weather_details,
        'form': form,
        'message': notification,
        'message_class': notification_class
    }

    return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')
