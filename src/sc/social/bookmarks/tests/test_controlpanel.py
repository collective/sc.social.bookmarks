import unittest

from zope.component import getMultiAdapter
from zope.component import getUtility

from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from plone.registry.interfaces import IRegistry

from sc.social.bookmarks.config import PROJECTNAME
from sc.social.bookmarks.controlpanel.bookmarks import IProvidersSchema
from sc.social.bookmarks.testing import INTEGRATION_TESTING


class SocialBookmarksTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_controlpanel_has_view(self):
        # social bookmarks setting control panel view
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name='bookmarks-providers')
        view = view.__of__(self.portal)
        self.failUnless(view())

    def test_controlpanel_view_is_protected(self):
        # social bookmarks setting control panel view can not be accessed
        # by anonymous users
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized, self.portal.restrictedTraverse,
                          '@@bookmarks-providers')

    def test_controlpanel_installed(self):
        cp = self.controlpanel
        installed = [a.getAction(self)['id'] for a in cp.listActions()]
        self.failUnless('socialbookmarks' in installed)

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertTrue('socialbookmarks' not in actions,
                        'control panel was not removed')


class RegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.prefix = 'sc.social.bookmarks.'
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IProvidersSchema,
                                                   prefix=self.prefix)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_sections_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'bookmark_providers'))
        self.assertNotEqual(self.settings.bookmark_providers, None)

        self.assertTrue(hasattr(self.settings, 'enabled_portal_types'))
        self.assertNotEqual(self.settings.enabled_portal_types, None)

        self.assertTrue(hasattr(self.settings, 'use_as_action'))
        self.assertNotEqual(self.settings.use_as_action, None)

        self.assertTrue(hasattr(self.settings, 'show_icons_only'))
        self.assertNotEqual(self.settings.show_icons_only, None)

    def get_record(self, record):
        """ Helper function; it raises KeyError if the record is not in the
        registry.
        """
        prefix = self.prefix
        return self.registry[prefix + record]

    def test_records_removed_on_uninstall(self):
        # XXX: I haven't found a better way to test this; anyone?
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        self.assertRaises(KeyError, self.get_record, 'bookmark_providers')
        self.assertRaises(KeyError, self.get_record, 'enabled_portal_types')
        self.assertRaises(KeyError, self.get_record, 'use_as_action')
        self.assertRaises(KeyError, self.get_record, 'show_icons_only')
