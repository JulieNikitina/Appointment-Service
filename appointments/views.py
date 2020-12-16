import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AppointmentForm
from .models import Appointment, User


@login_required
def index(request):
    username = request.user.username
    patient = get_object_or_404(User, username=username)
    appointments = Appointment.objects.filter(patient=patient)
    result = []
    for appointment in appointments:
        data = {
            'date': appointment.date.strftime('%d/%m/%Y'),
            'time': appointment.time.strftime('%H:%M:%S')
        }
        result.append(data)
    result = {'result': result}

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            patient.first_name = data['first_name']
            patient.last_name = data['last_name']
            patient.save()
            Appointment.objects.create(
                date=data['preferred_date'],
                time=data['available_time'],
                patient=patient,
                doctor=data['doctor'],
                message=data['message']
            )
            return redirect('profile')
    initial = {
        'first_name': patient.first_name,
        'last_name': patient.last_name
    }
    form = AppointmentForm(initial=initial)
    context = {
        'form': form,
        'date_time': json.dumps(result)
    }
    return render(request, 'index.html', context)


def schedule(request, doc_id):
    appointments = Appointment.objects.filter(doctor_id=doc_id)
    result = []
    for appointment in appointments:
        data = {
            'date': appointment.date.strftime('%d/%m/%Y'),
            'time': appointment.time.strftime('%H:%M:%S')
        }
        result.append(data)
    result = {'result': result}
    return JsonResponse(result)
