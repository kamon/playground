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




## SDI "add" view for ideas
@mgmt_view(
    context=IIdeas,
    name='add_idea',
    tab_title='Add Idea', 
    permission='sdi.add-content', 
    renderer='substanced.sdi:templates/form.pt',
    tab_condition=False,
    )
class AddIdeaView(FormView):
    title = 'Add Idea'
    schema = IdeaSchema()
    buttons = ('add',)

    def add_success(self, appstruct):
        registry = self.request.registry
        name = appstruct.pop('name')
        obj = registry.content.create('Idea', **appstruct)
        self.context[name] = obj
        return HTTPFound(
            self.request.sdiapi.mgmt_path(self.context, '@@contents')
            )


## SDI "add" view for links inside an idea
@mgmt_view(
    context=IIdea,
    name='add_link',
    tab_title='Add Link', 
    permission='sdi.add-content', 
    renderer='substanced.sdi:templates/form.pt',
    tab_condition=False,
    )
class AddLinkView(FormView):
    title = 'Add Link'
    schema = LinkSchema()
    buttons = ('add',)

    def add_success(self, appstruct):
        registry = self.request.registry
        #name = appstruct.pop('name')
        link = registry.content.create('Link', **appstruct)
        self.context.add_link(link)
        
        return HTTPFound(
            self.request.sdiapi.mgmt_path(self.context, '@@contents')
            )

