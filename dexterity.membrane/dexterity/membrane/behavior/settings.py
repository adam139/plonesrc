from zope.interface import Interface
from zope import schema
from dexterity.membrane import _

from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.z3cform import layout


class IDexterityMembraneSettings(Interface):
    """ Enables through-the-web configuration of some aspects of the
        dexterity.membrane behaviours.
    """

    local_roles = schema.Set(
        title=_(u'Local Roles'),
        description=_(u'The list of additional local roles members will be granted in the context of their own profile objects'),
        value_type=schema.TextLine(),
        required=False,
        missing_value=set([]),
        default=set([]))

    use_email_as_username = schema.Bool(
        title=_(u'Use email address for username?'),
        description=_(u'If checked, the value in the email field will be used as a username/login. If unchecked, your content type must provide a username field.'),
        required=False)

    use_uuid_as_userid = schema.Bool(
        title=_(u'Use object UUID for the userid?'),
        description=_(u'If checked, the UUID value for the adapted object will be used for a userid. Otherwise, the username will be used for the userid.'),
        required=False)


class DexterityMembraneControlPanelForm(RegistryEditForm):
    schema = IDexterityMembraneSettings


DexterityMembraneControlPanelView = layout.wrap_form(
    DexterityMembraneControlPanelForm, ControlPanelFormWrapper)
