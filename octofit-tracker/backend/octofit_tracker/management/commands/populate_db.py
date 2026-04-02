from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
from djongo import models

from octofit_tracker import models as app_models

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Delete all data
        User.objects.all().delete()
        app_models.Team.objects.all().delete()
        app_models.Activity.objects.all().delete()
        app_models.Leaderboard.objects.all().delete()
        app_models.Workout.objects.all().delete()

        # Create Teams
        marvel = app_models.Team.objects.create(name='Team Marvel')
        dc = app_models.Team.objects.create(name='Team DC')

        # Create Users
        tony = User.objects.create_user(username='ironman', email='tony@marvel.com', password='pass', first_name='Tony', last_name='Stark', team=marvel)
        steve = User.objects.create_user(username='cap', email='steve@marvel.com', password='pass', first_name='Steve', last_name='Rogers', team=marvel)
        bruce = User.objects.create_user(username='hulk', email='bruce@marvel.com', password='pass', first_name='Bruce', last_name='Banner', team=marvel)
        clark = User.objects.create_user(username='superman', email='clark@dc.com', password='pass', first_name='Clark', last_name='Kent', team=dc)
        bruce_dc = User.objects.create_user(username='batman', email='bruce@dc.com', password='pass', first_name='Bruce', last_name='Wayne', team=dc)

        # Create Activities
        app_models.Activity.objects.create(user=tony, type='Run', duration=30, distance=5)
        app_models.Activity.objects.create(user=steve, type='Swim', duration=45, distance=2)
        app_models.Activity.objects.create(user=clark, type='Fly', duration=60, distance=100)

        # Create Workouts
        app_models.Workout.objects.create(name='Morning Cardio', description='Cardio for all heroes', duration=40)
        app_models.Workout.objects.create(name='Strength Training', description='Strength for all heroes', duration=60)

        # Create Leaderboard
        app_models.Leaderboard.objects.create(user=tony, score=100)
        app_models.Leaderboard.objects.create(user=clark, score=120)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
