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

from zc.relation.interfaces import ICatalog
from Acquisition import aq_inner
from zope.component import getUtility
from zope import component
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission

from Products.CMFCore.utils import getToolByName


class IPerson(form.Schema):
    """Person of Interest
    """
  
    details = RichText(
                title=_(u"Details"),
                required=False,
            ) 


class View(dexterity.DisplayForm):
    grok.context(IPerson),
    grok.require('zope2.View')

    def directly_implicated(self):
        
        catalog = component.getUtility(ICatalog)
        intids = component.getUtility(IIntIds)
        context = aq_inner(self.context)
        rels=catalog.findRelations({'to_id': intids.getId(context),
                          'from_attribute' : "persons_directly_implicated"},
                                     )
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

    def indirectly_implicated(self):
        
        #from ipdb import set_trace; set_trace()
        
        catalog = component.getUtility(ICatalog)
        intids = component.getUtility(IIntIds)
        rels=catalog.findRelations({'to_id': intids.getId(self.context),
                          'from_attribute' : "persons_indirectly_implicated"},
                                     )
        result = []
        for i in rels:
            result.append(i.from_object)
        return result

    def indirectly_implicated(self):
        
        #from ipdb import set_trace; set_trace()
        
        catalog = component.getUtility(ICatalog)
        intids = component.getUtility(IIntIds)
        rels=catalog.findRelations({'to_id': intids.getId(self.context),
                          'from_attribute' : "persons_indirectly_implicated"},
                                     )
        result = []
        for i in rels:
            result.append(i.from_object)
        return result

    def supporting(self):
        
        #from ipdb import set_trace; set_trace()
        
        catalog = component.getUtility(ICatalog)
        intids = component.getUtility(IIntIds)
        rels=catalog.findRelations({'to_id': intids.getId(self.context),
                          'from_attribute' : "persons_supporting"},
                                     )
        result = []
        for i in rels:
            result.append(i.from_object)
        return result

    def against(self):
        
        #from ipdb import set_trace; set_trace()
        
        catalog = component.getUtility(ICatalog)
        intids = component.getUtility(IIntIds)
        rels=catalog.findRelations({'to_id': intids.getId(self.context),
                          'from_attribute' : "persons_against"},
                                     )
        result = []
        for i in rels:
            result.append(i.from_object)
        return result

    def disclosing(self):
        
        #from ipdb import set_trace; set_trace()
        
        catalog = component.getUtility(ICatalog)
        intids = component.getUtility(IIntIds)
        rels=catalog.findRelations({'to_id': intids.getId(self.context),
                          'from_attribute' : "persons_disclosing"},
                                     )
        result = []
        for i in rels:
            result.append(i.from_object)
        return result


@indexer(IPerson)
def searchablePersonIndexer(obj):
    return  obj.details.output
grok.global_adapter(searchablePersonIndexer, name='SearchablePersonText')
