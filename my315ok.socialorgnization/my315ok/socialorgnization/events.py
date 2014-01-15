#-*- coding: UTF-8 -*-
from zope import interface
from zope.component import adapts
from zope.component.interfaces import ObjectEvent

from my315ok.socialorgnization.interfaces import ICreateOrgEvent

class CreateOrgEvent(object):
    interface.implements(ICreateOrgEvent)
    
    def __init__(self,id,title,description,address,legal_person,supervisor,\
                 register_code,belondto_area,organization_type,announcement_type,passDate):
        """角色,级别,备注"""
        self.id = id
        self.title = title
        self.description = description
        self.address = address 
        self.legal_person = legal_person
        self.supervisor = supervisor
        self.register_code = register_code
        self.belondto_area = belondto_area
        self.organization_type = organization_type 
        self.announcement_type = announcement_type
        self.passDate = passDate

         

       