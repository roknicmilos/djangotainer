import factory
from factory.django import DjangoModelFactory
from faker import Faker

from apps.emails.models import EmailThread

faker = Faker()


class EmailThreadFactory(DjangoModelFactory):
    class Meta:
        model = EmailThread

    subject = factory.LazyAttribute(lambda _: "Email subject")
    recipient = factory.LazyAttribute(lambda _: faker.email())
    context = factory.LazyAttribute(lambda _: {"first_name": faker.first_name()})
    template_path = "example_email.html"
