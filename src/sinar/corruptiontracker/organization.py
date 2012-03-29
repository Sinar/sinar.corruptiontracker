from five import grok
from zope import schema

from plone.directives import form, dexterity
from plone.app.textfield import RichText
from plone.z3cform.textlines import TextLinesFieldWidget
from plone.autoform.interfaces import IFormFieldProvider
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.relationfield.schema import RelationList
from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.indexer import indexer

from sinar.corruptiontracker import _
from sinar.corruptiontracker.person import IPerson


from zc.relation.interfaces import ICatalog
from Acquisition import aq_inner
from zope.component import getUtility
from zope import component
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission

from Products.CMFCore.utils import getToolByName


class IOrganization(form.Schema):
    """Organization of Interest
    """
  
    details = RichText(
                title=_(u"Details"),
                required=False,
            ) 

    persons_related = RelationList( 
        title =_(u"Persons related to this organization"),
        description=_(u"Hold positions or are majority shareholders in this organization"),
        default=[],
        value_type=RelationChoice(title=_(u"Related Persons"), 
                                  source= ObjPathSourceBinder(object_provides=IPerson.__identifier__)),
        required=False,
        )

    subsidiaries = RelationList( 
        title =_(u"Subsidiaries of this organization"),
        description=_(u"Wholly or partially owned by this organization"),
        default=[],
        value_type=RelationChoice(title=_(u"Subsidiaries"), 
                                  source= ObjPathSourceBinder(object_provides="sinar.corruptiontracker.organization.IOrganization")),
        required=False,
        )


class View(dexterity.DisplayForm):
    grok.context(IOrganization),
    grok.require('zope2.View')

    def implicated_issues(self):
        
        catalog = component.getUtility(ICatalog)
        intids = component.getUtility(IIntIds)
        context = aq_inner(self.context)
        rels=catalog.findRelations({'to_id': intids.getId(context),
                          'from_attribute' : "implicated_organization"},
                                     )

        #Code following to resolve proper objects from backreferences is
        #crudely cut and pasted below. Should be refactored into a
        #simpler better written function.

        ids = []
        for i in rels:
            ids.append(i.from_object.getId())
        portal_catalog = self.context.portal_catalog
        result = []
        for i in ids:
            items = portal_catalog({'getId': i})
            if items:
                result.append(items[0].getObject())

        return result

    def parent(self):
        
        catalog = component.getUtility(ICatalog)
        intids = component.getUtility(IIntIds)
        context = aq_inner(self.context)
        rels=catalog.findRelations({'to_id': intids.getId(context),
                          'from_attribute' : "subsidiaries"},
                                     )

        #Code following to resolve proper objects from backreferences is
        #crudely cut and pasted below. Should be refactored into a
        #simpler better written function.

        ids = []
        for i in rels:
            ids.append(i.from_object.getId())
        portal_catalog = self.context.portal_catalog
        result = []
        for i in ids:
            items = portal_catalog({'getId': i})
            if items:
                result.append(items[0].getObject())

        return result



@indexer(IOrganization)
def searchableIndexer(obj):
    return "%s %s %s" % (obj.title, obj.description, obj.details.output)
grok.global_adapter(searchableIndexer, name='SearchableText')
