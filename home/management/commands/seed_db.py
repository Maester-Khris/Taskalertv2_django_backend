from django.core.management.base import BaseCommand
from taskmanager.models import Task, Item
from usermanager.models import User 
from datetime import datetime


class Command(BaseCommand):
    help = 'Taskalert database seeding with initial data'

    def handle(self, *args, **kwargs):
        # Create users
        users = [
            User(name='Alice').save(),
            User(name='Bob').save(),
            User(name='Charlie').save()
        ]

        # Create items
        items = [
            Item(name='Item 1').save(),
            Item(name='Item 2').save(),
            Item(name='Item 3').save(),
            Item(name='Item 4').save()
        ]

        # Create tasks
        tasks = [
            Task(
                title='Task 1',
                group='Group A',
                description='This is the first task.',
                items=[items[0], items[1]],
                editors=[users[0], users[1]]
            ).save(),
            Task(
                title='Task 2',
                group='Group B',
                description='This is the second task.',
                items=[items[2], items[3]],
                editors=[users[1], users[2]]
            ).save(),
            Task(
                title='Task 3',
                group='Group A',
                description='This is the third task.',
                items=[],
                editors=[users[0], users[2]]
            ).save()
        ]

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))