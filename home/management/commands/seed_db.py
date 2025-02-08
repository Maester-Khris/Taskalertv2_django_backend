import json, os
from pathlib import Path
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
        print("=========== Creating new records =======")
        # # Create users
        # users = [
        #     User(name='Alice').save(),
        #     User(name='Bob').save(),
        #     User(name='Charlie').save()
        # ]

        # # Create tasks
        # tasks = [
        #     Task(
        #         title='Task 1',
        #         group=['Group A'],
        #         description='This is the first task.',
        #         items=["Holla", "Senior fall"],
        #         editors=[users[0], users[1]]
        #     ).save(),
        #     Task(
        #         title='Task 2',
        #         group=['Group B'],
        #         description='This is the second task.',
        #         items=[],
        #         editors=[users[1], users[2]]
        #     ).save(),
        #     Task(
        #         title='Task 3',
        #         group=['Group A'],
        #         description='This is the third task.',
        #         items=["Dev test", "Splunk test", "Load test"],
        #         editors=[users[0], users[2]]
        #     ).save()
        # ]
        base_dir = Path(__file__).resolve().parent.parent
        file_path = os.path.join(base_dir, 'data', 'seed_data.json')

        # Read the JSON data from the file
        with open(file_path, 'r') as file:
            seed_data = json.load(file)

        # Create users from the JSON data
        users = {}
        for user_data in seed_data['users']:
            user = User(name=user_data['name']).save()
            users[user_data['name']] = user 
        print(users)

        # Create tasks from the JSON data
        for task_data in seed_data['tasks']:
            task = Task(
                title=task_data['title'],
                group=task_data['group'],
                description=task_data['description'],
                items=task_data['items'],
                editors=[users[editor] for editor in task_data['editors']]
            ).save()
        

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))