# app_name/models.py
from django.db import models



class Contact(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20, blank=True) 
    email = models.EmailField(blank=True)
    message = models.TextField()

   
    created_at = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact message"
        verbose_name_plural = "Contact messages"

    def __str__(self):
        base = self.name or "Anonymous"
        return f"{base} ({self.email or self.phone or 'no contact'})"
