# artifacts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Artifact, ArtifactInventory
from .forms import ArtifactForm
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files import File
from .forms import RestorationHistoryForm
from django import forms
from .forms import ArtifactInventoryForm


def home(request):
    newest_artifacts = Artifact.objects.order_by('-date_found')[:5]
    
    return render(request, 'artifacts/home.html', {'newest_artifacts': newest_artifacts})
def artifact_list(request):
    artifacts = Artifact.objects.all().order_by('-date_found')

    year = request.GET.get('year')
    start_year = request.GET.get('start_year')
    end_year = request.GET.get('end_year')

    if year:
        try:
            year = int(year)
            artifacts = artifacts.filter(date_found__year=year)
        except ValueError:
            pass
    elif start_year and end_year:
        try:
            start_year = int(start_year)
            end_year = int(end_year)
            artifacts = artifacts.filter(date_found__year__range=(start_year, end_year))
        except ValueError:
            pass

    all_years = Artifact.objects.dates('date_found', 'year', order='DESC')
    year_options = sorted(set(y.year for y in all_years), reverse=True)

    return render(request, 'artifacts/artifact_list.html', {
        'artifacts': artifacts,
        'year_options': year_options,
        'request_get': request.GET  # Pass explicitly for safety in template
    })
def artifact_detail(request, pk):
    artifact = get_object_or_404(Artifact, pk=pk)
    inventory = ArtifactInventory.objects.filter(artifact=artifact)  # Get inventory for this artifact
    restorations = artifact.restorations.all()

    context = {
        'artifact': artifact,
        'inventory': inventory,
    }
    return render(request, 'artifacts/artifact_detail.html', {'artifact': artifact})

def artifact_create(request):
    if request.method == 'POST':
        form = ArtifactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('artifact_list')
    else:
        form = ArtifactForm()
    return render(request, 'artifacts/artifact_form.html', {'form': form})

def artifact_update(request, pk):
    artifact = get_object_or_404(Artifact, pk=pk)
    if request.method == 'POST':
        form = ArtifactForm(request.POST, request.FILES, instance=artifact)
        if form.is_valid():
            form.save()
            return redirect('artifact_list')
    else:
        form = ArtifactForm(instance=artifact)
    return render(request, 'artifacts/artifact_form.html', {'form': form})

def artifact_delete(request, pk):
    artifact = get_object_or_404(Artifact, pk=pk)
    if request.method == 'POST':
        artifact.delete()
        return redirect('artifact_list')
    return render(request, 'artifacts/artifact_confirm_delete.html', {'artifact': artifact})

def dashboard(request):
    total_artifacts = Artifact.objects.count()
    total_origins = Artifact.objects.values('origin').distinct().count()
    oldest_artifact = Artifact.objects.order_by('date_found').first()
    
    context = {
        'total_artifacts': total_artifacts,
        'total_origins': total_origins,
        'oldest_artifact': oldest_artifact,
    }
    return render(request, 'artifacts/dashboard.html', context)

def add_restoration(request, artifact_id):
    artifact = get_object_or_404(Artifact, pk=artifact_id)
    
    if request.method == 'POST':
        form = RestorationHistoryForm(request.POST)
        if form.is_valid():
            restoration = form.save(commit=False)
            restoration.artifact = artifact
            restoration.save()
            return redirect('artifact_detail', pk=artifact.id)
    else:
        form = RestorationHistoryForm()
    
    return render(request, 'artifacts/add_restoration.html', {'form': form, 'artifact': artifact})

def update_inventory(request, artifact_id):
    artifact = get_object_or_404(Artifact, id=artifact_id)
    inventory = getattr(artifact, 'inventory', None)

    if request.method == 'POST':
        form = ArtifactInventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            inventory = form.save(commit=False)
            inventory.artifact = artifact
            inventory.save()
            return redirect('artifact_detail', pk=artifact.id) 
    else:
        form = ArtifactInventoryForm(instance=inventory)

    return render(request, 'artifacts/update_inventory.html', {
        'form': form,
        'artifact': artifact
    })
