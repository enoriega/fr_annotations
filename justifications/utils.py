import itertools as it
from collections import defaultdict
from django.db.models import Q
from django.db import transaction

from .models import *

def get_items():
    return [('PMC3291551', 725796),
 (u'PMC2802674', 653779),
 (u'PMC2802674', 271606),
 (u'PMC2802674', 147146),
 (u'PMC3174991', 177945),
 (u'PMC3174991', 653910),
 (u'PMC3174991', 311170),
 (u'PMC3174991', 317982),
 (u'PMC3174991', 514640),
 (u'PMC3174991', 390812),
 (u'PMC3174991', 9901)]

def get_next_to_annotate(items):
    # Build constraints
    constraints = Q(pmcid=items[0][0], interaction_id = items[0][1])

    for pmcid, interaction_id in items[1:]:
        constraints |= Q(pmcid=pmcid, interaction_id = interaction_id)

    unannotated = PaperInteraction.objects.filter(annotated__isnull = True)

    elements = unannotated.filter(constraints)

    if elements.count() > 0:
        return elements[0]
    else:
        return None

def highlight_participants(e):
    controller = e.controller_text
    controlled = e.controlled_text

    text = e.evidence

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

    pi = PaperInteraction.objects.get(pk=annotation_id)
    sentences = Evidence.objects.filter(id__in=annotated_sentence_ids)

    pi.annotated = True
    pi.save()
    for s in sentences:
        s.correct = True
        s.save()


@transaction.atomic
def clear_annotations():
    for pi in PaperInteraction.objects.filter(annotated__isnull = False):
        pi.annotated = None
        pi.save()

    for e in Evidence.objects.filter(correct__isnull = False):
        e.correct = None
        e.save()
