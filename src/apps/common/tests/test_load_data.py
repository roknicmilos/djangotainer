from unittest.mock import patch

from django.conf import settings
from django.core.management import BaseCommand, call_command
from django.db import models
from django.test import override_settings

from apps.common.management.commands.load_data import Command as LoadDataCommand
from apps.common.models import BaseModel
from apps.common.tests import TestCase


@override_settings(FIXTURES=())
class TestLoadData(TestCase):
    class FixtureTestModel(BaseModel):
        """
        This model will be migrated to the temporary tests
        database(s) even though it has no migration files.
        Model migration will FAIL if the app has migrations
        (module "migrations").
        """

        name = models.CharField(max_length=100, default="")

        class Meta:
            app_label = "common"

    def test_should_not_add_default_fixture_names_when_some_provided(self):
        argv = ["-f", "--second-flag", "--third-flag", "fixture_name"]
        prepared_argv = LoadDataCommand.prepare_argv(argv=argv)
        self.assertEqual(prepared_argv, argv)

    def test_should_add_default_fixture_names_when_none_provided(self):
        argv = ["-f", "--second-flag", "--third-flag"]
        actual_prepared_argv = LoadDataCommand.prepare_argv(argv=argv)
        expected_prepared_argv = ["-f", "--second-flag", *settings.FIXTURES, "--third-flag"]
        self.assertEqual(actual_prepared_argv, expected_prepared_argv)

    def test_should_not_raise_any_error_when_default_fixtures_are_not_declared(self):
        original_settings_fixtures = settings.FIXTURES
        del settings.FIXTURES
        argv = ["-f", "--second-flag", "--third-flag"]
        prepared_argv = LoadDataCommand.prepare_argv(argv=argv)
        self.assertEqual(prepared_argv, argv)
        settings.FIXTURES = original_settings_fixtures

    @patch.object(LoadDataCommand, "prepare_argv")
    @patch.object(BaseCommand, "run_from_argv")
    def test_should_call_prepare_argv_function(self, _, mock_prepare_argv):
        command = LoadDataCommand()
        argv = [
            "-f",
            "--second-flag",
        ]
        command.run_from_argv(argv=argv)
        mock_prepare_argv.assert_called_once_with(argv=argv)

    @override_settings(FIXTURES=("example",))
    def test_should_load_fixtures(self):
        prepared_argv = LoadDataCommand.prepare_argv(argv=[])
        call_command("load_data", *prepared_argv)
