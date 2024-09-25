from django.utils import timezone
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from authorization.models import CustomUser
from training.models import Exercise, UserDimension, UserGoal, Training
from rest_framework.authtoken.models import Token


class ExerciseViewSetTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.exercise_data = {
            'name': 'Push Up',
            'description': 'Push up exercise',
            'public': True
        }
        self.exercise = Exercise.objects.create(user=self.user, **self.exercise_data)

    def test_create_exercise(self):
        url = reverse('exercise-list')  # Assuming you have set proper URLs
        response = self.client.post(url, self.exercise_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_user_exercises(self):
        url = reverse('exercise-get-user-exercises')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Push Up')


class UserDimensionViewSetTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.dimension_data = {
            'weight': 80,
            'growth': 180,
            'left_biceps': 40,
        }
        self.user_dimension = UserDimension.objects.create(user=self.user, **self.dimension_data)

    def test_create_user_dimension(self):
        url = reverse('userdimension-list')
        response = self.client.post(url, self.dimension_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_user_dimensions(self):
        url = reverse('userdimension-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['weight'], 80)



class UserGoalViewSetTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.goal_data = {
            'goal': 'Lose Weight',
            'completed': False,
            'finish_date': timezone.now().date()
        }
        self.user_goal = UserGoal.objects.create(user=self.user, **self.goal_data)

    def test_create_user_goal(self):
        url = reverse('usergoal-list')
        response = self.client.post(url, self.goal_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_not_completed_goals(self):
        url = reverse('usergoal-not-completed')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['goal'], 'Lose Weight')

    def test_get_completed_goals(self):
        self.user_goal.completed = True
        self.user_goal.save()

        url = reverse('usergoal-completed')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['goal'], 'Lose Weight')

class SingleTrainingViewSetTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.training_data = {
            'name': 'Training 1',
            'date': '2024-09-25',
        }
        self.training = Training.objects.create(user=self.user, **self.training_data)

    def test_create_training(self):
        url = reverse('training-list')
        response = self.client.post(url, self.training_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_training_by_id(self):
        url = reverse('training-get-training-by-id', args=[self.training.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Training 1')
