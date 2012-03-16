from five import grok
from zope import schema

from plone.directives import form, dexterity
#from plone.plone.namedfile.field import NamedBLobFile
#from plone.plone.namedfile.field import NamedBlobImage
from plone.app.textfield import RichText
from plone.z3cform.textlines import TextLinesFieldWidget
from plone.autoform.interfaces import IFormFieldProvider
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.relationfield.schema import RelationList
from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.indexer import indexer

from sinar.corruptiontracker import _


class IIssue(form.Schema):
    """A Corrruption Issue
    """
  
    details = RichText(
                title=_(u"Corruption Details"),
                required=True,
            ) 
    financial_cost = schema.Int(
                        title=_(u"Financial Cost"),
                        description=_(u"Total financial cost of this corruption issue in RM"),
                        required=False,
                        )

    form.widget(persons_directly_implicated=TextLinesFieldWidget)
    persons_directly_implicated = schema.List(
                            title =_(u"Persons directly implicated"),
                            description=_(u"Persons directly implicated ie. with name or should be charged with corruption. One per line."),
                            value_type=schema.TextLine(),
                            required=False,
                            )
    form.widget(persons_indirectly_implicated=TextLinesFieldWidget)
    persons_indirectly_implicated = schema.List(
                            title =_(u"Persons indirectly implicated. "),
                            description =_(u"eg. minister or superior who approved loan or awarded tender. One per line."),
                            value_type = schema.TextLine(),
                            required=False
                            )
    form.widget(persons_disclosing=TextLinesFieldWidget)
    persons_disclosing = schema.List(
                            title = _(u"Persons disclosing"),
                            description = _(u"Persons who public disclosed this issue. One per line."),
                            value_type = schema.TextLine(),
                            required=False
                            )
    form.widget(persons_supporting=TextLinesFieldWidget)
    persons_supporting= schema.List(
                            title = _(u"Persons supporting"),
                            description = _(u"Persons who support persons implicated such as defending their actions or defending that this is not an issue of corruption. One per line."),
                            value_type = schema.TextLine(),
                            required=False
                            )
    form.widget(persons_against=TextLinesFieldWidget)
    persons_against= schema.List(
                            title = _(u"Persons against"),
                            description = _(u"Persons who are against this action per line."),
                            value_type = schema.TextLine(),
                            required=False
                            )

    related_issues = RelationList(
        title=u"Related Issues",
        default=[],
        value_type=RelationChoice(title=_(u"Related"),
                                source=ObjPathSourceBinder()),
        required=False,
        )

@indexer(IIssue)
def searchableIndexer(obj):
    return "%s %s %s" % (obj.title, obj.description, obj.details.output)
grok.global_adapter(searchableIndexer, name='SearchableText')

@indexer(IIssue)
def indexer_persons_directly_implicated(obj):
    if obj.persons_directly_implicated:
        return tuple(obj.persons_directly_implicated)
grok.global_adapter(indexer_persons_directly_implicated, name='persons_directly_implicated')


