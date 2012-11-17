import unittest

from zope.component import getUtility

from plone.browserlayer.utils import registered_layers

from plone.registry.interfaces import IRegistry

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from sc.social.bookmarks.config import PROJECTNAME

from sc.social.bookmarks.controlpanel.bookmarks import IProvidersSchema

from sc.social.bookmarks.testing import INTEGRATION_TESTING

CSS = (
    '++resource++sb_resources/social_bookmark.css',
)

JS = (
    '++resource++sb_resources/social_bookmarks_overlay.js',
)

CONFIGLETS = (
    'socialbookmarks',
)


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.props = self.portal['portal_properties']
        self.registry = getUtility(IRegistry)

    def _load_profile(self, st=None, profile_id=''):
        if not (st and profile_id):
            return
        from Products.GenericSetup import profile_registry
        from Products.CMFCore.interfaces import ISiteRoot
        from Products.GenericSetup import EXTENSION
        profile_registry.registerProfile(
            name=profile_id, title=profile_id,
            description=(profile_id),
            path='profiles/%s' % profile_id,
            product='sc.social.bookmarks.tests',
            profile_type=EXTENSION, for_=ISiteRoot)
        profile = 'profile-sc.social.bookmarks.tests:%s' % profile_id
        st.runAllImportStepsFromProfile(profile)

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('ISocialBookmarksLayer' in layers,
                        'add-on layer was not installed')

    def test_jsregistry(self):
        resource_ids = self.portal.portal_javascripts.getResourceIds()
        for id in JS:
            self.assertTrue(id in resource_ids, '%s not installed' % id)

    def test_cssregistry(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        for id in CSS:
            self.assertTrue(id in resource_ids, '%s not installed' % id)

    def test_upgrade_1_to_2(self):
        profile_id = 'sc.social.bookmarks:default'
        st = getattr(self.portal, 'portal_setup')
        st.setLastVersionForProfile(profile_id, u'1')
        upgrades = st.listUpgrades(profile_id)
        step_info = upgrades[0]
        self.assertEquals(step_info.get('ssource'), '1')
        self.assertEquals(step_info.get('sdest'), '2')
        step = step_info['step']
        step.doStep(st)
        new_version = st.getLastVersionForProfile(profile_id)
        self.assertEquals(new_version, (u'2', ))

    def test_upgrade_2_to_3(self):
        st = getattr(self.portal, 'portal_setup')
        profile_id = 'sc.social.bookmarks:default'
        st.setLastVersionForProfile(profile_id, u'2')
        upgrades = st.listUpgrades(profile_id)
        step_info = upgrades[0]
        self.assertEquals(step_info.get('ssource'), '2')
        self.assertEquals(step_info.get('sdest'), '3')
        step = step_info['step']
        step.doStep(st)
        new_version = st.getLastVersionForProfile(profile_id)
        self.assertEquals(new_version, (u'3', ))

    def test_upgrade_2_to_3_property_sheet_migration(self):
        # Load a profile that will create a property sheet
        # as we used to have until version 3
        st = getattr(self.portal, 'portal_setup')
        self._load_profile(st, 'version2')

        props = self.portal.portal_properties
        sheet = getattr(props, 'sc_social_bookmarks_properties', None)
        self.assertFalse(sheet is None)
        self.assertEquals(sheet.bookmark_providers, ('Reddit', 'Twitter'))
        self.assertEquals(sheet.enabled_portal_types, ('Document', ))

        profile_id = 'sc.social.bookmarks:default'
        st.setLastVersionForProfile(profile_id, u'2')
        upgrades = st.listUpgrades(profile_id)
        step = upgrades[0]['step']
        step.doStep(st)

        sheet = getattr(props, 'sc_social_bookmarks_properties', None)
        self.assertTrue(sheet is None)
        settings = self.registry.forInterface(IProvidersSchema,
                                              prefix='sc.social.bookmarks.')
        self.assertTrue(hasattr(settings, 'bookmark_providers'))
        self.assertEqual(settings.bookmark_providers, ('Reddit', 'Twitter'))

        self.assertTrue(hasattr(settings, 'enabled_portal_types'))
        self.assertEqual(settings.enabled_portal_types, ('Document', ))


class UninstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_removed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('ICoverLayer' not in layers,
                        'add-on layer was not removed')

    def test_jsregistry_removed(self):
        resource_ids = self.portal.portal_javascripts.getResourceIds()
        for id in JS:
            self.assertTrue(id not in resource_ids, '%s not removed' % id)

    def test_cssregistry_removed(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        for id in CSS:
            self.assertTrue(id not in resource_ids, '%s not removed' % id)
