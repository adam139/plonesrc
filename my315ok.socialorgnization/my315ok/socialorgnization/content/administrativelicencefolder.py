from five import grok
from zope import schema

from plone.directives import form, dexterity

from my315ok.socialorgnization import _

class IAdministrativeLicenceFolder(form.Schema):
    """
    a folder contain some administrative licence information for social organizations
    """
