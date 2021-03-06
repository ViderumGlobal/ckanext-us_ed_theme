from ckan import plugins
from ckan.tests import helpers as test_helpers
from ckanext.us_ed_theme import helpers
from ckan.tests import factories
from ckan.lib.search import rebuild


class HelpersBase(object):
    def setup(self):
        test_helpers.reset_db()

        rebuild()

        if not plugins.plugin_loaded('us_ed_theme'):
            plugins.load('us_ed_theme')

    @classmethod
    def teardown_class(self):

        if plugins.plugin_loaded('us_ed_theme'):
            plugins.unload('us_ed_theme')


class TestHelpers(HelpersBase, test_helpers.FunctionalTestBase):
    def test_get_recently_updated_datasets(self):
        factories.Dataset()
        factories.Dataset()
        factories.Dataset()
        dataset = factories.Dataset()

        result = helpers.get_recently_updated_datasets()

        assert len(result) == 4
        assert result[0]['id'] == dataset['id']

        result = helpers.get_recently_updated_datasets(limit=2)

        assert len(result) == 2
        assert result[0]['id'] == dataset['id']

    def test_get_groups(self):
        group1 = factories.Group()
        result = helpers.get_groups()

        assert len(result) == 1

        factories.Group()
        factories.Group()
        factories.Group()

        result = helpers.get_groups()

        assert result[0]['id'] == group1['id']
        assert len(result) == 4
