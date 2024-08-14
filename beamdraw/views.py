from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def beam_data(request):
    # Example beam parameters
    length = 10  # Length of the beam in meters
    width = 0.3   # Width of the beam in meters
    number_of_bars = 5  # Number of iron bars
    bar_width = 0.1  # Width of each iron bar in meters
    spacing = (length - (number_of_bars * bar_width)) / (number_of_bars + 1)  # Space between bars

    # Generate positions for bars
    positions = [spacing * (i + 1) + bar_width * i for i in range(number_of_bars)]

    data = {
        'length': length,
        'width': width,
        'number_of_bars': number_of_bars,
        'bar_width': bar_width,
        'spacing': spacing,
        'positions': positions
    }

    return JsonResponse(data)

def index(request):
    return render(request, 'index.html')

