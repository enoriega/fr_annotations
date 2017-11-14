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
    pi = get_next_to_annotate(elements)

    if pi is not None:
        # Get the information we care about
        interaction = pi.interaction
        evidence = Evidence.objects.filter(pmcid = pi.pmcid, interaction = interaction.id)

        evidence = group_evidence(evidence)

        for e in evidence:
            e.text = highlight_participants(e)


        return HttpResponse(render(request, "justifications/annotate.html", { "pi":pi, "interaction": interaction,
            'evidence_set': evidence} ))
    else:
        return HttpResponse(render(request, "justifications/finished.html"))

def save_annotation(request):
    if request.method == "POST":
        store_annotation(request.POST)

    return redirect('annotate')
