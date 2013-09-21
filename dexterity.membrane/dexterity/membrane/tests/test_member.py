#-*- coding: UTF-8 -*-
import unittest

from Products.CMFCore.utils import getToolByName
from plone.app.content.interfaces import INameFromTitle
from plone.app.dexterity.behaviors import metadata
from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.behavior.interfaces import IBehaviorAssignable
from dexterity.membrane.content.member import IMember

from dexterity.membrane.behavior.membraneuser import IMembraneUser
from dexterity.membrane.behavior.membraneuser import INameFromFullName
from dexterity.membrane.behavior.membraneuser import IProvidePasswords
from dexterity.membrane.behavior.membraneuser import get_full_name
from dexterity.membrane.membrane_helpers import get_user_id_for_email
from dexterity.membrane.tests.base import TestCase
from zope import event
from dexterity.membrane.events import CreateMembraneEvent

class TestMember(TestCase):
    def test_createmembrane_event(self):
        membrane = getToolByName(self.portal, 'membrane_tool')
        catalog = getToolByName(self.portal, 'portal_catalog')
        
        newest = catalog.unrestrictedSearchResults({'object_provides': IMember.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on': 'created'})                            
        start_count = len(newest)
# create memberfolder
        memberfolder = self._createType(
            self.portal, 'dexterity.membrane.memberfolder', 'memberfolder')
         
# email,password,title,description,homepage,phone,organization,sector,position,province,address               
        event.notify(CreateMembraneEvent('1000000',
                                         u'12@qq.com',
                                         u'password',
                                         u'唐军',
                                         u'',
                                         u'http://315ok.org',
                                         u'135',
                                         u'315ok',
                                         u'IT',
                                         u'CEO',
                                         u'HuNan',
                                         u'xt'))
        brain = catalog.unrestrictedSearchResults({'object_provides': IMember.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on': 'created'})   
        now_count = len(brain)

        self.assertEqual(start_count + 1,now_count)
        self.assertEqual(brain[0].id,str(1000000))
        event.notify(CreateMembraneEvent('1000001',
                                         u'13@qq.com',
                                         u'password',
                                         u'唐军2',
                                         u'',
                                         u'http://315ok.org',
                                         u'135',
                                         u'315ok',
                                         u'IT',
                                         u'CEO',
                                         u'HuNan',
                                         u'xt'))
        newest = catalog.unrestrictedSearchResults({'object_provides': IMember.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on': 'created',
                             'sort_limit': 1})        
        self.assertEqual(newest[0].id,str(1000001))                                         

    def test_create_member(self):
        member = self._createType(
            self.portal, 'dexterity.membrane.member', 'jane')
        self.assertEqual(member.portal_type, 'dexterity.membrane.member')
        
    def test_create_member(self):
        memberfolder = self._createType(
            self.portal, 'dexterity.membrane.memberfolder', 'memberfolder')
        self.assertEqual(memberfolder.portal_type, 'dexterity.membrane.memberfolder')
        
    def test_member_is_membrane_type(self):
        membrane = getToolByName(self.portal, 'membrane_tool')
        self.assertTrue('dexterity.membrane.member' in
                        membrane.listMembraneTypes())
        # Fine, it is a membrane_type, but does it actually work?  We
        # add a member and see if we can find it again using the
        # membrane_tool.

        # Record the current number of members; we do not want this
        # test to fail just because someone adds an extra test member
        # somewhere.
        start_count = len(membrane.unrestrictedSearchResults())
        member = self._createType(
            self.portal, 'dexterity.membrane.member', 'jane')
        # Need to reindex the new object manually in the tests (or
        # maybe notify an event).  We would want to just do
        # 'member.reindexObject()' but that is apparently not enough
        # to get it added to the membrane_tool catalog.  Simply adding
        # a member in the live site works though and we do not need to
        # redo the membrane or collective.indexing tests here.
#        membrane.reindexObject(member)
#        self.assertEqual(len(membrane.unrestrictedSearchResults()),
#                         start_count + 1)

    def test_member_properties(self):
        # Some properties from portal_memberdate can be queried from
        # the member content item.
        member = self._createType(
            self.portal, 'dexterity.membrane.member', 'joe')
        member.first_name = 'Joe'
        member.last_name = 'User'
        member.title = 'Joe User'
        member.email = 'joe@example.org'
        member.homepage = 'http://example.org/'
#        member.bio = u'I am Joe.  I want to set a good example.'
        member.description = u'I am Joe.  I want to set a good example.'        
        membrane = getToolByName(self.portal, 'membrane_tool')
        membrane.reindexObject(member)
        # Currently the user_id is an intid, so we need to query for
        # that by email/login name:
        user_id = get_user_id_for_email(self.portal, 'joe@example.org')
        self.assertTrue(user_id)
        memship = getToolByName(self.portal, 'portal_membership')
        user = memship.getMemberById(user_id)
        self.failUnless(user)
        self.assertEqual(user.getProperty('fullname'), 'Joe User')
        self.assertEqual(user.getProperty('email'), 'joe@example.org')
        self.assertEqual(user.getProperty('home_page'), 'http://example.org/')
        self.assertEqual(user.getProperty('description'),
                         u'I am Joe.  I want to set a good example.')

    def test_user_name(self):
        # Some upper and lower case issues.
        member = self._createType(
            self.portal, 'dexterity.membrane.member', 'joe')
        member.email = 'JOE@example.org'
        member.password = 'secret'
        member.confirm_password = 'secret'
        membrane = getToolByName(self.portal, 'membrane_tool')
        membrane.reindexObject(member)

        # Uppercase:
        user_id = get_user_id_for_email(self.portal, 'JOE@EXAMPLE.ORG')
        self.assertFalse(user_id)

        # Lowercase:
        user_id = get_user_id_for_email(self.portal, 'joe@example.org')
        self.assertFalse(user_id)

        # Mixed case:
        user_id = get_user_id_for_email(self.portal, 'joe@EXAMPLE.org')
        self.assertFalse(user_id)

        # Mixed case:
        user_id = get_user_id_for_email(self.portal, 'JOE@example.org')
        self.assertTrue(user_id)

        # Real authentication is pickier on the case unfortunately.
        auth = self.portal.acl_users.membrane_users.authenticateCredentials
        credentials = {'login': 'JOE@example.org', 'password': 'secret'}
        # First the member needs to be enabled before authentication
        # can succeed.
        self.assertEqual(auth(credentials), None)
# pending status may login
#        self.assertEqual(auth(credentials), (user_id, 'JOE@example.org'))        
        wf_tool = getToolByName(self.portal, 'portal_workflow')
        self.setRoles(['Reviewer'])
        wf_tool.doActionFor(member, 'enable')
        self.setRoles([])
#        self.assertEqual(auth(credentials), None)        
        self.assertEqual(auth(credentials), (user_id, 'JOE@example.org'))

        # It would be nice if we could get the next test to pass by
        # setting self.portal.membrane_tool.case_sensitive_auth to
        # False, but this does not work as advertised.
        #credentials = {'login': 'JOE@EXAMPLE.ORG', 'password': 'secret'}
        #self.assertEqual(auth(credentials), (user_id, 'joe@example.org'))

        # Sanity check:
        credentials = {'login': 'otherjoe@example.org', 'password': 'secret'}
        self.assertEqual(auth(credentials), None)

    def test_delete_member(self):
        # Deleting should not leave behind the old brain in the
        # membrane catalog.  Actually, we can just check that an
        # unindexObject works properly.  Note that collective.indexing
        # needs to be available for this, and its monkey patches
        # applied, which should happen automatically on startup.
        member = self._createType(
            self.portal, 'dexterity.membrane.member', 'joe')
        member.email = 'joe@example.org'
        membrane = getToolByName(self.portal, 'membrane_tool')
        membrane.reindexObject(member)
        self.assertEqual(len(membrane.unrestrictedSearchResults(
            exact_getUserName='joe@example.org')), 1)
        member.unindexObject()
        self.assertEqual(len(membrane.unrestrictedSearchResults(
            exact_getUserName='joe@example.org')), 0)

    def test_reset_password(self):
        member = self._createType(
            self.portal, 'dexterity.membrane.member', 'joe')
        member.email = 'joe@example.org'
        self.portal.membrane_tool.reindexObject(member)
        user_id = get_user_id_for_email(self.portal, 'joe@example.org')
        self.portal.acl_users.userSetPassword(user_id, 'foobar')
        from AccessControl.AuthEncoding import pw_validate
        self.assertTrue(pw_validate(member.password, 'foobar'))

    def test_default_local_roles(self):
        # Members get extra local roles on their own object.
        # Get tools:
        membrane = getToolByName(self.portal, 'membrane_tool')
        memship = getToolByName(self.portal, 'portal_membership')
        # Create joe:
        joe = self._createType(self.portal, 'dexterity.membrane.member', 'joe')
        joe.email = 'joe@example.org'
        membrane.reindexObject(joe)
        joe_id = get_user_id_for_email(self.portal, 'joe@example.org')
        self.assertTrue(joe_id)
        # Create bob:
        bob = self._createType(self.portal, 'dexterity.membrane.member', 'bob')
        bob.email = 'bob@example.org'
        membrane.reindexObject(bob)
        bob_id = get_user_id_for_email(self.portal, 'bob@example.org')
        self.assertTrue(bob_id)
        # Get members:
        joe_member = memship.getMemberById(joe_id)
        self.assertTrue(joe_member)
        bob_member = memship.getMemberById(bob_id)
        self.assertTrue(bob_member)
        # At first, no one gets an extra local role, because the
        # members are not enabled.
        # Test roles of fresh joe:
        self.assertEqual(joe_member.getRolesInContext(self.portal),
                         ['Member','Authenticated'])
        self.assertEqual(joe_member.getRolesInContext(self.portal.bob),
                         ['Member','Authenticated'])
        self.assertEqual(sorted(joe_member.getRolesInContext(self.portal.joe)),
                         ['Authenticated','Member'])
        # Test roles of fresh bob:
        self.assertEqual(bob_member.getRolesInContext(self.portal),
                         ['Member','Authenticated'])
        self.assertEqual(sorted(bob_member.getRolesInContext(self.portal.bob)),
                         ['Authenticated','Member'])
        self.assertEqual(bob_member.getRolesInContext(self.portal.joe),
                         ['Member','Authenticated'])
        # We enable/approve both members now.
        wf_tool = getToolByName(self.portal, 'portal_workflow')
        self.setRoles(['Reviewer'])
        wf_tool.doActionFor(joe, 'enable')
        wf_tool.doActionFor(bob, 'enable')
        # Do some reindexing for good measure (alternatively: fire
        # some events).
        #membrane.reindexObject(joe)
        #membrane.reindexObject(bob)
        # Test roles of enabled joe:
        self.assertEqual(joe_member.getRolesInContext(self.portal),
                         ['Member','Authenticated'])
        self.assertEqual(joe_member.getRolesInContext(self.portal.bob),
                         ['Member','Authenticated'])
        self.assertEqual(sorted(joe_member.getRolesInContext(self.portal.joe)),
                         ['Authenticated', u'Creator', u'Editor', 'Member', u'Reader'])
        # Test roles of enabled bob:
        self.assertEqual(bob_member.getRolesInContext(self.portal),
                         ['Member','Authenticated'])
        self.assertEqual(sorted(bob_member.getRolesInContext(self.portal.bob)),
                         ['Authenticated', u'Creator', u'Editor', 'Member', u'Reader'])
        self.assertEqual(bob_member.getRolesInContext(self.portal.joe),
                         ['Member','Authenticated'])
        # Now disable both members:
        wf_tool.doActionFor(joe, 'disable')
        wf_tool.doActionFor(bob, 'disable')
        # Test the most important roles again:
        self.assertEqual(sorted(joe_member.getRolesInContext(self.portal.joe)),
                         ['Authenticated','Member'])
        self.assertEqual(sorted(bob_member.getRolesInContext(self.portal.bob)),
                         ['Authenticated','Member'])

    def test_local_roles_are_configurable(self):
        memship = getToolByName(self.portal, 'portal_membership')
        # Create joe, approve him, and get him indexed with membrane
        joe = self._createType(self.portal, 'dexterity.membrane.member', 'joe')
        joe.email = 'joe@example.org'
        wf_tool = getToolByName(self.portal, 'portal_workflow')
        self.setRoles(['Reviewer'])
        wf_tool.doActionFor(joe, 'enable')
        joe.reindexObject()
        joe_id = get_user_id_for_email(self.portal, 'joe@example.org')
        joe_member = memship.getMemberById(joe_id)
        # Test default roles:
        self.assertEqual(sorted(joe_member.getRolesInContext(self.portal.joe)),
                         ['Authenticated', 'Creator', 'Editor', 'Member','Reader'])
        # Adjust the registry setting
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        from dexterity.membrane.behavior import settings
        reg = getUtility(IRegistry)
        config = reg.forInterface(settings.IDexterityMembraneSettings, False)
        config.local_roles = set([u'Reader'])
        # Roles should now be trimmed down
        self.assertEqual(sorted(joe_member.getRolesInContext(self.portal.joe)),
                         ['Authenticated', 'Member','Reader'])

    def test_member_behaviors(self):
        behaviors = [INameFromFullName, IReferenceable,
                     metadata.ICategorization, metadata.IPublication,
                     metadata.IOwnership, IMembraneUser, IProvidePasswords]
        member = self._createType(
            self.portal, 'dexterity.membrane.member', 'les')
        assignable = IBehaviorAssignable(member)
        for b in behaviors:
            self.assertTrue(assignable.supports(b),
                            "member type should support %s behavior" % b)

    def test_member_behavior_blacklist(self):
        # Some behaviors should definitely NOT be provided.
        black_list = [metadata.IDublinCore, metadata.IBasic]
        # Note that we would want INameFromTitle in the black list as
        # well, but it cannot be, as it gets pulled in as base class
        # of INameFromFullName.
        member = self._createType(
            self.portal, 'dexterity.membrane.member', 'les')
        assignable = IBehaviorAssignable(member)
        for b in black_list:
            self.assertFalse(assignable.supports(b),
                            "member type should NOT support %s behavior" % b)

    def test_name_from_full_name(self):
        # We do not want to set a title but instead have the first and
        # last name used as title.  We do not mind too much if the
        # title field itself is empty, as long as we have our ways to
        # get the fullname and get a name (basis for id) based on our
        # title.
        member = self._createType(
            self.portal, 'dexterity.membrane.member', 'joe')
        name_title = INameFromTitle(member)
#        import pdb
#        pdb.set_trace()
        self.assertEqual(name_title.title, u'')
        member.title = u"Joe User"

#        self.assertEqual(name_title.title, u'')
#        member.last_name = u"User"
#        self.assertEqual(name_title.title, u'User')
#        member.first_name = u"Joe"
        self.assertEqual(name_title.title, u'Joe User')
        self.assertEqual(get_full_name(member), u'Joe User')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMember))
    return suite
