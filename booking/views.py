from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
import booking.models

def booking_page(request):
    if request.user.is_authenticated:
        bookings = booking.models.Booking.objects.filter(user=request.user)
        return render(request, "bookings.html", {"bookings": bookings})
    return HttpResponse("You need to login first")

def booking_cancel(request, user_id):
    if request.user.is_authenticated:
        booking_id = request.POST.get("booking_id")
        bookings = booking.models.Booking.objects.get(id=booking_id)
        if booking.user.id == request.user.id:
            booking.delete()
            return HttpResponseRedirect("/bookings/")
    return HttpResponse("You need to login first or you do not have permission to cancel this booking")

def booking_acception(request):
    if request.user.groups.filter(name='Trainer').exists():
        booking_id = request.POST.get("booking_id")
        bookings = booking.models.Booking.objects.get(id=booking_id)
        booking.accepted = True
        booking.save()
        return HttpResponseRedirect("/trainer/bookings/")
    return HttpResponseForbidden()
