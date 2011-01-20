# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets import ViewletBase
from plone.memoize.view import memoize
from sc.social.bookmarks.config import all_providers
from string import Template
import re


class SocialBookmarksBase(object):
    """ Abstract Base class for social bookmarks
    """
    @memoize
    def _availableProviders(self):
        """
        """
        context = aq_inner(self.context)
        pp = getToolByName(context,'portal_properties')
        if hasattr(pp,'sc_social_bookmarks_properties'):
            bookmark_providers = pp.sc_social_bookmarks_properties.getProperty("bookmark_providers") or []
        else:
            bookmark_providers = []
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
           filtered and populated"""
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
    def enabled(self):
        """Validates if social bookmarks should be enabled
           for this context"""
        context = aq_inner(self.context)
        pp = getToolByName(context,'portal_properties')
        if hasattr(pp,'sc_social_bookmarks_properties'):
            enabled_portal_types = pp.sc_social_bookmarks_properties.getProperty("enabled_portal_types") or []
        else:
            enabled_portal_types = []
        return context.portal_type in enabled_portal_types


class SocialBookmarksView(BrowserView, SocialBookmarksBase):
    """ Social Bookmarks View
    """

class SocialBookmarksViewlet(ViewletBase, SocialBookmarksBase):
    """ Social Bookmarks Viewlet
    """