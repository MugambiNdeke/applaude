import httpx
from django.conf import settings
import json

class Claude4Client:
    """
    A dedicated client for interacting with the Anthropic Claude Sonnet 4.0 API.
    Handles prompt construction and API calls.
    """
    
    API_URL = "https://api.anthropic.com/v1/messages"
    # Using the latest Claude model which is often 'claude-3-sonnet' (or higher)
    MODEL = "claude-3-sonnet" 

    def __init__(self):
        # Ensure the API key is set in the environment 
        if not hasattr(settings, 'CLAUDE_API_KEY') or not settings.CLAUDE_API_KEY:
            raise ValueError("CLAUDE_API_KEY is not configured in settings.")
        
        self.headers = {
            "x-api-key": settings.CLAUDE_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        self.client = httpx.Client(headers=self.headers, timeout=180.0) # Set a long timeout for complex tasks

    def call_api(self, system_prompt, user_prompt, max_tokens=3000):
        """
        Generic function to send a prompt to the Claude API.
        Returns the text response or raises an exception.
        """
        payload = {
            "model": self.MODEL,
            "max_tokens": max_tokens,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}]
        }

        try:
            print(f"--- Calling Claude API with System Prompt: {system_prompt[:50]}...")
            response = self.client.post(self.API_URL, json=payload)
            response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
            
            data = response.json()
            
            # Extract content from the Anthropic response structure
            if data and data.get('content'):
                return data['content'][0]['text']
            
            return "API response format error: Content missing."
            
        except httpx.RequestError as e:
            raise ConnectionError(f"Error connecting to Anthropic API: {e}")
        except Exception as e:
            raise Exception(f"General Claude API Error: {e}")

    # --- Agent-Specific Methods ---

    def generate_test_plan(self, file_structure_summary, requirements_file):
        """Agent 1: Generates the comprehensive test suite[cite: 9, 30, 32]."""
        system_prompt = (
            "You are the Testing Agent (The Planner). You are an expert in React/Django/PostgreSQL development. "
            "Your goal is to generate a comprehensive Playwright/Pytest suite based on the codebase analysis. "
            "You must return ONLY the raw code for the test files (e.g., tests.js and conftest.py). "
            "Focus on high-value paths like authentication and checkout."
        )
        user_prompt = (
            f"Here is the analyzed file structure and dependency list:\n\n"
            f"File Structure: {file_structure_summary}\n"
            f"Requirements: {requirements_file}\n\n"
            "Generate the necessary test scripts to achieve full coverage."
        )
        # Max tokens higher for test generation
        return self.call_api(system_prompt, user_prompt, max_tokens=4096) 
    
    def generate_diff_fix(self, error_log, failed_file_content):
        """Agent 2: Generates the code fix/diff[cite: 10, 36, 135]."""
        system_prompt = (
            "You are the Debugging Agent (The Fixer). You are an expert Django developer (or React developer, based on the file type). "
            "You must analyze the error log and the code, then provide ONLY the corrected file content. "
            "Your output must be the complete, corrected version of the file, ready for direct saving and verification."
        )
        user_prompt = (
            f"A test failed with this log:\n\n{error_log}\n\n"
            f"Here is the code for the failing file (Find the bug and fix it):\n\n{failed_file_content}\n\n"
            "Provide the entire, corrected code for this file."
        )
        return self.call_api(system_prompt, user_prompt, max_tokens=2048)

    def generate_report(self, run_logs):
        """Agent 3: Generates the 2-3 page summary and PR description[cite: 11, 39, 141]."""
        system_prompt = (
            "You are the Reporting Agent (The Scribe). Summarize the technical logs and diffs into a 2-page, "
            "professional, and compelling PDF summary and a technical Pull Request description."
        )
        user_prompt = (
            f"Here are the complete logs, failed tests, and applied diffs:\n\n{run_logs}\n\n"
            "Generate the full report and PR description."
        )
        return self.call_api(system_prompt, user_prompt, max_tokens=3000)
