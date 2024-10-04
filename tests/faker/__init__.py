import faker.providers

from tests.faker.fake_provider import UserProvider

fake = faker.Faker()

fake.add_provider(UserProvider)
