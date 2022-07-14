from django.core.management.base import BaseCommand
import random
from quickstart.models import User, Brand

# python manage.py seed --mode=refresh

""" Clear all data and creates users and brands """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    print("Delete users instances")
    User.objects.all().delete()
    print("Delete brand instances")
    Brand.objects.all().delete()


def create_users():
    """Creates a user object combining different elements from the list"""
    print("Creating users")
    names = ['John', 'Jane', 'Jack', 'Jill']
    emails = ['john@example.com', 'jane@example.com',
              'jill@example.com', 'jack@gmail.com']

    for i in range(len(names)):
        user = User(name=names[i], email=emails[i])
        user.save()
        print("{} user with mail:{} created.".format(
            user.name, user.email))


def create_brands():
    """Creates a brand object combining different elements from the list"""
    print("Creating brands")
    brands = ['Apple', 'Samsung', 'Xiaomi', 'OnePlus']

    for i in range(len(brands)):
        brand = Brand(name=brands[i])
        brand.save()
        print("{} brand created.".format(brand.name))


def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    # Creating 5 users and brands
    create_users()
    create_brands()
