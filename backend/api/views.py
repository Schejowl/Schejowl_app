from rest_framework.decorators import api_view
from rest_framework.response import Response
from .optimization import TimeSlotOptimizer

user_data = []

@api_view(['POST'])
def submit_availability(request):
    name = request.data.get('name')
    availability = request.data.get('availability')
    user_data.append((name, availability))
    return Response({"status": "received"})

@api_view(['GET'])
def get_optimal_timeslot(request):
    if not user_data:
        return Response({"error": "No data submitted."})

    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    hours = [f"{i + 8}:00" for i in range(12)]
    time_keys = [f"{day}-{hour}" for hour in hours for day in days]

    matrix = []
    for _, availability in user_data:
        row = [float(availability.get(slot, 0.0)) for slot in time_keys]
        matrix.append(row)

    optimizer = TimeSlotOptimizer(matrix)
    result = optimizer.optimize()

    return Response(result)