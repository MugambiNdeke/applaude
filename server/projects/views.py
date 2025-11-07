from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Project, TestRun
from .serializers import ProjectSerializer, TestRunSerializer, StartRunSerializer
from worker.tasks import run_autonomous_test # Import the Celery task

class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects (GitHub repos) to be viewed or edited.
    """
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        # Only show projects belonging to the authenticated user
        return Project.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user on project creation
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='run')
    def start_run(self, request, pk=None):
        """
        Endpoint to start an autonomous test run for a specific project.
        Core logic: Check subscription -> Decrement run count -> Trigger Celery task.
        """
        project = self.get_object()
        user_subscription = getattr(request.user, 'subscription', None)

        # 1. Check Subscription and Remaining Runs [cite: 114]
        if not user_subscription or user_subscription.runs_remaining <= 0:
            return Response(
                {"detail": "No runs remaining. Please upgrade your subscription."},
                status=status.HTTP_402_PAYMENT_REQUIRED
            )

        # Validate the run type input
        serializer = StartRunSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        run_type = serializer.validated_data['run_type']
        
        # 2. Decrement runs_remaining [cite: 115]
        user_subscription.runs_remaining -= 1
        user_subscription.save(update_fields=['runs_remaining'])
        
        # 3. Create a new TestRun object (status='Queued') 
        test_run = TestRun.objects.create(
            project=project,
            status='QUEUED',
            run_type=run_type
        )
        
        # 4. Triggers the asynchronous Celery task [cite: 117]
        task = run_autonomous_test.delay(run_id=str(test_run.id))
        
        # Save the Celery task ID for status polling
        test_run.celery_task_id = task.id
        test_run.save(update_fields=['celery_task_id'])
        
        # 5. Immediately returns a 202 Accepted response [cite: 118]
        return Response(
            {"detail": "Autonomous run started.", 
             "run_id": str(test_run.id),
             "runs_remaining": user_subscription.runs_remaining},
            status=status.HTTP_202_ACCEPTED
        )

class TestRunViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing the user's past and current TestRuns.
    """
    serializer_class = TestRunSerializer
    
    def get_queryset(self):
        # Only show runs for projects owned by the authenticated user
        return TestRun.objects.filter(project__user=self.request.user).select_related('project')
    
    @action(detail=True, methods=['get'], url_path='status')
    def status(self, request, pk=None):
        """
        Polling endpoint to check the current status of a single run[cite: 148].
        """
        test_run = get_object_or_404(TestRun, id=pk, project__user=request.user)
        return Response(TestRunSerializer(test_run).data)
