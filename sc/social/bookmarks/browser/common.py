# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Acquisition import Explicit
from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts
from zope.component import getUtility
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.publisher.interfaces.browser import IBrowserView
from zope.contentprovider.interfaces import IContentProvider
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import ViewletBase
from plone.memoize.view import memoize
from plone.registry.interfaces import IRegistry
from sc.social.bookmarks.config import all_providers
from sc.social.bookmarks.controlpanel.bookmarks import IProvidersSchema
from string import Template
import re


class SocialBookmarksBase(object):
    """Abstract Base class for social bookmarks.
    """

    @memoize
    def settings(self):
        controlpanel = getUtility(IRegistry).forInterface(IProvidersSchema,
                                                 prefix="sc.social.bookmarks")
        return controlpanel

    @memoize
    def _availableProviders(self):
        bookmark_providers = self.settings().bookmark_providers
        providers=[]
        for bookmarkId in bookmark_providers:
            tmp_providers = [provider for provider in all_providers if provider.get('id', '') == bookmarkId]
            if not tmp_providers:
                continue
            else:
                provider = tmp_providers[0]

            logo = provider.get('logo','')
            url = provider.get('url','')
            providers.append({'id': bookmarkId, 'logo': logo, 'url': url})

        return providers

    def providers(self):
        """Returns a list of dicts with providers already
        filtered and populated.
        """
        context = aq_inner(self.context)
        available = self._availableProviders()
        providers = []
        param = {}
        param['title'] = context.Title()
        param['description'] = context.Description()
        param['url'] = context.absolute_url()
        # BBB: Instead of using string formatting we moved to string Templates
        pattern = re.compile("\%\(([a-zA-Z]*)\)s")
        for provider in available:
            url_tmpl = provider.get('url','').strip()
            if not(url_tmpl):
                continue
            url_tmpl = re.sub(pattern,r'${\1}',url_tmpl)
            provider['url'] = Template(url_tmpl).safe_substitute(param)
            providers.append(provider)
        return providers

    @property
    def icons_only(self):
        """Flag whether to show icons only.
        """
        return self.settings().show_icons_only

    @property
    def action_enabled(self):
        """Validates if social bookmarks should be enabled
        for this context using an action.
        """
        return self.settings().use_as_action

    @property
    def enabled(self):
        """Validates if social bookmarks should be enabled
        for this context.
        """
        import pdb; pdb.set_trace()
        context = aq_inner(self.context)
        return context.portal_type in self.settings().enabled_portal_types


class SocialBookmarksProvider(Explicit, SocialBookmarksBase):
    """Social Bookmarks Viewlet content provider
    """

    implements(IContentProvider)
    adapts(Interface, IBrowserRequest, IBrowserView)
    template = ViewPageTemplateFile(u'templates/bookmarks.pt')

    def __init__(self, context, request, view):
        self.__parent__ = view
        self.context = context
        self.request = request

    def update(self): pass

    def render(self):
        return self.template(self)


class SocialBookmarksView(BrowserView, SocialBookmarksBase):
    """Social Bookmarks Viewlet
    """


class SocialBookmarksViewlet(ViewletBase, SocialBookmarksBase):
    """Social Bookmarks Viewlet
    """
