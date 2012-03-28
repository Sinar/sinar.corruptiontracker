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
from sinar.corruptiontracker.person import IPerson
from sinar.corruptiontracker.organization import IOrganization

class IIssue(form.Schema):
    """A Corrruption Issue
    """

    issue_start = schema.Date(
                    title=_(u"Date Issue Occurred/Started"),
                    required=False,
                    )

    issue_end = schema.Date(
                    title=_(u"Date Issue Ended"),
                    description=_(u"When it stopped happening, if not single occurence."),
                    required=False,
                    )


    financial_cost = schema.Int(
                        title=_(u"Financial Cost"),
                        description=_(u"Total financial cost of this corruption issue in RM"),
                        required=False,
                        )
  
    details = RichText(
                title=_(u"Corruption Details"),
                required=True,
            ) 
    persons_directly_implicated = RelationList( 
        title =_(u"Persons directly implicated"),
        description=_(u"Persons directly implicated ie. with name or should be charged with corruption. One per line."),
        default=[],
        value_type=RelationChoice(title=_(u"Related Persons"), 
                                  source= ObjPathSourceBinder(object_provides=IPerson.__identifier__)),
        required=False,
        )

    persons_indirectly_implicated = RelationList(
                            title =_(u"Persons indirectly implicated. "),
                            description =_(u"eg. minister or superior who approved loan or awarded tender."),
                            value_type=RelationChoice(title=_(u"Related Persons"), 
                                  source= ObjPathSourceBinder(object_provides=IPerson.__identifier__)),
                            required=False
                            )

    persons_disclosing = RelationList(
                                title = _(u"Persons disclosing"),
                                description = _(u"Persons who public disclosed this issue."),
                                value_type=RelationChoice(title=_(u"Related Persons"), 
                                  source= ObjPathSourceBinder(object_provides=IPerson.__identifier__)),
                                required=False
                                )
    persons_supporting= RelationList(
                            title = _(u"Persons supporting"),
                            description = _(u"Persons who support persons implicated such as defending their actions or defending that this is not an issue of corruption."),
                            value_type=RelationChoice(title=_(u"Related Persons"), 
                                  source= ObjPathSourceBinder(object_provides=IPerson.__identifier__)),
                            required=False
                            )
    persons_against= RelationList(
                            title = _(u"Persons against"),
                            description = _(u"Persons who are against this action."),
                            value_type=RelationChoice(title=_(u"Related Persons"), 
                                  source= ObjPathSourceBinder(object_provides=IPerson.__identifier__)),
                            required=False
                            )

    implicated_organization = RelationList(
        title=u"Organizations implicated",
        default=[],
        value_type=RelationChoice(title=_(u"Implicated Organizations"),
            source=ObjPathSourceBinder(object_provides="sinar.corruptiontracker.organization.IOrganization")),
        required=False,
        )

    related_issues = RelationList(
        title=u"Related Issues",
        default=[],
        value_type=RelationChoice(title=_(u"Related"),
                                source=ObjPathSourceBinder(object_provides="sinar.corruptiontracker.issue.IIssue")),
        required=False,
        )

class View(dexterity.DisplayForm):
    grok.context(IIssue),
    grok.require('zope2.View')

@indexer(IIssue)
def searchableIndexer(obj):
    return "%s %s %s" % (obj.title, obj.description, obj.details.output)
grok.global_adapter(searchableIndexer, name='SearchableText')

