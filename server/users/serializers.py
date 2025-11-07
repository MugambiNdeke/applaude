from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

# Import the custom User model defined in users/models.py
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving user data.
    """
    # Includes a nested field to show subscription status directly
    runs_remaining = serializers.SerializerMethodField()
    plan = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'github_username', 'runs_remaining', 'plan')
        read_only_fields = ('email', 'github_username',)

    def get_runs_remaining(self, user):
        """Fetches the runs_remaining from the Subscription model."""
        try:
            return user.subscription.runs_remaining
        except:
            return 0
            
    def get_plan(self, user):
        """Fetches the active plan name from the Subscription model."""
        try:
            return user.subscription.get_plan_display()
        except:
            return "None"


class UserCreateSerializer(BaseUserCreateSerializer):
    """
    Serializer for creating a new user (via email/password fallback, or just for structure).
    We inherit from Djoser's base serializer.
    """
    class Meta(BaseUserCreateSerializer.Meta):
        # We enforce email usage and do not require the GitHub fields during creation
        fields = ('id', 'email', 'password')
