import random
from decimal import Decimal
from faker import Faker
from django.core.management.base import BaseCommand
from articles.models import Article, Brand, Provider


class Command(BaseCommand):
    help = 'Populates the database with random articles'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='The number of articles to create')

    def handle(self, *args, **options):
        faker = Faker('es_ES')
        count = options['count']

        # Generate 10 random brands
        brands = [Brand(name=faker.company()) for _ in range(10)]
        Brand.objects.bulk_create(brands)
        brands = Brand.objects.all()

        # Generate 5 random providers
        providers = [Provider(name=faker.company()) for _ in range(5)]
        Provider.objects.bulk_create(providers)
        providers = Provider.objects.all()

        # Generate random articles in batches of 1000
        batch_size = 2000
        for i in range(0, count, batch_size):
            articles = []

            for j in range(batch_size):
                # Generate a random code and OEM code
                code = faker.numerify('V######')
                oem_code = faker.numerify('D###')

                # Generate a random description using autopart names, colors, and positions
                description = f"{faker.word()} - {faker.color_name()} {faker.word()} {faker.word()}"

                # Choose a random brand and provider for the article
                brand = random.choice(brands)
                provider = random.choice(providers)

                # Create the article with the generated data and add it to the list
                articles.append(Article(code=code, oem_code=oem_code, description=description, brand=brand, provider=provider, price=Decimal(random.uniform(1.0, 1000.0))))

            # Bulk create the articles in this batch
            Article.objects.bulk_create(articles)
            self.stdout.write(self.style.SUCCESS(f"Created {min(i+batch_size, count)} articles"))


        self.stdout.write(self.style.SUCCESS(f'{count} articles created.'))