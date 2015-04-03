# -*- coding: utf-8 -*-

#   Copyright (c) 2010-2014, MIT Probabilistic Computing Project
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import StringIO
import pytest

import bayeslite.shell.pretty as pretty

class MockCursor(object):
    def __init__(self, description, rows):
        self.description = description
        self.rows = rows

    def __iter__(self):
        return iter(self.rows)

def test_pretty():
    cursor = MockCursor([['name'], ['age'], ['favourite food']], [
        ['Spot', 3, 'kibble'],
        ['Skruffles', 2, 'kibble'],
        ['Zorb', 2, 'zorblaxian kibble'],
        [u'Zörb', 87, u'zørblaχian ﻛبﻞ'],
    ])
    out = StringIO.StringIO()
    pretty.pp_cursor(out, cursor)
    assert out.getvalue() == \
        u'     name | age |    favourite food\n' \
        u'----------+-----+------------------\n' \
        u'     Spot |   3 |            kibble\n' \
        u'Skruffles |   2 |            kibble\n' \
        u'     Zorb |   2 | zorblaxian kibble\n' \
        u'     Zörb |  87 |    zørblaχian ﻛبﻞ\n'

def test_pretty_unicomb():
    pytest.xfail('pp_cursor counts code points, not grapheme clusters.')
    cursor = MockCursor([['name'], ['age'], ['favourite food']], [
        ['Spot', 3, 'kibble'],
        ['Skruffles', 2, 'kibble'],
        ['Zorb', 2, 'zorblaxian kibble'],
        ['Zörb', 87, 'zørblaχian ﻛبﻞ'],
        [u'Zörb', 42, u'zörblǎxïǎn kïbble'],
        ['Zörb', 87, 'zørblaχian ﻛِبّﻞ'],
    ])
    out = StringIO.StringIO()
    pretty.pp_cursor(out, cursor)
    assert out.getvalue() == \
        u'     name | age |    favourite food\n' \
        u'----------+-----+------------------\n' \
        u'     Spot |   3 |            kibble\n' \
        u'Skruffles |   2 |            kibble\n' \
        u'     Zorb |   2 | zorblaxian kibble\n' \
        u'     Zörb |  42 | zörblǎxïǎn kïbble\n' \
        u'     Zörb |  87 |    zørblaxian ﻛِبّﻞ\n'
