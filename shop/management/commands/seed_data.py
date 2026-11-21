from django.core.management.base import BaseCommand
from django.utils.text import slugify
from shop.models import Category, Product


class Command(BaseCommand):
    help = "Seed the database with sample categories and products."

    def handle(self, *args, **options):
        categories = ['Electronics', 'Clothing', 'Books', 'Home & Kitchen']
        cat_objs = {}
        for name in categories:
            cat, _ = Category.objects.get_or_create(name=name, slug=slugify(name))
            cat_objs[name] = cat

        products = [
            ('Wireless Headphones', 'Electronics', 1499.00, 25,
             'Over-ear wireless headphones with noise cancellation.'),
            ('Smartphone Stand', 'Electronics', 199.00, 100,
             'Adjustable aluminum stand for phones and tablets.'),
            ('Cotton T-Shirt', 'Clothing', 249.00, 60,
             'Soft 100% cotton t-shirt, available in multiple colors.'),
            ('Denim Jacket', 'Clothing', 899.00, 15,
             'Classic denim jacket, unisex fit.'),
            ('Django for Beginners', 'Books', 350.00, 40,
             'A practical introduction to building web apps with Django.'),
            ('Clean Code', 'Books', 420.00, 20,
             'A handbook of agile software craftsmanship.'),
            ('Non-stick Frying Pan', 'Home & Kitchen', 599.00, 30,
             '28cm non-stick frying pan, dishwasher safe.'),
            ('Electric Kettle', 'Home & Kitchen', 749.00, 0,
             '1.7L electric kettle with auto shut-off.'),
        ]

        for title, cat_name, price, stock, description in products:
            Product.objects.get_or_create(
                title=title,
                slug=slugify(title),
                defaults={
                    'category': cat_objs[cat_name],
                    'price': price,
                    'stock': stock,
                    'description': description,
                    'is_active': True,
                }
            )

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(categories)} categories and {len(products)} products."
        ))
