import logging
from Products.CMFCore.utils import getToolByName

logger = logging.getLogger("sc.social.bookmarks")

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
