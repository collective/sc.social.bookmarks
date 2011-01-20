import unittest

from Products.CMFCore.utils import getToolByName
from Products.PloneTestCase.ptc import PloneTestCase

from sc.social.bookmarks.config import PROJECTNAME
from sc.social.bookmarks.tests.layer import SocialBookmarksLayer

STYLESHEETS = (
    '++resource++sb_stylesheets/social_bookmark.css',
    )

JAVASCRIPTS = (
    'sarissa.js',
    '++resource++kukit.js',
    )

KSS = (
    '++resource++sb_stylesheets/share.kss',
    )

CONFIGLETS = (
    'socialbookmarks',
    )

class InstallTest(PloneTestCase):
    
    layer = SocialBookmarksLayer

    def test_stylesheets(self):
        for css in STYLESHEETS:
            self.failUnless(css in self.portal.portal_css.getResourceIds(), '%s stylesheet not installed' % css)

    def test_javascripts(self):
        for js in JAVASCRIPTS:
            self.failUnless(js in self.portal.portal_javascripts.getResourceIds(), '%s javascript not installed' % js)

    def test_kss(self):
        for k in KSS:
            self.failUnless(k in self.portal.portal_kss.getResourceIds(), '%s kss not installed' % k)

    def test_configlets(self):
        installed = [a.getAction(self)['id'] for a in self.portal.portal_controlpanel.listActions()]
        for c in CONFIGLETS:
            self.failUnless(c in installed, '%s configlet not installed' % c)

    def test_actions(self):
        self.fail('To be implemented...')

    def test_viewlets(self):
        self.fail('To be implemented...')

class UninstallTest(PloneTestCase):

    layer = SocialBookmarksLayer

    def afterSetUp(self):
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_product_uninstall(self):
        self.failIf(self.qi.isProductInstalled(PROJECTNAME))

    def test_stylesheets(self):
        for css in STYLESHEETS:
            self.failIf(css in self.portal.portal_css.getResourceIds(), '%s stylesheet not installed' % css)

    def test_javascripts(self):
        for js in JAVASCRIPTS:
            self.failIf(js in self.portal.portal_javascripts.getResourceIds(), '%s javascript not installed' % js)

    def test_kss(self):
        for k in KSS:
            self.failIf(k in self.portal.portal_kss.getResourceIds(), '%s kss not uninstalled' % k)

    def test_configlets(self):
        installed = [a.getAction(self)['id'] for a in self.portal.portal_controlpanel.listActions()]
        for c in CONFIGLETS:
            self.failIf(c in installed, '%s configlet not uninstalled' % c)

    def test_actions(self):
        self.fail('To be implemented...')

    def test_viewlets(self):
        self.fail('To be implemented...')

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

