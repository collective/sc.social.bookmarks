# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing import logout

from plone.registry.interfaces import IRegistry

from sc.social.bookmarks.browser.common import SocialBookmarksViewlet

from sc.social.bookmarks.controlpanel.bookmarks import IProvidersSchema

from sc.social.bookmarks.testing import INTEGRATION_TESTING


class ViewletTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.reg = getUtility(IRegistry)
        self.set_up_social_bookmarks()
        self.wt = self.portal.portal_workflow
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']
        self.folder.invokeFactory('Document', 'foo')
        self.page = self.folder['foo']

    def set_up_social_bookmarks(self, providers=(), portal_types=()):
        reg = self.reg
        controlpanel = reg.forInterface(IProvidersSchema,
                                        prefix="sc.social.bookmarks")
        providers = providers or ('Reddit', )
        controlpanel.bookmark_providers = (providers)
        portal_types = portal_types or ('Document', )
        controlpanel.enabled_portal_types = (portal_types)

    def _enable_sb_action(self):
        reg = self.reg
        controlpanel = reg.forInterface(IProvidersSchema,
                                        prefix="sc.social.bookmarks")
        controlpanel.use_as_action = True

    def test_viewlet_not_enabled(self):
        """ Not enabled for folders
        """
        viewlet = SocialBookmarksViewlet(self.folder, self.request, None)
        viewlet.update()
        self.assertEqual(viewlet.enabled, False)

    def test_viewlet_enabled(self):
        """ Enabled for pages
        """
        viewlet = SocialBookmarksViewlet(self.page, self.request, None)
        viewlet.update()
        self.assertEqual(viewlet.enabled, True)

    def test_viewlet_enabled_anonymous(self):
        """ Enabled for pages, even for anonymous
        """
        logout()
        viewlet = SocialBookmarksViewlet(self.page, self.request, None)
        viewlet.update()
        self.assertEqual(viewlet.enabled, True)

    def test_as_action_not_enabled(self):
        """ Viewlet display as document action is not available by default
        """
        viewlet = SocialBookmarksViewlet(self.page, self.request, None)
        viewlet.update()
        self.assertEqual(viewlet.action_enabled, False)

    def test_as_action_enabled(self):
        """ Enable viewlet as document action
        """
        self._enable_sb_action()
        viewlet = SocialBookmarksViewlet(self.page, self.request, None)
        viewlet.update()
        self.assertEqual(viewlet.action_enabled, True)

    def test_rendering(self):
        """ Validate if Reddit is rendered as an option
        """
        viewlet = SocialBookmarksViewlet(self.page, self.request, None)
        viewlet.update()
        html = viewlet.render()
        self.assertTrue('Reddit' in html)

        expected = "http://reddit.com/submit?url=http://nohost"
        self.assertTrue(expected in html)

    def test_wrong_provider(self):
        """ Deal with a wrong provider set on the registry
        """
        self.set_up_social_bookmarks(providers=('foo', ))
        viewlet = SocialBookmarksViewlet(self.page, self.request, None)
        viewlet.update()
        html = viewlet.render()
        self.assertFalse('foo' in html)

    def test_provider_without_url(self):
        """ Deal with a provider set without an url template
        """
        from plone.registry import field
        from plone.registry.record import Record
        reg = self.reg
        value = {u'url': u'', u'logo': u'', u'id': u'foo'}
        record = Record(field.Dict(title=u"Foo"), value)
        reg.records['sc.social.bookmarks.providers.foo'] = record
        self.set_up_social_bookmarks(providers=('foo', ))
        viewlet = SocialBookmarksViewlet(self.page, self.request, None)
        viewlet.update()
        html = viewlet.render()
        self.assertFalse('foo' in html)
