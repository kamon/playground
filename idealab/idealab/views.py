from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.renderers import get_renderer

from substanced.sdi import mgmt_view
from substanced.form import FormView
from substanced.interfaces import IRoot
from substanced.interfaces import IFolder

from .interfaces import (
    IIdeas,
    IIdea,    
    )
    
from .resources import (
    Ideas,
    
    IdeaSchema,
    Idea,

    LinkSchema,
    Link,
    )



## Retail view for ideas
@view_config(
    context=Idea,
    renderer='templates/idea.pt',
    )
def idea_view(context, request):
    links = []
    for name, item in context['links'].items():
        if request.registry.content.istype(item, 'Link'):
            links.append(
                {'url': item.url,
                 'title': item.title,
                 #'edit_url': , # How to link back to the SDI view ?
                 })

    return {'title': "Idea %s" % context.title,
            'body': context.text,
            'links': links,
            'master': get_renderer('templates/master.pt').implementation(),
           }


