# -*- coding: utf-8 -*-
import logging

from zope.component import getUtility

from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName

from sc.social.bookmarks.controlpanel.bookmarks import IProvidersSchema


logger = logging.getLogger("sc.social.bookmarks")

profile_id = 'sc.social.bookmarks:default'


def removeConfiglets(context):
    """Remove configlets from the portal control panel"""
    configlet = "socialbookmarks"
    controlpanel = getToolByName(context, "portal_controlpanel", None)
    if controlpanel:
        controlpanel.unregisterConfiglet(configlet)
        logger.log(logging.INFO, "Unregistered configlet %s\n" % configlet)


def uninstall(context):
    """Do customized uninstallation"""
    if context.readDataFile("sc.social.bookmarks_uninstall.txt") is None:
        return
    logger.log(logging.INFO, "Doing customized uninstallation.")
    site = context.getSite()
    removeConfiglets(site)
    logger.log(logging.INFO, "Customized uninstallation done.")


def upgrade_1_to_2(context):
    context.runAllImportStepsFromProfile('profile-sc.social.bookmarks:default')
    # This way we will be able to run other steps
    context.setLastVersionForProfile(profile_id, u'2')


def upgrade_2_to_3(context):
    # First, make sure, the profile is applied to prepare the registry
    context.runAllImportStepsFromProfile('profile-sc.social.bookmarks:default')

    registry = getUtility(IRegistry)
    controlpanel = registry.forInterface(IProvidersSchema,
                                         prefix="sc.social.bookmarks")

    props = getToolByName(context, 'portal_properties')
    sheet = getattr(props, 'sc_social_bookmarks_properties', None)

    # Then migrate individual settings
    if sheet:
        action_enabled = sheet.getProperty("action_enabled")
        controlpanel.action_enabled = action_enabled
        logger.info(u"Setting action_enabled migrated to plone.registry.")

        bookmark_providers = sheet.getProperty("bookmark_providers")
        controlpanel.bookmark_providers = bookmark_providers
        logger.info(u"Setting bookmark_providers migrated to plone.registry.")

        enabled_portal_types = sheet.getProperty("enabled_portal_types")
        controlpanel.enabled_portal_types = enabled_portal_types
        logger.info(u"""Setting enabled_portal_types migrated
                        to plone.registry.""")

        show_icons_only = sheet.getProperty("show_icons_only")
        controlpanel.show_icons_only = show_icons_only
        logger.info(u"Setting show_icons_only migrated to plone.registry.")

        sheet.manage_delObjects('sc_social_bookmarks_properties')
        logger.info(u"Deleted property sheet.")
    # This way we will be able to run other steps
    context.setLastVersionForProfile(profile_id, u'3')
