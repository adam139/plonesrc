from zope.interface import implements
from AccessControl import getSecurityManager

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Acquisition import aq_inner
from zope.component import getMultiAdapter

#from plone.portlet.collection.collection import ICollectionPortlet
#from plone.portlet.collection.collection import Assignment as baseAssignment
from plone.portlet.collection.collection import Renderer as baseRenderer

# TODO: If you define any fields for the portlet configuration schema below
# do not forget to uncomment the following import
from zope import schema
from zope.formlib import form
from plone.memoize.instance import memoize


from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from Products.ATContentTypes.interface import IATTopic

# TODO: If you require i18n translation for any of your schema fields below,
# uncomment the following to import your package MessageFactory
from my315ok.portlet.groupcollection import groupcollectionMessageFactory as _
from my315ok.portlet.groupcollection import ploneMessageFactory as _p


class Igroupcollection(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    header = schema.TextLine(title=_p(u"Portlet header"),
                             description=_p(u"Title of the rendered portlet"),
                             required=True)
    header2 = schema.TextLine(title=_p(u"Portlet header"),
                             description=_p(u"Title of the rendered portlet"),
                             required=True)
    header3 = schema.TextLine(title=_p(u"Portlet header"),
                             description=_p(u"Title of the rendered portlet"),
                             required=True)

    header4 = schema.TextLine(title=_p(u"Portlet header"),
                             description=_p(u"Title of the rendered portlet"),
                             required=True)
        
    target_collection = schema.Choice(title=_p(u"Target collection"),
                                  description=_p(u"Find the collection which provides the items to list"),
                                  required=True,
                                  source=SearchableTextSourceBinder(
            {'portal_type': ('Topic', 'Collection')},
            default_query='path:'))
    target_collection2 = schema.Choice(title=_p(u"Target collection"),
                                  description=_p(u"Find the collection which provides the items to list"),
                                  required=True,
                                  source=SearchableTextSourceBinder(
            {'portal_type': ('Topic', 'Collection')},
            default_query='path:'))
    target_collection3 = schema.Choice(title=_p(u"Target collection"),
                                  description=_p(u"Find the collection which provides the items to list"),
                                  required=True,
                                  source=SearchableTextSourceBinder(
            {'portal_type': ('Topic', 'Collection')},
            default_query='path:'))
    
    target_collection4 = schema.Choice(title=_p(u"Target collection"),
                                  description=_p(u"Find the collection which provides the items to list"),
                                  required=True,
                                  source=SearchableTextSourceBinder(
            {'portal_type': ('Topic', 'Collection')},
            default_query='path:'))

    limit = schema.Int(title=_p(u"Limit"),
                       description=_p(u"Specify the maximum number of items to show in the portlet. "
                                       "Leave this blank to show all items."),
                       required=False)
                       
    random = schema.Bool(title=_p(u"Select random items"),
                         description=_p(u"If enabled, items will be selected randomly from the collection, "
                                        "rather than based on its sort order."),
                         required=True,
                         default=False)
                       
    show_more = schema.Bool(title=_p(u"Show more... link"),
                       description=_p(u"If enabled, a more... link will appear in the footer of the portlet, "
                                      "linking to the underlying Collection."),
                       required=True,
                       default=True)
                       
    show_dates = schema.Bool(title=_p(u"Show dates"),
                       description=_p(u"If enabled, effective dates will be shown underneath the items listed."),
                       required=True,
                       default=False)
    
    crop_title = schema.Bool(title=_p(u"crop title"),
                         description=_p(u"If enabled, title will be cropped using specify number words."),
                         required=True,
                         default=False)
    wordsnum = schema.Int(title=_p(u"number"),
                       description=_p(u"Specify the maximum number of words to show as title. "
                                       "Leave this blank to show all items."),
                       default=6,
                       required=False)

class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(Igroupcollection)

    header = u""
    header3 = u""
    header2 = u""
    header4 = u""    
    target_collection=None
    target_collection3=None
    target_collection4=None    
    target_collection2=None
    limit = None
    random = False
    show_more = True
    show_dates = False
    crop_title = False
    wordsnum = 6

    def __init__(self, header=u"",header3=u"",header4=u"",header2=u"", target_collection=None,\
                 target_collection3=None,target_collection2=None,target_collection4=None,limit=None, random=False, show_more=True, show_dates=False,crop_title=False,wordsnum=6):
        self.header = header
        self.header3 = header3
        self.header4 = header4        
        self.header2 = header2
        self.target_collection = target_collection
        self.target_collection3 = target_collection3
        self.target_collection4 = target_collection4        
        self.target_collection2 = target_collection2
        self.limit = limit
        self.random = random
        self.show_more = show_more
        self.show_dates = show_dates
        self.crop_title = crop_title
        self.wordsnum = wordsnum

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.header

class Renderer(baseRenderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('groupcollection.pt')
    
    @property
    def available(self):
        s = self.available1 or self.available3 or self.available2 or self.available4
        return s
        
    @property
    def available1(self):
        return len(self.results(self.data.target_collection))
    @property
    def available2(self):
        return len(self.results(self.data.target_collection2))
    
    @property
    def available3(self):
        return len(self.results(self.data.target_collection3))    
    
    @property
    def available4(self):
        return len(self.results(self.data.target_collection4))        
    


    def collection_url(self,target_collection):
        collection = self.collection(target_collection)
        if collection is None:
            return None
        else:
            return collection.absolute_url()

    def results(self,target_collection):
        """ Get the actual result brains from the collection. 
            This is a wrapper so that we can memoize if and only if we aren't
            selecting random items."""
        if self.data.random:
            return self._random_results(target_collection)
        else:
            return self._standard_results(target_collection)


    @memoize    
    def _standard_results(self,target_collection):
        results = []
        collection = self.collection(target_collection)
        if collection is not None:
            limit = self.data.limit
            if limit and limit > 0:
                # pass on batching hints to the catalog
                results = collection.queryCatalog(batch=True, b_size=limit)
                if results == []:return results
                
                results = results._sequence
            else:
                results = collection.queryCatalog()

        return results

    def _random_results(self,target_collection):
        # intentionally non-memoized
        results = []
        collection = self.collection(target_collection)
        if collection is not None:
            results = collection.queryCatalog(sort_on=None)
            if results is None:
                return []
            limit = self.data.limit and min(len(results), self.data.limit) or 1

            if len(results) < limit:
                limit = len(results)
            results = random.sample(results, limit)

        return results

    @memoize
    def collection(self,target_collection):
        collection_path = target_collection
        if not collection_path:
            return None

        if collection_path.startswith('/'):
            collection_path = collection_path[1:]

        if not collection_path:
            return None

        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        portal = portal_state.portal()
        if isinstance(collection_path, unicode):
            # restrictedTraverse accepts only strings
            collection_path = str(collection_path)

        result = portal.unrestrictedTraverse(collection_path, default=None)
        if result is not None:
            sm = getSecurityManager()
            if not sm.checkPermission('View', result):
                result = None
        return result



class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(Igroupcollection)

    form_fields['target_collection'].custom_widget = UberSelectionWidget
    form_fields['target_collection2'].custom_widget = UberSelectionWidget
    form_fields['target_collection3'].custom_widget = UberSelectionWidget
    form_fields['target_collection4'].custom_widget = UberSelectionWidget    
    
    label = _p(u"Add Collection Portlet")
    description = _p(u"This portlet display a listing of items from a Collection.")

    def create(self, data):
        return Assignment(**data)


# NOTE: If this portlet does not have any configurable parameters, you
# can use the next AddForm implementation instead of the previous.

# class AddForm(base.NullAddForm):
#     """Portlet add form.
#     """
#     def create(self):
#         return Assignment()


# NOTE: If this portlet does not have any configurable parameters, you
# can remove the EditForm class definition and delete the editview
# attribute from the <plone:portlet /> registration in configure.zcml


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(Igroupcollection)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
    form_fields['target_collection2'].custom_widget = UberSelectionWidget
    form_fields['target_collection3'].custom_widget = UberSelectionWidget
    form_fields['target_collection3'].custom_widget = UberSelectionWidget
    form_fields['target_collection4'].custom_widget = UberSelectionWidget 
        
    label = _p(u"Edit Collection Portlet")
    description = _p(u"This portlet display a listing of items from a Collection.")
