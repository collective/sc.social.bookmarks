# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing import logout

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer

from plone.registry.interfaces import IRegistry

from Products.GenericSetup.utils import _getDottedName

from sc.social.bookmarks.browser import portlet

from sc.social.bookmarks.controlpanel.bookmarks import IProvidersSchema

from sc.social.bookmarks.testing import INTEGRATION_TESTING


class BasePortlet(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.set_up_social_bookmarks()
        self.wt = self.portal.portal_workflow
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']
        self.folder.invokeFactory('Document', 'foo')
        self.page = self.folder['foo']

    def set_up_social_bookmarks(self):
        reg = getUtility(IRegistry)
        controlpanel = reg.forInterface(IProvidersSchema,
                                        prefix="sc.social.bookmarks")
        controlpanel.bookmark_providers = (('Reddit', ))
        controlpanel.enabled_portal_types = (('Page', ))


class PortletRegistrationTest(BasePortlet):

    def test_portlet_registered(self):
        sb_portlet = queryUtility(IPortletType,
                                  name='sc.social.bookmarks.sb_portlet')
        self.assertEqual(sb_portlet.addview, 'sc.social.bookmarks.sb_portlet')

    def test_registered_interfaces(self):
        sb_portlet = queryUtility(IPortletType,
                                  name='sc.social.bookmarks.sb_portlet')
        registered_interfaces = [_getDottedName(i) for i in sb_portlet.for_]
        registered_interfaces.sort()
        self.assertEqual(['plone.app.portlets.interfaces.IColumn',
                          'plone.app.portlets.interfaces.IDashboard'],
                         registered_interfaces)

    def test_interfaces(self):
        sb_portlet = portlet.Assignment()
        self.assertTrue(IPortletAssignment.providedBy(sb_portlet))
        self.assertTrue(IPortletDataProvider.providedBy(sb_portlet.data))

    def test_invoke_addview(self):
        portal = self.portal
        traversal = '++contextportlets++plone.leftcolumn'
        sb_portlet = queryUtility(IPortletType,
                                  name='sc.social.bookmarks.sb_portlet')
        mapping = portal.restrictedTraverse(traversal)
        for m in mapping.keys():
            # Remove all assignments
            del mapping[m]

        addview = mapping.restrictedTraverse('+/' + sb_portlet.addview)

        addview()

        self.assertEqual(len(mapping), 1)
        self.assertTrue(isinstance(mapping.values()[0],
                                   portlet.Assignment))

    def test_renderer(self):
        context = self.page
        request = self.page.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager,
                             name='plone.leftcolumn',
                             context=self.page)
        assignment = portlet.Assignment()

        renderer = getMultiAdapter((context, request, view,
                                    manager, assignment),
                                   IPortletRenderer)
        self.assertTrue(isinstance(renderer, portlet.Renderer))


class PortletRendererTest(BasePortlet):

    def renderer(self, context=None, request=None, view=None,
                 manager=None, assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager,
                                        name='plone.leftcolumn',
                                        context=self.page)

        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

    def test_available_folder(self):
        r = self.renderer(assignment=portlet.Assignment())
        self.assertEqual(False, r.available)

    def test_available_anonymous_folder(self):
        r = self.renderer(assignment=portlet.Assignment())
        logout()
        self.assertEqual(False, r.available)

    def test_available_page(self):
        r = self.renderer(assignment=portlet.Assignment(),
                          context=self.page)
        self.assertEqual(False, r.available)

    def test_available_anonymous_page(self):
        r = self.renderer(assignment=portlet.Assignment(),
                          context=self.page)
        logout()
        self.assertEqual(False, r.available)

    def test_rendering(self):
        r = self.renderer(assignment=portlet.Assignment(),
                          context=self.page)
        html = r.render()
        expected = "http://reddit.com/submit?url=http://nohost"
        self.assertTrue(expected in html)
