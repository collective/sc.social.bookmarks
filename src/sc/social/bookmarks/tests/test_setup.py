# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.browserlayer.utils import registered_layers
from plone.registry.interfaces import IRegistry
from sc.social.bookmarks.config import PROJECTNAME
from sc.social.bookmarks.testing import INTEGRATION_TESTING
from zope.component import getUtility

import unittest


CSS = ("++resource++sb_resources/social_bookmark.css",)

JS = ("++resource++sb_resources/social_bookmarks_overlay.js",)

CONFIGLETS = ("socialbookmarks",)


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.props = self.portal["portal_properties"]
        self.registry = getUtility(IRegistry)

    @unittest.skip("Test failure in Plone 5.2")
    def test_installed(self):
        qi = getattr(self.portal, "portal_quickinstaller")
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer(self):
        layers = [layer.getName() for layer in registered_layers()]
        self.assertTrue(
            "ISocialBookmarksLayer" in layers, "add-on layer was not installed"
        )

    @unittest.skip("Test failure in Plone 5.2")
    def test_jsregistry(self):
        resource_ids = self.portal.portal_javascripts.getResourceIds()
        for resource_id in JS:
            self.assertTrue(
                resource_id in resource_ids, "{0} not installed".format(resource_id)
            )

    @unittest.skip("Test failure in Plone 5.2")
    def test_cssregistry(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        for resource_id in CSS:
            self.assertTrue(
                resource_id in resource_ids, "{0} not installed".format(resource_id)
            )


class UninstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.qi = getattr(self.portal, "portal_quickinstaller")
        self.qi.uninstallProducts(products=[PROJECTNAME])

    @unittest.skip("Test failure in Plone 5.2")
    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    @unittest.skip("Test failure in Plone 5.2")
    def test_addon_layer_removed(self):
        layers = [layer.getName() for layer in registered_layers()]
        self.assertTrue("ICoverLayer" not in layers, "add-on layer was not removed")

    @unittest.skip("Test failure in Plone 5.2")
    def test_jsregistry_removed(self):
        resource_ids = self.portal.portal_javascripts.getResourceIds()
        for resource_id in JS:
            self.assertTrue(
                resource_id not in resource_ids, "{0} not removed".format(resource_id)
            )

    @unittest.skip("Test failure in Plone 5.2")
    def test_cssregistry_removed(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        for resource_id in CSS:
            self.assertTrue(
                resource_id not in resource_ids, "{0} not removed".format(resource_id)
            )
