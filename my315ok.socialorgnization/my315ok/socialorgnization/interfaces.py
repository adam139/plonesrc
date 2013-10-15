#-*- coding: UTF-8 -*-
from zope import schema
from zope.interface import Interface
from zope.interface import Attribute

# event
class  ICreateOrgEvent(Interface):
    """新增一个organization object"""
    
