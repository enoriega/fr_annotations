# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .utils import *

# Create your views here.
def index(request):
    return HttpResponse("Here we will see the justifications")

def annotate(request):

    elements = get_items()

    # Get the next item to annotate
    interaction, index, total = get_next_to_annotate(elements)

    if interaction is not None:
        # Get the information we care about
        #interaction = pi.interaction
        evidence = Evidence.objects.filter(interaction = interaction.id)

        evidence = group_evidence(evidence)

        for e in evidence:
            e.text = highlight_participants(e)

        controller_names = {e.controller_text for e in evidence}
        controlled_names = {e.controlled_text for e in evidence}

        return HttpResponse(render(request, "justifications/annotate.html", {"controllers": controller_names,
            "controlleds":controlled_names, "interaction": interaction,
            'evidence_set': evidence, 'index':index, 'total':total} ))
    else:
        return HttpResponse(render(request, "justifications/finished.html"))

def annotate_one(request, id):
    interaction = Interactions.objects.get(pk=id)
    evidence = Evidence.objects.filter(interaction = interaction.id)

    total = 0
    index = 0

    evidence = group_evidence(evidence)

    for e in evidence:
        e.text = highlight_participants(e)

    controller_names = {e.controller_text for e in evidence}
    controlled_names = {e.controlled_text for e in evidence}

    return HttpResponse(render(request, "justifications/annotate.html", {"controllers": controller_names,
        "controlleds":controlled_names, "interaction": interaction,
        'evidence_set': evidence, 'index':index, 'total':total} ))

def skipped(request):
    elements = get_items()

    # Get the next item to annotate
    interactions, indices = get_skipped(elements)

    if len(interactions) > 0:
        return HttpResponse(render(request, "justifications/skipped.html", {"interactions": zip(interactions, indices)} ))
    else:
        return HttpResponse(render(request, "justifications/finished.html"))

def save_annotation(request):
    if request.method == "POST":
        skipped = request.POST['skipped']
        if skipped == "no":
            store_annotation(request.POST)
        else:
            skip_annotation(request.POST)

    return redirect('annotate')
