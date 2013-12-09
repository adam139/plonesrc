#-*- coding: UTF-8 -*-
from five import grok
import json

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from zope.i18n.interfaces import ITranslationDomain
from zope.component import queryUtility
from zope.component import getMultiAdapter

from Products.CMFCore.interfaces import ISiteRoot
from plone.app.layout.navigation.interfaces import INavigationRoot

from my315ok.socialorgnization import _
from z3c.form import form, field
from plone.directives import form,dexterity


from my315ok.socialorgnization.content.orgnization import IOrgnization
from my315ok.socialorgnization.content.orgnization import IOrgnization_administrative_licence
from my315ok.socialorgnization.content.orgnization import IOrgnization_annual_survey
from my315ok.socialorgnization.content.orgnizationfolder import IOrgnizationFolder





class EditOrgnizationSurvey(dexterity.EditForm):
    grok.name('ajaxedit')
    grok.context(IOrgnization_annual_survey)    
    label = _(u'Edit Organization Survey')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IOrgnization_annual_survey).select('annual_survey', 'year')  

class EditOrgnizationLicence(dexterity.EditForm):
    grok.name('ajaxedit')
    grok.context(IOrgnization_administrative_licence)    
    label = _(u'Edit Organization Licence')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IOrgnization_administrative_licence).select('audit_item','audit_result')   
    
class EditOrgnization(dexterity.EditForm):
    grok.name('ajaxedit')
    grok.context(IOrgnization)    
    label = _(u'Edit Organization')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IOrgnization).select('title', 'description','address','belondto_area','legal_person',
                                                'supervisor','register_code','organization_type','passDate')  