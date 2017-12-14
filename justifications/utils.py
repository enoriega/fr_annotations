import itertools as it
from collections import defaultdict
from django.db.models import Q
from django.db import transaction
import csv, os


from .models import *


def get_items():
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'to_annotate.txt')
    with open(path) as f:
        reader = csv.reader(f)
        rows = list(reader)

    weighs = list()

    for row in rows:
        weighs.append((int(row[0]), len(row[1:])))

    weighs = sorted(weighs, key=lambda x: x[1], reverse=True)

    pathways = defaultdict(list)
    for row in rows:
        iid = int(row[0])
        pways = row[1:]
        for pway in pways:
            pathways[pway].append(iid)

    sorted_pathways = sorted([(k, sum(v)) for k, v in pathways.iteritems()], key=lambda x: x[1], reverse=True)

    # Small collection so doesn't matter if this is suboptimal
    ret = list()
    for p in sorted_pathways:
        for iid in pathways[p[0]]:
            if not iid in ret:
                ret.append(iid)

    return ret



    return [(pmcid, int(interaction)) for pmcid, interaction in rows]

def get_next_to_annotate(items):

    # Build constraints
    constraints = Q(id = items[0])

    for interaction_id in items[1:]:
        constraints |= Q(id = interaction_id)

    unannotated = Interactions.objects.filter(annotated__isnull =True)

    elements = unannotated.filter(constraints)

    elements = sorted(elements, key=lambda e: items.index(e.id))

    total_elements = len(items)

    if len(elements) > 0:
        index = total_elements - len(elements) + 1
        return elements[0], index, total_elements
    else:
        return None, 0, total_elements

def get_skipped(items):
    # Build constraints
    skipped = Interactions.objects.filter(annotated = False)

    if skipped.count() > 0:
        elements = list()
        indices = list()
        for e in skipped:
            elements.append(e)
            indices.append(items.index(e.id)+1)
        return elements, indices
    else:
        return list(), list()


def highlight_participants(e):
    controller = e.controller_text
    controlled = e.controlled_text

    text = e.evidence.split('++++')[0]

    text = text.replace(controller, '<span class="controller">%s</span>' % controller)
    text = text.replace(controlled, '<span class="controlled">%s</span>' % controlled)

    return text

def group_evidence(evidence):
    grouped = defaultdict(list)

    for e in evidence:
        key = (e.evidence, e.controller_text, e.controlled_text)
        grouped[key].append(e)

    ret = list()
    for k in grouped:
        elements = grouped[k]
        representative = elements[0]
        ids = '_'.join(str(e.id) for e in elements)
        representative.id = ids
        ret.append(representative)

    return ret

@transaction.atomic
def store_annotation(params):

    annotation_id = int(params['interaction_id'])
    annotated_fields = [k for k in params if k.startswith("sentence") and params[k] == 'on']
    annotated_sentence_ids = [int(i) for i in it.chain(*[k.split('_')[1:] for k in annotated_fields])]

    pi = Interactions.objects.get(pk=annotation_id)
    sentences = Evidence.objects.filter(id__in=annotated_sentence_ids)

    pi.annotated = True
    pi.save()
    for s in sentences:
        s.correct = True
        s.save()

@transaction.atomic
def skip_annotation(params):

    annotation_id = int(params['interaction_id'])

    pi = Interactions.objects.get(pk=annotation_id)
    pi.annotated = False
    pi.save()


@transaction.atomic
def clear_annotations():
    for pi in Interactions.objects.filter(annotated__isnull = False):
        pi.annotated = None
        pi.save()

    for e in Evidence.objects.filter(correct__isnull = False):
        e.correct = None
        e.save()
