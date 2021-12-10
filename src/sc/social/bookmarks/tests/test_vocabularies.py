# -*- coding: utf-8 -*-

from plone.testing import layered
from sc.social.bookmarks.testing import INTEGRATION_TESTING

import doctest
import unittest2 as unittest


optionflags = (
    doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(
        [
            layered(
                doctest.DocTestSuite(
                    "sc.social.bookmarks.vocabularies", optionflags=optionflags
                ),
                layer=INTEGRATION_TESTING,
            ),
        ]
    )
    return suite
