from django.db.models import Q

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
        return list()

def highlight_participants(e):
    controller = e.controller_text
    controlled = e.controlled_text

    text = e.evidence

    text = text.replace(controller, '<span class="controller">%s</span>' % controller)
    text = text.replace(controlled, '<span class="controlled">%s</span>' % controlled)

    return text
