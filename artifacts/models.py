# artifacts/models.py

from django.db import models
from datetime import date
from django.urls import reverse

class Artifact(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    origin = models.CharField(max_length=100)
    date_found = models.DateField(default=date.today)
    image = models.ImageField(upload_to='artifacts/', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('artifact_detail', args=[str(self.id)])
    
class Location(models.Model):
    LOCATION_CHOICES = [
        ('museum', 'Museum'),
        ('storage', 'Storage'),
        ('on_loan', 'On Loan'),
    ]
    name = models.CharField(max_length=100)
    location_type = models.CharField(max_length=20, choices=LOCATION_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.get_location_type_display()})"

class ArtifactInventory(models.Model):
    CONDITION_CHOICES = [
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]

    artifact = models.OneToOneField(Artifact, on_delete=models.CASCADE, related_name='inventory')
    location = models.CharField(max_length=100)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.artifact.name} in {self.location}"

class RestorationHistory(models.Model):
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE, related_name='restorations')
    restoration_date = models.DateField()
    description = models.TextField()
    restored_by = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Restoration on {self.restoration_date} for {self.artifact.name}"
