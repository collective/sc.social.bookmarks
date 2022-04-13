# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

import logging


logger = logging.getLogger("sc.social.bookmarks")

profile_id = "sc.social.bookmarks:default"


def removeConfiglets(context):
    """Remove configlets from the portal control panel"""
    configlet = "socialbookmarks"
    controlpanel = getToolByName(context, "portal_controlpanel", None)
    if controlpanel:
        controlpanel.unregisterConfiglet(configlet)
        logger.log(logging.INFO, "Unregistered configlet {0}\n".format(configlet))


def uninstall(context):
    """Do customized uninstallation"""
    if context.readDataFile("sc.social.bookmarks_uninstall.txt") is None:
        return
    logger.log(logging.INFO, "Doing customized uninstallation.")
    site = context.getSite()
    removeConfiglets(site)
    logger.log(logging.INFO, "Customized uninstallation done.")
