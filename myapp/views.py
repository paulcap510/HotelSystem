from django.shortcuts import render
from datetime import datetime
from .models import Room, Reservation
from django.db.models import Q, Count


def reservation_success(request, reservation_details):
    context = {
        'reservation_details': reservation_details,
    }
    return render(request, 'myapp/reservation_success.html', context)

def calculate_total_cost(room_price, nights):
    return room_price * nights


def make_reservation(request):
    if request.method == 'POST':
        check_in = request.GET.get('check-in')
        check_out = request.GET.get('check-out')
        room_type = request.GET.get('room_type')
        nights = int(request.GET.get('nights')) if request.GET.get('nights') else 0

        guest_name = request.POST.get('guest_name')
        credit_card_number = request.POST.get('credit_card_number')
        security_code = request.POST.get('security_code')
        name_on_card = request.POST.get('name_on_card')
        expiration_date = request.POST.get('expiration_date')

        room = Room.objects.filter(room_type=room_type).annotate(num_reservations=Count('reservation_set')).order_by('num_reservations').first()

        if room is not None:
            new_room_cost = room.price * nights
            total_cost = new_room_cost
        else:
            total_cost = 0

        reservation = Reservation.objects.create(
            guest_name=guest_name,
            check_in_date=check_in,
            check_out_date=check_out,
            room=room,
            credit_card_number=credit_card_number,
            security_code=security_code,
            name_on_card=name_on_card,
            expiration_date=expiration_date,
            total_cost=total_cost
        )

        reservation_details = {
            'check_in': check_in,
            'check_out': check_out,
            'room_type': room_type,
            'nights': nights,
            'total_cost': total_cost,
        }
        return reservation_success(request, reservation_details)


    check_in = request.GET.get('check-in')
    check_out = request.GET.get('check-out')
    room_type = request.GET.get('room_type')
    nights = int(request.GET.get('nights')) if request.GET.get('nights') else 0
    room = Room.objects.filter(room_type=room_type).first()

    if room is not None:
        new_room_cost = room.price * nights
        total_cost = new_room_cost
    else:
        total_cost = 0

    context = {
        'check_in': check_in,
        'check_out': check_out,
        'room_type': room_type,
        'nights': nights,
        'total_cost': total_cost,   
    }

    return render(request, 'myapp/make_reservation.html', context)


def search_results(request):
    check_in = request.POST.get('check_in_date')
    check_out = request.POST.get('check_out_date')

    check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
    check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()

    nights = (check_out_date - check_in_date).days
    room_type = request.POST.get('room_type')  

    available_rooms = Room.objects.exclude(
        reservation_set__check_in_date__lte=check_out_date,
        reservation_set__check_out_date__gte=check_in_date
    )

    available_room_types = available_rooms.values_list('room_type', flat=True).distinct()

    context = {
        'check_in': check_in,
        'check_out': check_out,
        'available_rooms': available_rooms,
        'available_room_types': available_room_types,
        'nights': nights,  
    }

    return render(request, 'myapp/search_results.html', context)

def search_results(request):
    check_in = request.POST.get('check_in_date')
    check_out = request.POST.get('check_out_date')

    check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
    check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()

    nights = (check_out_date - check_in_date).days
    room_type = request.POST.get('room_type')  

    available_rooms = Room.objects.filter(
        ~Q(reservation_set__check_in_date__lt=check_out_date, reservation_set__check_out_date__gt=check_in_date)
    )

    available_room_types = available_rooms.values_list('room_type', flat=True).distinct()

    context = {
        'check_in': check_in,
        'check_out': check_out,
        'available_rooms': available_rooms,
        'available_room_types': available_room_types,
        'nights': nights,  
    }

    return render(request, 'myapp/search_results.html', context)

def index(request):
    return render(request, 'myapp/index.html')