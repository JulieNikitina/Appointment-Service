import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from appointments.models import Appointment, User

from .forms import SignUp


def signup(request):
    if request.method == 'POST':
        form = SignUp(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    form = SignUp()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        id = json.loads(request.body).get('id')
        Appointment.objects.get(id=id).delete()

    username = request.user.username
    patient = get_object_or_404(User, username=username)
    appointments = Appointment.objects.filter(patient=patient)
    return render(request, 'profile.html', {'appointments': appointments})
