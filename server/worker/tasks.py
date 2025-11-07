import time
import random
from celery import shared_task
from django.utils import timezone
from projects.models import TestRun
import httpx # Used as the mock Claude 4.0 client [cite: 92]
from django.conf import settings

@shared_task
def run_autonomous_test(run_id):
    """
    The main asynchronous task that executes the 3-Agent autonomous remediation process.
    """
    try:
        run = TestRun.objects.get(id=run_id)
        
        # Retrieve necessary context
        user = run.project.user
        repo_url = run.project.github_url
        user_token = user.github_access_token
        
        print(f"Starting autonomous run {run_id} for {user.email} on {repo_url}")

        # --- Phase 1: Agent 1 (Testing) [cite: 122] ---
        run.status = 'CLONING'
        run.save(update_fields=['status'])
        time.sleep(1) # Simulate cloning the repo [cite: 124]

        # Mock Claude 4.0 call for Test Plan [cite: 125]
        mock_claude_call(f"Analyze repo {repo_url} and generate Playwright test plan.")
        
        run.status = 'TESTING' # [cite: 126]
        run.save(update_fields=['status'])
        time.sleep(3) # Simulate test execution [cite: 127]
        
        # Mock result: Assume 2 bugs are found for the demonstration
        bugs_found = random.choice([0, 2, 5]) 
        
        # --- Phase 2: Agent 2 (Debugging) [cite: 129] ---
        if bugs_found > 0:
            run.status = 'DEBUGGING' # [cite: 132]
            run.save(update_fields=['status'])
            
            for i in range(bugs_found):
                print(f"--> Debugging Bug #{i+1}...")
                # Mock Claude 4.0 call for code fix [cite: 135]
                mock_claude_call(f"Fix bug on file X. Return only the diff.", is_fix=True)
                time.sleep(2) # Simulate applying diff and re-running test [cite: 136, 137]

        # --- Phase 3: Agent 3 (Reporting) [cite: 138] ---
        run.status = 'REPORTING' # [cite: 139]
        run.save(update_fields=['status'])
        
        # Mock Claude 4.0 call for PDF report summary [cite: 141]
        mock_claude_call(f"Write a 2-page summary of {bugs_found} fixes.")
        
        # --- Phase 4: Delivery [cite: 142] ---
        # Mock GitHub API interaction: Create PR [cite: 145]
        mock_pr_url = f"https://github.com/{user.github_username}/{run.project.name}/pull/1"
        mock_report_url = f"/api/v1/runs/{run_id}/report.pdf"

        run.pr_url = mock_pr_url
        run.report_url = mock_report_url
        run.status = 'COMPLETE' # [cite: 146]
        run.completed_at = timezone.now()
        run.save()
        
        print(f"Run {run_id} Complete. PR: {mock_pr_url}")

    except TestRun.DoesNotExist:
        print(f"Error: TestRun with ID {run_id} not found.")
    except Exception as e:
        # Handle errors, update status to FAILED, and log [cite: 131]
        if 'run' in locals():
            run.status = 'FAILED'
            run.save(update_fields=['status'])
        print(f"Critical error during run {run_id}: {e}")

def mock_claude_call(prompt, is_fix=False):
    """Simulates the httpx client call to the Anthropic Claude 4.0 API."""
    # This is a placeholder for the actual API call [cite: 92]
    # In production, this would use the real settings.CLAUDE_API_KEY
    if is_fix:
        # Cost per bug is low ($0.60) [cite: 69] - short, focused prompt
        tokens_used = 120_000 
    else:
        # Cost per run start is high ($21.00) [cite: 65] - large token count
        tokens_used = 3_000_000
        
    # Simulate API latency
    time.sleep(random.uniform(0.1, 0.5)) 
    print(f"  [AI Agent Call]: '{prompt[:50]}...' (Mock tokens: {tokens_used:,})")
    return {"status": "ok", "response": "Mock AI Response."}
