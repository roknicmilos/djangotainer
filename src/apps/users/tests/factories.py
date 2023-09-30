from uuid import uuid4

import factory
from factory.django import DjangoModelFactory
from faker import Faker

from apps.users.models import User

faker = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda user: f"{user.first_name}.{user.last_name}.{uuid4().hex}@example.rs")
    first_name = factory.LazyAttribute(lambda _: faker.first_name())
    last_name = factory.LazyAttribute(lambda _: faker.last_name())
