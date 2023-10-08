from django.db import models

from apps.common.models import BaseModel
from apps.common.tests import TestCase


class TestBaseModel(TestCase):
    class ConcreteBaseModel(BaseModel):
        """
        This model will be migrated to the temporary tests
        database(s) even though it has no migration files.
        Model migration will FAIL if the app has migrations
        (module "migrations")!
        """

        first_name = models.CharField(
            max_length=100,
            default="Jon"
        )

        class Meta:
            app_label = "common"
            verbose_name = "Test Model"
            verbose_name_plural = "Test Models"

    def test_should_have_correct_verbose_name(self):
        model_instance = self.ConcreteBaseModel()
        self.assertEqual(model_instance.verbose_name, "Test Model")

    def test_should_have_correct_verbose_name_plural(self):
        model_instance = self.ConcreteBaseModel()
        self.assertEqual(model_instance.verbose_name_plural, "Test Models")

    def test_should_update_field_value(self):
        model_instance = self.ConcreteBaseModel.objects.create()
        new_first_name = "Sam"
        self.assertNotEqual(model_instance.first_name, new_first_name)
        queryset = self.ConcreteBaseModel.objects.filter(first_name=new_first_name, pk=model_instance.pk)
        self.assertFalse(queryset.exists())

        model_instance.update(first_name=new_first_name)

        self.assertTrue(queryset.exists())
        self.assertEqual(model_instance.first_name, new_first_name)
