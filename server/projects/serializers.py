from rest_framework import serializers
from .models import Project, TestRun

class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Project objects (GitHub Repositories).
    """
    runs_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ('id', 'name', 'github_url', 'created_at', 'runs_count')
        read_only_fields = ('created_at', 'runs_count')
        
    def get_runs_count(self, project):
        return project.runs.count()

class TestRunSerializer(serializers.ModelSerializer):
    """
    Serializer for TestRun results, used for the dashboard display and status polling.
    """
    project_name = serializers.CharField(source='project.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = TestRun
        fields = (
            'id', 'project_name', 'status', 'status_display', 'run_type', 
            'pr_url', 'report_url', 'started_at', 'completed_at'
        )
        read_only_fields = fields


class StartRunSerializer(serializers.Serializer):
    """
    Input serializer for the start_run custom action.
    """
    RUN_TYPE_CHOICES = TestRun.TYPE_CHOICES
    
    run_type = serializers.ChoiceField(
        choices=RUN_TYPE_CHOICES,
        required=True,
        help_text="Option A: FULL_STACK, Option B: FRONTEND_ONLY"
    )
