from django.db import models

class CarAction(models.Model):
    GARAGE_CHOICES = [
        ('A', 'Garagem VIP'),
        ('B', 'Garagem CIMATEC PARK'),
    ]

    ACTION_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]

    garage = models.CharField(max_length=1, choices=GARAGE_CHOICES, default='A')
    action = models.CharField(max_length=7, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.garage} - {self.timestamp}"