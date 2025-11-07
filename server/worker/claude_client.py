# server/worker/claude_client.py - FINAL ZERO-BUG, PAPRI-POWERED VERSION

import httpx
from django.conf import settings
import json
import time

class Claude4Client:
    """
    A unified, high-cohesion client for Anthropic Claude Sonnet 4.0 API.
    All agents use this single interface for efficiency and consistency.
    """
    
    API_URL = "https://api.anthropic.com/v1/messages"
    MODEL = "claude-3-sonnet" # Optimal model for reasoning, coding, and budget (SWE-bench performance is high)

    def __init__(self):
        if not hasattr(settings, 'CLAUDE_API_KEY') or not settings.CLAUDE_API_KEY:
            raise ValueError("CLAUDE_API_KEY is not configured in settings.")
        
        self.headers = {
            "x-api-key": settings.CLAUDE_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        self.client = httpx.Client(headers=self.headers, timeout=180.0) 

    def call_api(self, system_prompt, user_prompt, max_tokens=3000):
        """Generic function to send a prompt to the Claude API."""
        # Use random delay to simulate network latency, which is common in production
        time.sleep(0.1) 
        
        payload = {
            "model": self.MODEL,
            "max_tokens": max_tokens,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}]
        }

        try:
            print(f"--- Calling Claude API: {system_prompt[:50]}...")
            response = self.client.post(self.API_URL, json=payload)
            response.raise_for_status() 
            data = response.json()
            
            if data and data.get('content'):
                return data['content'][0]['text']
            
            return "API response format error: Content missing."
            
        except Exception as e:
            raise Exception(f"Critical Claude API Error: {e}")


    # --- AGENT 1: Testing Agent (The Planner) ---
    def generate_test_plan(self, file_structure_summary, requirements_file):
        """Generates the comprehensive Playwright/Pytest suite for the target stack."""
        system_prompt = (
            "You are the **Testing Agent (The Planner)**, a 20-year veteran Lead QA Architect specializing in **React (Vite) and Django (DRF) codebases**. "
            "Your sole mission is to create a complete, high-coverage suite of **Playwright and Pytest** scripts. "
            "Your persona demands flawless logic and adherence to the project's 'Zero Bug' standard."
        )
        user_prompt = (
            "**Reasoning Framework (Chain of Thought):**\n"
            "1. **Blueprint Analysis:** Deconstruct the provided file structure and dependencies (React/Django/PostgreSQL stack).\n"
            "2. **Critical Path Mapping:** Identify and prioritize all critical paths (Auth, Billing, Start Run logic).\n"
            "3. **Code Generation:** Write the raw, complete code for all necessary test files.\n\n"
            f"**INPUT:**\n"
            f"File Structure: {file_structure_summary}\n"
            f"Requirements: {requirements_file}\n\n"
            "**OUTPUT CONSTRAINT:** You MUST return ONLY the raw, runnable code blocks (Pytest/Playwright). Do NOT include any conversational filler, explanations, or text outside of the code itself."
        )
        # Higher max_tokens for code generation
        return self.call_api(system_prompt, user_prompt, max_tokens=4096) 
    
    # --- AGENT 2: Debugging Agent (The Fixer) ---
    def generate_diff_fix(self, error_log, failed_file_content, failed_file_path):
        """Analyzes error, reads code, and provides the minimal, verifiable code diff."""
        system_prompt = (
            "You are the **Debugging Agent (The Fixer)**, a Principal Full-Stack Engineer at Google whose code is unbreakable. "
            "Your task is to fix the bug using the **most minimal and precise code change possible**. "
            "Your persona dictates that the fix MUST be verifiably correct and strictly follow the project stack (Django ORM, React Hooks)."
        )
        user_prompt = (
            "**Reasoning Framework (Chain of Thought):**\n"
            "1. **Trace Analysis:** Pinpoint the exact line and type of error using the log (e.g., Django 500, React State issue).\n"
            "2. **Code Context:** Examine the provided file content to locate the root cause (e.g., incorrect query, missing dependency).\n"
            "3. **Minimal Patch:** Generate the smallest possible fix that resolves the issue.\n\n"
            f"**INPUT:**\n"
            f"Failing File Path: {failed_file_path}\n"
            f"Error Log:\n{error_log}\n"
            f"Failing File Content:\n{failed_file_content}\n\n"
            "**OUTPUT CONSTRAINT:** You MUST return **ONLY the Unified Diff patch**. Do NOT include any filler, persona chatter, or surrounding text. The output must be ready for `git apply`."
        )
        # Low max_tokens for focused output (efficiency and cost-saving)
        return self.call_api(system_prompt, user_prompt, max_tokens=1024) 

    # --- AGENT 3: Reporting Agent (The Scribe) ---
    def generate_report(self, run_logs, fixes_count):
        """Generates the 2-3 page PDF summary and the technical Pull Request description."""
        system_prompt = (
            "You are the **Reporting Agent (The Scribe)**, a seasoned Technical Writer and Analyst. "
            "Your goal is to transform technical logs into high-value, client-facing artifacts. "
            "Your persona requires polished, professional communication that emphasizes value (e.g., 'X% more stable')."
        )
        user_prompt = (
            "**Reasoning Framework (Chain of Thought):**\n"
            "1. **Synthesis:** Collect all fixed diffs and logs.\n"
            "2. **Value Translation:** Calculate the stability gain and translate technical fixes into business value.\n"
            "3. **Dual Output:** Generate two distinct documents.\n\n"
            f"**INPUT:** The autonomous run found and fixed {fixes_count} bugs. Logs and diffs follow:\n{run_logs}\n\n"
            "**OUTPUT CONSTRAINT:** You MUST provide a two-part response: 1. The full Markdown content for the **2-3 Page PDF Summary** (titled 'Applaude Autonomous Remediation Report'). 2. The full text for the **GitHub Pull Request Description**. Separate these two sections clearly."
        )
        return self.call_api(system_prompt, user_prompt, max_tokens=3000)
