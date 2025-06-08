from django.db import models


class CarAction(models.Model):
    class Garage(models.TextChoices):
        VIP = 'A', 'Garagem VIP'
        CIMATEC = 'B', 'Garagem CIMATEC PARK'

    class ActionType(models.TextChoices):
        ENTRADA = 'entrada', 'Entrada'
        SAIDA = 'saida', 'Saída'

    garage = models.CharField(
        max_length=1,
        choices=Garage.choices,
        default=Garage.VIP,
        verbose_name='Garagem'
    )

    action = models.CharField(
        max_length=7,
        choices=ActionType.choices,
        verbose_name='Tipo de Ação'
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data e Hora'
    )

    class Meta:
        verbose_name = "Movimentação de Carro"
        verbose_name_plural = "Movimentações de Carros"
        ordering = ['-timestamp']  # mais recente primeiro

    def __str__(self):
        return f"{self.get_action_display()} - {self.get_garage_display()} - {self.timestamp.strftime('%d/%m/%Y %H:%M:%S')}"
