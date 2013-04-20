import colander
import deform.widget

from persistent import Persistent

from pyramid.security import (
    Allow,
    Everyone,
    )

from zope.interface import (
    implementer,
    )

from substanced.root import (
    Root,
    RootPropertySheet,
    )

from substanced.content import content
from substanced.folder import Folder
from substanced.property import PropertySheet
from substanced.schema import (
    Schema,
    NameSchemaNode
    )
from substanced.objectmap import find_objectmap
from substanced.util import renamer

from .interfaces import (
    IIdeas,
    IIdea,
    IComment,
    ILink,
    )


@colander.deferred
def now_default(node, kw):
    return datetime.date.today()


# Ideas

# @content(
#     IIdeas,
#     name='Ideas',
#     icon='icon-tags',
# )
# @implementer(IIdeas)
# class Ideas(Folder):
#     def __init__(self):
#         Folder.__init__(self)
#         self.title = 'Ideas'


def ideas_folder_columns(folder, subobject, request, default_columnspec):
    subobject_name = getattr(subobject, '__name__', str(subobject))
    objectmap = find_objectmap(folder)
    
    #user_oid = getattr(subobject, '__creator__', None)
    created = getattr(subobject, '__created__', None)
    modified = getattr(subobject, '__modified__', None)
    #if user_oid is not None:
    #    user = objectmap.object_for(user_oid)
    #    user_name = getattr(user, '__name__', 'anonymous')
    #else:
    #    user_name = 'anonymous'
    if created is not None:
        created = created.isoformat()
    if modified is not None:
        modified = modified.isoformat()
    return default_columnspec + [
        {'name': 'Title',
        'field': 'title',
        'value': getattr(subobject, 'title', ''),
        'sortable': True,
        'formatter': 'icon_label_url',
        },
        {'name': 'Created',
        'field': 'created',
        'value': created,
        'sortable': True,
        'formatter': 'date',
        },
#         {'name': 'Last edited',
#         'field': 'modified',
#         'value': modified,
#         'sortable': True,
#         'formatter': 'date',
#         },
        {'name': 'Author',
        'field': 'author',
        'value': getattr(subobject, 'author', ''),
        'sortable': True,
        }
        ]

@content(
    'Root',
    icon='icon-home',
    propertysheets = (
        ('', RootPropertySheet),
        ),
    columns=ideas_folder_columns,
    after_create= ('after_create', 'after_create2')
    )
@implementer(IIdeas)
class Ideas(Root):
    title = ''

    @property
    def sdi_title(self):
        return self.title

    @sdi_title.setter
    def sdi_title(self, value):
        self.title = value
    
    def after_create2(self, inst, registry):
        self.sdi_title = "Ideas management app"
        acl = getattr(self, '__acl__', [])
        acl.append((Allow, Everyone, 'view'))
        self.__acl__ = acl
        
        
class IdeaSchema(Schema):
    name = NameSchemaNode(
        editing=lambda c, r: r.registry.content.istype(c, 'Idea'),
        )
    title = colander.SchemaNode(
       colander.String(),
       )
    author = colander.SchemaNode(
       colander.String(),
       )
    text = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.RichTextWidget()
        )

class IdeaPropertySheet(PropertySheet):
    schema = IdeaSchema()

@content(
    'Idea',
    icon='icon-align-left',
    add_view='add_idea', 
    propertysheets = (
        ('Basic', IdeaPropertySheet),
        ),
    tab_order=('properties', 'contents', 'acl_edit'),
    catalog=True,
    )
@implementer(IIdea)
class Idea(Folder):

    name = renamer()
    
    def __init__(self, title='', author='', text=''):
        Folder.__init__(self)
        self.title = title
        self.author = author
        self.text = text
        self['attachments'] = Folder()  # implement these later...
        self['links'] = Folder()   
        self['comments'] = Folder()     # implement these later...

    def add_link(self, link):
        while 1:
            linksFolder = self['links']
            name = str(len(linksFolder.items()) + 1)
            #if not name in self:
            linksFolder[name] = link
            break

#     def add_comment(self, comment):
#         while 1:
#             name = str(time.time())
#             if not name in self:
#                 self['comments'][name] = comment
#                 break


class LinkSchema(Schema):
    url = colander.SchemaNode(
       colander.String(),
       validator = colander.url,
       )

    title = colander.SchemaNode(
       colander.String(),
       )
    description = colander.SchemaNode(
       colander.String(),
       )

class LinkPropertySheet(PropertySheet):
    schema = LinkSchema()


@content(
    'Link',
    icon='icon-align-right',
    add_view='add_link',
    propertysheets = (
        ('Basic', LinkPropertySheet),
        ),
    catalog = True,
    )
#@implementer(ILink)
class Link(Persistent):
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description



# class CommentSchema(Schema):
#     commenter = colander.SchemaNode(
#        colander.String(),
#        )
#     text = colander.SchemaNode(
#        colander.String(),
#        )
#     pubdate = colander.SchemaNode(
#        colander.DateTime(),
#        default = now_default,
#        )
# 
# class CommentPropertySheet(PropertySheet):
#     schema = CommentSchema()

# @content(
#     'Comment',
#     icon='icon-comment',
#     add_view='add_comment',
#     propertysheets = (
#         ('Basic', CommentPropertySheet),
#         ),
#     catalog = True,
#     )
# @implementer(IComment)
# class Comment(Persistent):
#     def __init__(self, commenter, text, pubdate):
#         self.commenter = commenter
#         self.text = text
#         self.pubdate = pubdate


