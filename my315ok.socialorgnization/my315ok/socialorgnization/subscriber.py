#-*- coding: UTF-8 -*-
import json
from five import grok
from time import strftime, localtime 
from zope.component import getMultiAdapter

from my315ok.socialorgnization.interfaces import ICreateOrgEvent

from Products.CMFCore.utils import getToolByName

from plone.dexterity.utils import createContentInContainer

from zope.site.hooks import getSite
from zope.component import getUtility

from zope.interface import Interface
from ZODB.POSException import ConflictError
from zExceptions import Forbidden

from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone import PloneMessageFactory as _p
#from collective.singing import mail
from my315ok.socialorgnization.content.orgnization import IOrgnization
#from my315ok.socialorgnization.content.orgnization import IOrgnization_administrative_licence
#from my315ok.socialorgnization.content.orgnization import IOrgnization_annual_survey
from my315ok.socialorgnization.content.orgnizationfolder import IOrgnizationFolder

# be call by membrane.usersinout
@grok.subscribe(ICreateOrgEvent)
def CreateOrgEvent(event):
    """this event be fired by member join event, username,address password parameters to create a membrane object"""
    site = getSite()
#    mp = getToolByName(site,'portal_membership')
#    members = mp.getMembersFolder()
#    if members is None: return      
    catalog = getToolByName(site,'portal_catalog')
    try:
        newest = catalog.unrestrictedSearchResults({'object_provides': IOrgnizationFolder.__identifier__})
    except:
        return      

    memberfolder = newest[0].getObject()


    memberid = event.id        
    try:
        item =createContentInContainer(memberfolder,"my315ok.socialorgnization.orgnization",checkConstraints=False,id=memberid)
#        setattr(memberfolder,'registrant_increment',memberid)
        item.title = event.title 

        item.description = event.description
        item.address = event.address
        item.legal_person = event.legal_person 
        item.supervisor = event.supervisor
        item.register_code = event.register_code
        ot = event.organization_type
        if  isinstance(ot, unicode):
            ot = ot.encode("utf-8")
        if ot == '\xe6\xb0\x91\xe9\x9d\x9e':  # 民非
            item.organization_type == "minfei"
        elif ot == '\xe7\xa4\xbe\xe4\xbc\x9a\xe5\x9b\xa2\xe4\xbd\x93':  #社会团体
            item.organization_type == "shetuan"
        else:
            item.organization_type == "jijinhui"
        

#        item.announcement_type = event.announcement_type
        
        import datetime
        datearray = event.passDate.split('-')
        if len(datearray) >= 3:
            val = map(int,datearray)
               
            item.passDate = datetime.date(*val)  
        else:
            item.passDate = datetime.date.today()
        item.reindexObject()                
#        membrane = getToolByName(item, 'membrane_tool')
#        membrane.reindexObject(item)        
    except:
        return
    
                  
                            
    
        
