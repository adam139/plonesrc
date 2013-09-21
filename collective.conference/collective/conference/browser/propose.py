from five import grok
from zope import event

from collective.conference.events import RegisteredConfEvent,RegisteredSessionEvent

from collective.conference.session import ISession, Session
from collective.conference.conference import IConference
from plone.formwidget.captcha import CaptchaFieldWidget
from plone.formwidget.captcha.validator import CaptchaValidator
from plone.dexterity.utils import createContentInContainer
from plone.directives import form
from zope.component.hooks import getSite
from zope.globalrequest import getRequest
from zope import schema
from datetime import timedelta

from Products.CMFPlone.utils import _createObjectByType
from collective.conference import MessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage

class IProposalForm(ISession):
    form.widget(captcha=CaptchaFieldWidget)
    captcha = schema.TextLine(title=u"",
                            required=False)
    form.omitted('conference_rooms', 'color', 'textColor')

@form.validator(field=IProposalForm['captcha'])
def validateCaptca(value):
    site = getSite()
    request = getRequest()

    if request.getURL().endswith('kss_z3cform_inline_validation'):
        return

    captcha = CaptchaValidator(site, request, None,
            IProposalForm['captcha'], None)
    captcha.validate(value)


class ProposalForm(form.SchemaAddForm):
    grok.name('propose')
    grok.context(IConference)
#    grok.require("zope.Public")
    grok.require('zope2.View')    
    schema = IProposalForm
    label = _(u"Propose a Session")

    def create(self, data):
        obj = Session()
        inc = getattr(self.context, 'session_increment', 0) + 1
        data['id'] = 'session-%s' % inc
        data['startDate'] = self.context.startDate
        data['endDate'] = self.context.startDate + timedelta(0, 3600)
        self.context.session_increment = inc
        obj = _createObjectByType("collective.conference.session",
                self.context, data['id'])
        del data['captcha']
        for k, v in data.items():
            setattr(obj, k, v)
        IStatusMessage(self.request).addStatusMessage(
        _(u'Thank you for your submission.' +
        'Your submission is now held for approval and will appear on the ' + 
        'site once it is approved'))
        obj.reindexObject()
#        import pdb
#        pdb.set_trace()
        event.notify(RegisteredSessionEvent(self.context))
        return obj

    def add(self, obj):
        pass
