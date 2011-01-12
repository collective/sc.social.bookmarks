# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

class SocialBookmarks(BrowserView):
    
    def __init__(self, context, request,*args,**kwargs):
        super(SocialBookmarks, self).__init__(context, request,*args,**kwargs)
        context = aq_inner(context)
        self.context = context
        pp = getToolByName(context,'portal_properties')
        self.enabled_portal_types = pp.sc_social_bookmarks_properties.getProperty("enabled_portal_types") or []
    
    @property
    def enabled(self):
        """Validates if social bookmarks should be enabled 
           for this context"""
        context = self.context
        enabled_portal_types = self.enabled_portal_types
        return context.portal_type in enabled_portal_types