#!/bin/bash
# kudos to Products.Ploneboard for the base for this file
# ensure that when something is wrong, nothing is broken more than it should...
set -e

BASEDIR=src/sc/social/bookmarks
LOCALES=$BASEDIR/locales

# first, create some pot containing anything
i18ndude rebuild-pot --pot $LOCALES/sc.social.bookmarks.pot --create sc.social.bookmarks --merge $LOCALES/manual.pot $BASEDIR

# finally, update the po files
i18ndude sync --pot $LOCALES/sc.social.bookmarks.pot  `find . -iregex '.*sc.social.bookmarks\.po$'|grep -v plone`

