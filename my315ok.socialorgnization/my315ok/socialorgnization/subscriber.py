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
        ot = event.belondto_area 
        if  isinstance(ot, unicode):
            ot = ot.encode("utf-8")
        if ot == '\xe5\xb2\xb3\xe5\xa1\x98\xe5\x8c\xba':  # 岳塘区
            item.belondto_area = "yuetangqu"
        elif ot == '\xe9\x9b\xa8\xe6\xb9\x96\xe5\x8c\xba':  #雨湖区
            item.belondto_area = "yuhuqu"
        elif ot == '\xe9\x9f\xb6\xe5\xb1\xb1\xe5\xb8\x82':  #韶山市
            item.belondto_area = "shaoshanshi"
        elif ot == '\xe6\xb9\x98\xe4\xb9\xa1\xe5\xb8\x82':  #湘乡市
            item.belondto_area = "xiangxiangshi"  
        elif ot == '\xe6\xb9\x98\xe6\xbd\xad\xe5\x8e\xbf':  #湘潭县
            item.belondto_area = "xiangtanxian"                                   
        else:
            item.belondto_area = "xiangtanshi"             #湘潭市  
#        item.belondto_area = event.belondto_area        
        ot = event.organization_type
        if  isinstance(ot, unicode):
            ot = ot.encode("utf-8")
        if ot == '\xe6\xb0\x91\xe9\x9d\x9e':  # 民非
            item.organization_type = "minfei"
        elif ot == '\xe7\xa4\xbe\xe4\xbc\x9a\xe5\x9b\xa2\xe4\xbd\x93':  #社会团体
            item.organization_type = "shetuan"
        else:
            item.organization_type = "jijinhui"
        

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
    
                  
                            
    
        
