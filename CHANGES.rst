Changelog
=========

1.3dev (unreleased)
-------------------

- Remove old upgrade steps.
  [wesleybl]

- Add support to Python 3.6, 3.7 and 3.8.
  [wesleybl]

- Drop support to Plone 4.
  [wesleybl]

- Add support to Plone 5.2.
  [wesleybl]

- Refactor tests to use plone.app.testing
  [ericof]

- Support Travis-Ci
  [ericof]

- Use plone.registry instead portal_properties.
  [thet]

- Add bookmark titles to the <a> element instead of the <img>.
  [thet]

- Sort the bookmarks provider list alphabetically.
  [thet]

- Remove version.txt and define it just in setup.py.
  [thet]

- PEP8 and PyFlakes compliancy
  [ericof]


1.2.3 (2012-06-12)
^^^^^^^^^^^^^^^^^^^^

    * Add a MANIFEST.in file [ericof]


1.2.2 (2012-06-11)
^^^^^^^^^^^^^^^^^^^^

    * Add sb_portlet module for 1.1 backwards compatibility.
      [thet]

    * Conditionally include permission.cfg [ericof]


1.2.1 (2011-06-27)
^^^^^^^^^^^^^^^^^^^^

    * Adding buildout configs to test sc.social.bookmarks
      [ericof]

    * Fixing Zope API change: IVocabularyFactory now in zope.schema.interfaces.
      [ericof]


1.2 (2011-06-13)
^^^^^^^^^^^^^^^^^^^^

    * Base bookmarks rendering with content provider instead of macro.
      [rnix]

    * Cleanup JS
      [rnix]

    * Add "Show Icons Only" Property to control panel and integrate into views
      [rnix]

    * German Translation
      [rnix]

    * Plone 4.1 compatibility.
      [thet]

    * Add all dependencies to setup.py.
      [thet]

    * Zope API change: IVocabularyFactory now in zope.schema.interfaces.
      [thet]

    * Add migration step.
      [thet]

    * More cleanup.
      [thet]


1.1 (2011-01-21)
^^^^^^^^^^^^^^^^^^^^

    * Add portlet for social bookmarks. [thet]
    * Removed KSS dependency and replace functionality with jQuery. [thet]
    * Created a bookmarks view and assigned it as href for the bookmarks-action.
      This makes it more accessible. [thet]
    * Code cleanup & refactoring. [thet]
    * change on version number [hvelarde]
    * entry_points to z3c.autoinclude.plugin; there's no need for a ZCML slug now [hvelarde]
    * fixing MessageFactory [hvelarde]
    * adding icon_expr to controlpanel.xml as required in Plone 4 [hvelarde]
    * adding some basic tests [hvelarde]
    * aesthetic changes on xml files [hvelarde]


1.0 (2009-12-04)
^^^^^^^^^^^^^^^^^^^^

    * Fix order of providers [lucmult]
    * Improve styles [tamosauskas]


0.9 (2009-08-15)
^^^^^^^^^^^^^^^^^^^^

    * Moves code to svn.plone.org/svn/collective/sc.social.bookmarks/
      [ericof]


0.8 (2009-05-18)
^^^^^^^^^^^^^^^^^^^^

    * Fixes an annoying issue with dancing divs
      [tamosauskas]


0.7 (2009-04-15)
^^^^^^^^^^^^^^^^^^^^

    * Fixes string formatting error in providers without all parameters mapped
      [ericof]
    * Adds a condition to avoid displaying bookmark action on content types not
      configured to enabled it
      [ericof]


0.6 (2009-04-07)
^^^^^^^^^^^^^^^^^^^^

    * Support for ordering selected providers
      [ericof]
    * Improvement on Control Panel usability, using new widgets
      [ericof]
    * Adds myspace icon
      [tamosauskas]


0.5 (2009-02-27)
^^^^^^^^^^^^^^^^^^^^

    * Initial Public Release to PyPi and Plone.org
      [ericof]
    * Very basic i18n support
      [ericof]
    * Styling and css
      [tamosauskas]
    * KSS-enabled document action
      [tamosauskas]
    * Filtering of content types
      [ericof]
    * Support for a fixed set of bookmarks providers
      [ericof]
    * Initial release
