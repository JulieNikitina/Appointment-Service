from datetime import date, datetime, time

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()

TIME_CHOICES = [
    ('', 'Choose Time'),
    (time(9, 00), '09:00'),
    (time(10, 00), '10:00'),
    (time(11, 00), '11:00'),
    (time(12, 00), '12:00'),
    (time(13, 00), '13:00'),
    (time(14, 00), '14:00'),
    (time(15, 00), '15:00'),
    (time(16, 00), '16:00'),
    (time(17, 00), '17:00')
]


class Doctor(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True)
    speciality = models.CharField(max_length=150)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Appointment(models.Model):
    date = models.DateField(
        validators=[MinValueValidator(limit_value=date.today)]
    )
    time = models.TimeField(
        choices=TIME_CHOICES[1:],
        validators=[MinValueValidator(limit_value=datetime.now().time())]
    )
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    message = models.TextField(max_length=500, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('date', 'time'),
                name='unique appointment'
            )
        ]

    def clean(self):
        available_time = [i[0] for i in TIME_CHOICES]
        if isinstance(self.time, str):
            self.time = datetime.strptime(self.time, '%H:%M:%S').time()
        if self.time not in available_time:
            raise ValidationError('Unavailable time')
        if self.date == date.today() and self.time < datetime.now().time():
            raise ValidationError('Unavailable time')
        if self.date < date.today():
            raise ValidationError('Unavailable date')

    def save(self, *args, **kwargs):
        self.clean()
        super(Appointment, self).save(*args, **kwargs)
