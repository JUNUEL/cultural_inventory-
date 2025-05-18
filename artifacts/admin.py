from django.contrib import admin
from .models import Artifact, Location, ArtifactInventory, RestorationHistory

admin.site.register(Artifact)
admin.site.register(Location)
admin.site.register(ArtifactInventory)
admin.site.register(RestorationHistory)
