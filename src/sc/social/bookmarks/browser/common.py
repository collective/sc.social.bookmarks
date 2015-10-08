# -*- coding: utf-8 -*-
import logging
import re
from string import Template

from Acquisition import aq_inner
from Acquisition import Explicit
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import ViewletBase
from plone.memoize.view import memoize
from plone.registry.interfaces import IRegistry
from zope.component import adapts
from zope.component import getUtility
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Interface
from zope.interface import implements
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.publisher.interfaces.browser import IBrowserView

from ..controlpanel.bookmarks import IProvidersSchema


logger = logging.getLogger(__name__)


class SocialBookmarksBase(object):
    """Abstract Base class for social bookmarks.
    """
    def _registry(self):
        return getUtility(IRegistry)

    def _all_providers(self):
        """ Return a dict with all providers """
        reg = self._registry()
        providers = [reg[k] for k in reg.records.keys()
                     if k.startswith('sc.social.bookmarks.providers')]
        all_providers = dict([(p.get('id'), p) for p in providers])
        return all_providers

    def settings(self):
        reg = self._registry()
        controlpanel = reg.forInterface(IProvidersSchema,
                                        prefix="sc.social.bookmarks")
        return controlpanel

    def _availableProviders(self):
        all_providers = self._all_providers()
        bookmark_providers = self.settings().bookmark_providers or []
        providers = []
        for bookmark_id in bookmark_providers:
            provider = all_providers.get(bookmark_id, None)
            if not provider:
                continue
            providers.append(provider)

        return providers

    def providers(self):
        """Returns a list of dicts with providers already
        filtered and populated.
        """
        context = aq_inner(self.context)
        portal_url = getToolByName(context, 'portal_url')()
        available = self._availableProviders()
        providers = []
        # Attributes available to be substituted in the URL
        param = {
            'title': context.Title(),
            'description': context.Description(),
            'url': context.absolute_url()
        }
        # BBB: Instead of using string formatting we moved to string Templates
        pattern = re.compile("\%\(([a-zA-Z]*)\)s")
        for provider in available:
            rendered_provider = provider.copy()
            url_tmpl = provider.get('url', '').strip()
            logo = provider.get('logo', '')
            if not url_tmpl or not logo:
                # A provider must have a logo and a share URL
                logger.error('Provider %s has not URL or logo specified', provider['id'])
                continue
            url_tmpl = re.sub(pattern, r'${\1}', url_tmpl)
            rendered_provider['url'] = Template(url_tmpl).safe_substitute(param)

            resource_name = provider.get('resource', 'sb_images')
            logo = provider.get('logo', '')
            rendered_provider['icon_url'] = '%s/++resource++%s/%s' % (
                portal_url,
                resource_name,
                logo
            )
            providers.append(rendered_provider)
        return providers

    @property
    def icons_only(self):
        """Flag whether to show icons only.
        """
        return self.settings().show_icons_only or False

    @property
    def action_enabled(self):
        """Validates if social bookmarks should be enabled
        for this context using an action.
        """
        return self.settings().use_as_action or False

    @property
    def enabled(self):
        """Validates if social bookmarks should be enabled
        for this context.
        """
        context = aq_inner(self.context)
        enabled_portal_types = self.settings().enabled_portal_types or []
        return context.portal_type in enabled_portal_types


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

    def update(self):
        pass

    def render(self):
        return self.template(self)


class SocialBookmarksView(BrowserView, SocialBookmarksBase):
    """Social Bookmarks View
    """


class SocialBookmarksViewlet(ViewletBase, SocialBookmarksBase):
    """Social Bookmarks Viewlet
    """
    template = ViewPageTemplateFile('templates/bookmarks_viewlet.pt')

    def render(self):
        return self.template(self)
