# -*- coding: utf-8 -*-
from Testing import ZopeTestCase as ztc
from unittest import TestSuite
from z3c.table.testing import setUp
from z3c.table.testing import tearDown

import doctest


optionflags = (
    doctest.REPORT_ONLY_FIRST_FAILURE |  # doctest.REPORT_UDIFF |
    doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
)


def test_suite():
    return TestSuite([
        ztc.FunctionalDocFileSuite(
            'provider.txt', package='plone.z3ctable.tests',
            setUp=setUp, tearDown=tearDown, optionflags=optionflags),
    ])
