import unittest

import sys

from freshen.noseplugin import FreshenNosePlugin
from optparse import OptionParser
from os.path import abspath, dirname, join

class TestFreshenTestCaseName(unittest.TestCase):

    def __init__(self, method_name='runTest'):
        unittest.TestCase.__init__(self, method_name)
        self.cur_dir = dirname(abspath(__file__))

    def test_should_use_feature_name_as_class_name_when_subclassing_FreshenTestCase(self):
        plugin = self.__make_plugin()
        test_generator = plugin.loadTestsFromFile(self.__resource('valid_no_tags_no_use_only'))
        test_instance = test_generator.next()

        self.assertEquals(test_instance.__class__.__name__, 'Independence of the counter.')

    def test_should_use_scenario_name_as_method_name_when_subclassing_FreshenTestCase(self):
        plugin = self.__make_plugin()
        test_generator = plugin.loadTestsFromFile(self.__resource('valid_no_tags_no_use_only'))
        test_instance = test_generator.next()

        self.assert_(getattr(test_instance, 'Print counter', None) is not None)

    def __make_plugin(self):
        plugin = FreshenNosePlugin()
        parser = OptionParser()

        plugin.options(parser, {})

        sys.argv = ['nosetests', '--with-freshen']
        (options, args) = parser.parse_args()

        plugin.configure(options, None)
        return plugin

    def __resource(self, feature_file):
        return join(self.cur_dir, 'resources/%s.feature' % feature_file)
