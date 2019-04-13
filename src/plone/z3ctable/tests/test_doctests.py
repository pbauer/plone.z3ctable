# -*- coding: utf-8 -*-
from Testing import ZopeTestCase as ztc
from unittest import TestSuite
from z3c.table.testing import setUp
from z3c.table.testing import tearDown

import doctest
import six
import re

optionflags = (
    doctest.REPORT_ONLY_FIRST_FAILURE |  # doctest.REPORT_UDIFF |
    doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
)


class Py23DocChecker(doctest.OutputChecker):
    def check_output(self, want, got, optionflags):
        if six.PY2:
            got = re.sub("u'(.*?)'", "'\\1'", got)
        return doctest.OutputChecker.check_output(self, want, got, optionflags)


def test_suite():
    return TestSuite([
        ztc.FunctionalDocFileSuite(
            'provider.txt',
            package='plone.z3ctable.tests',
            checker=Py23DocChecker(),
            setUp=setUp,
            tearDown=tearDown,
            optionflags=optionflags),
    ])
