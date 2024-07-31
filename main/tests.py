# main/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import StudyGroup, StudyGoal, StudyHistory

class StudyGroupTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        self.group = StudyGroup.objects.create(
            name='Test Group',
            description='This is a test group',
            owner=self.user
        )
        self.group.members.add(self.user)

    def test_study_group_creation(self):
        self.assertEqual(self.group.name, 'Test Group')
        self.assertEqual(self.group.owner.username, 'testuser')
        self.assertIn(self.user, self.group.members.all())

class StudyGoalTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        self.goal = StudyGoal.objects.create(
            user=self.user,
            goal='Learn Django Testing',
            target_date='2024-12-31'
        )

    def test_study_goal_creation(self):
        self.assertEqual(self.goal.user.username, 'testuser')
        self.assertEqual(self.goal.goal, 'Learn Django Testing')
        self.assertFalse(self.goal.is_completed)

class StudyHistoryTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        self.group = StudyGroup.objects.create(
            name='Test Group',
            description='This is a test group',
            owner=self.user
        )
        self.history = StudyHistory.objects.create(
            user=self.user,
            group=self.group
        )

    def test_study_history_creation(self):
        self.assertEqual(self.history.user.username, 'testuser')
        self.assertEqual(self.history.group.name, 'Test Group')
        self.assertIsNotNone(self.history.completed_on)
