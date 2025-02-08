from django.core.management.base import BaseCommand
from taskapi.models import Task
from userapi.models import User 
from datetime import datetime


class Command(BaseCommand):
    help = 'Taskalert database seeding with initial data'
    print("=========== Clean existing records =======")
    Task.objects.delete()
    User.objects.delete()

    def handle(self, *args, **kwargs):
        # Create users
        users = [
            User(name='Alice').save(),
            User(name='Bob').save(),
            User(name='Charlie').save()
        ]

        

        # Create tasks
        tasks = [
            Task(
                title='Task 1',
                group=['Group A'],
                description='This is the first task.',
                items=["Holla", "Senior fall"],
                editors=[users[0], users[1]]
            ).save(),
            Task(
                title='Task 2',
                group=['Group B'],
                description='This is the second task.',
                items=[],
                editors=[users[1], users[2]]
            ).save(),
            Task(
                title='Task 3',
                group=['Group A'],
                description='This is the third task.',
                items=["Dev test", "Splunk test", "Load test"],
                editors=[users[0], users[2]]
            ).save()
        ]

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))