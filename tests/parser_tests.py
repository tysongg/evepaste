from evepaste import parse
from evepaste.testing.tables.cargo_scan import CARGO_SCAN_TABLE
from evepaste.testing.tables.fitting import FITTING_TABLE
from evepaste.testing.tables.eft import EFT_TABLE
from evepaste.testing.tables.dscan import DSCAN_TABLE
from evepaste.testing.tables.loot_history import LOOT_HISTORY_TABLE
from evepaste.testing.tables.contract import CONTRACT_TABLE
from evepaste.testing.tables.assets import ASSET_TABLE
from evepaste.testing.tables.bill_of_materials import BOM_TABLE
from evepaste.testing.tables.parse import PARSE_TABLE

import inspect
import unittest


class TableChecker(unittest.TestCase):
    """ This actually runs one named table test """
    def __init__(self, funct, name):
        unittest.TestCase.__init__(self, '__call__')
        self.funct = funct
        self.description = name

    def __call__(self, input_str, expected):
        if inspect.isclass(expected) and issubclass(expected, Exception):
            self.assertRaises(expected, self.funct, input_str)
        else:
            result = self.funct(input_str)
            self.assertEqual(result, expected)


def test_generator():
    # Perform each table test with their associated callable
    for table in [CARGO_SCAN_TABLE,
                  FITTING_TABLE,
                  EFT_TABLE,
                  DSCAN_TABLE,
                  LOOT_HISTORY_TABLE,
                  CONTRACT_TABLE,
                  ASSET_TABLE,
                  BOM_TABLE,
                  PARSE_TABLE]:
        for i, (input_str, expected) in enumerate(table.tests):
            name = ('test_%s[%s]' % (str(table.funct.__name__), i))
            checker = TableChecker(table.funct, name)
            yield checker, input_str, expected

    # Perform each table test with parse() instead of the associated callable
    for table in [CARGO_SCAN_TABLE,
                  FITTING_TABLE,
                  EFT_TABLE,
                  DSCAN_TABLE,
                  LOOT_HISTORY_TABLE,
                  CONTRACT_TABLE,
                  ASSET_TABLE,
                  BOM_TABLE]:
        for i, (input_str, expected) in enumerate(table.tests):
            if isinstance(expected, tuple) and not expected[1]:
                name = ('test_parse(%s)[%s]' % (str(table.funct.__name__), i))
                checker = TableChecker(parse, name)
                result, bad_lines = expected
                _type = table.funct.__name__.split('_', 1)[1]
                yield checker, input_str, {'type': _type,
                                           'result': result,
                                           'bad_lines': bad_lines}
