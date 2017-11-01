# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import *
from .utils import *

# Create your views here.
def index(request):
    return HttpResponse("Here we will see the justifications")

def annotate(request):

    elements = get_items()

    # Get the next item to annotate
    pi = get_next_to_annotate(elements)

    # Get the information we care about
    interaction = pi.interaction
    evidence = Evidence.objects.filter(pmcid = pi.pmcid, interaction = interaction.id)

    for e in evidence:
        e.text = highlight_participants(e)


    return HttpResponse(render(request, "justifications/annotate.html", { "interaction": interaction,
        'evidence_set': evidence} ))
