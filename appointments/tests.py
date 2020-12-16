from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from .forms import AppointmentForm
from .models import User, Doctor, Appointment
import datetime


class AppointmentTestCase(TestCase):
    def setUp(self):
        self.patient = User.objects.create_user(
            username='testuser',
            password='testpassword1234'
        )
        self.doctor1 = Doctor.objects.create(
            first_name='doctorname1',
            last_name='doctorlastname1',
            speciality='doctorspec1'
        )
        self.first_name = 'testname'
        self.last_name = 'testlastname'
        self.today = datetime.date.today()
        self.time = datetime.time(9, 00)

    def test_appointment_create(self):
        tomorrow = self.today + datetime.timedelta(days=1)
        appointment_count = Appointment.objects.count()
        Appointment.objects.create(
            date=tomorrow,
            time=self.time,
            patient=self.patient,
            doctor=self.doctor1
        )
        self.assertEqual(Appointment.objects.count(), appointment_count + 1)

    def test_appointment_form(self):
        new_appointment_data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'preferred_date': self.today,
            'available_time': self.time,
            'doctor': self.doctor1
        }
        form = AppointmentForm(data=new_appointment_data)
        self.assertTrue(form.is_valid())

    def test_appointment_create_with_wrong_time(self):
        with self.assertRaisesRegex(ValidationError, 'Unavailable time'):
            time = datetime.time(21, 00)
            Appointment.objects.create(
                date=self.today,
                time=time,
                patient=self.patient,
                doctor=self.doctor1
            )

    def test_appointment_create_with_past_date(self):
        with self.assertRaisesRegex(ValidationError, 'Unavailable date'):
            yesterday = self.today - datetime.timedelta(days=1)
            Appointment.objects.create(
                date=yesterday,
                time=self.time,
                patient=self.patient,
                doctor=self.doctor1
            )

    def test_appointment_create_with_same_time(self):
        with self.assertRaises(IntegrityError):
            tomorrow = self.today + datetime.timedelta(days=1)

            Appointment.objects.create(
                date=tomorrow,
                time=self.time,
                patient=self.patient,
                doctor=self.doctor1
            )

            Appointment.objects.create(
                date=tomorrow,
                time=self.time,
                patient=self.patient,
                doctor=self.doctor1
            )

    def test_appointment_create_with_reserved_time(self):
        with self.assertRaises(IntegrityError):
            tomorrow = self.today + datetime.timedelta(days=1)

            Appointment.objects.create(
                date=tomorrow,
                time=self.time,
                patient=self.patient,
                doctor=self.doctor1
            )

            patient2 = User.objects.create_user(
                username='testuser2',
                password='testpassword1234'
            )

            Appointment.objects.create(
                date=tomorrow,
                time=self.time,
                patient=patient2,
                doctor=self.doctor1
            )
