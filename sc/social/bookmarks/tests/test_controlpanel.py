import unittest

from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName
from Products.PloneTestCase.ptc import PloneTestCase

from sc.social.bookmarks.tests.layer import SocialBookmarksLayer

class SocialBookmarksTest(PloneTestCase):

    layer = SocialBookmarksLayer

    def test_socialbookmarks_controlpanel_view(self):
        # social bookmarks setting control panel view
        view = getMultiAdapter((self.portal, self.portal.REQUEST), name='bookmarks-providers')
        view = view.__of__(self.portal)
        self.failUnless(view())

    def test_socialbookmarks_controlpanel_view_protected(self):
        # social bookmarks setting control panel view can not be accessed by anonymous users
        from AccessControl import Unauthorized
        self.logout()
        self.assertRaises(Unauthorized, self.portal.restrictedTraverse, '@@bookmarks-providers')

    def test_configlet_install(self):
        controlpanel = getToolByName(self.portal, 'portal_controlpanel')
        installed = [a.getAction(self)['id'] for a in controlpanel.listActions()]
        self.failUnless('socialbookmarks' in installed)

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

