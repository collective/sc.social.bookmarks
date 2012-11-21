# -*- coding: utf-8 -*-
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from sc.social.bookmarks import _
from sc.social.bookmarks.browser.common import SocialBookmarksBase


class ISocialBookmarksPortlet(IPortletDataProvider):
    pass


class Assignment(base.Assignment):
    implements(ISocialBookmarksPortlet)

    @property
    def title(self):
        return _(u"Social Bookmarks Portlet")


class AddForm(base.NullAddForm):
    form_fields = form.Fields(ISocialBookmarksPortlet)
    label = _(u"Add a social bookmarks portlet")
    description = _(u"This portlet shows links to other sites, where the "
                    u"current content can be posted to.")

    def create(self):
        return Assignment()


class Renderer(base.Renderer, SocialBookmarksBase):
    render = ViewPageTemplateFile('templates/bookmarks_portlet.pt')

    @property
    def available(self):
        return self.enabled
