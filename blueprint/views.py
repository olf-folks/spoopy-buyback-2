from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import BlueprintBase
from .models import BlueprintVersion

def index(request):
    blueprints = "test"
    return render(request, 'blueprint/index.html')

def blueprint_list(request):
    blueprints = BlueprintBase.objects.all()
    return render(request, 'blueprint/blueprint_list.html', {'blueprints': blueprints})

def blueprint_detail(request, blueprint_id):
    blueprint = get_object_or_404(Blueprint, pk=blueprint_id)
    return render(request, 'blueprint/blueprint_detail.html', {'blueprint': blueprint})
