# artifacts/forms.py

from django import forms
from .models import Artifact
from .models import ArtifactInventory, RestorationHistory

class ArtifactForm(forms.ModelForm):
    class Meta:
        model = Artifact
        fields = ['name', 'description', 'origin', 'date_found', 'image']

class InventoryUpdateForm(forms.ModelForm):
    class Meta:
        model = ArtifactInventory
        fields = ['location', 'condition']

class RestorationHistoryForm(forms.ModelForm):
    class Meta:
        model = RestorationHistory
        fields = ['restoration_date', 'description', 'restored_by']

class ArtifactInventoryForm(forms.ModelForm):
    class Meta:
        model = ArtifactInventory
        fields = ['condition', 'location']

    def __init__(self, *args, **kwargs):
        super(ArtifactInventoryForm, self).__init__(*args, **kwargs)
        self.fields['condition'].widget = forms.Select(choices=self.fields['condition'].choices)
        self.fields['location'].widget = forms.TextInput(attrs={'placeholder': 'Enter location'})