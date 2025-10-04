from django.shortcuts import render
import requests
import datetime
from decouple import config  

def index(request):
    api_key = config('API_KEY')  
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'

    if request.method == 'POST':
        city = request.POST['city1']
        weather_data, daily_forecasts = fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url)
        context = {
            'weather_data1': weather_data,
            'daily_forecasts1': daily_forecasts,
        }
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')



def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }

    daily_forecasts = []
    try:
        daily_list = forecast_response['daily'][:5]
    except KeyError:
        with open('d:/Rubin/Django/weather_project/weather_app/error.log', 'a') as f:
            f.write(f"KeyError: 'daily' not found in forecast_response for city: {city}\nResponse: {forecast_response}\n")
        daily_list = []

    for daily_data in daily_list:
        daily_forecasts.append({
            'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
            'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
            'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
            'description': daily_data['weather'][0]['description'],
            'icon': daily_data['weather'][0]['icon'],
        })

    return weather_data, daily_forecasts