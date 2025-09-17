from django.db import models
from datetime import timedelta


def default_duration():
    return timedelta(minutes=30)


class Service(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=10000, blank=True, null=True)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, default=0.00, decimal_places=2)
    duration = models.DurationField(default=default_duration)


    def __str__(self):
        return self.name
    
    def formatted_duration(self):
        total_seconds = int(self.duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        if hours and minutes:
            return f"{hours} hour {minutes} min"
        elif hours:
            return f"{hours} hour"
        else:
            return f"{minutes} min"
