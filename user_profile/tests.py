from django.db.models.signals import post_save
from django.test import TestCase
from user_profile.models import UserProfile
from django.contrib.auth.models import User
from checkout.models import Order  # Import Order model
from user_profile.signals import update_user_profile  # Assuming this is your signal

class UserProfileDeletionTests(TestCase):
    def setUp(self):
        # Disable signals to prevent the automatic creation of UserProfile
        post_save.disconnect(update_user_profile, sender=User)

        # Create user and associated profile
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user)

        # Create an order linked to the user profile
        self.order = Order.objects.create(
            user_profile=self.user_profile,
            first_name="Test",
            last_name="User",
            email="test@example.com",
            phone_number="1234567890",
            address_1="123 Test Street",
            town="Test Town",
            country="GB",
        )

    def test_deleting_user_also_deletes_user_profile(self):
        # Ensure UserProfile is deleted when the user is deleted
        user_profile = self.user_profile
        self.user.delete()  # Delete the User
        
        # Check if the user profile is deleted
        with self.assertRaises(UserProfile.DoesNotExist):
            user_profile.refresh_from_db()  # This will raise an exception if the object is deleted

    def test_deleting_user_profile_sets_order_user_profile_to_null(self):
        self.user_profile.delete()  # Delete the UserProfile
        self.order.refresh_from_db()  # Refresh the order after deletion
        self.assertIsNone(self.order.user_profile)  # Ensure it's set to NULL
        self.assertEqual(Order.objects.count(), 1)  # Ensure order still exists

    def tearDown(self):
        # Re-enable the signal
        post_save.connect(update_user_profile, sender=User)
        
        # Clean up test data
        User.objects.all().delete()
        UserProfile.objects.all().delete()
        Order.objects.all().delete()
