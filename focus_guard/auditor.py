import os
import sys
import subprocess
import google.generativeai as genai
from plyer import notification
from config import REWARD_DURATION_MINUTES
from state_manager import StateManager

# Configure API Key
API_KEY = os.environ.get("GEMINI_API_KEY")

def send_notification(title, message):
    try:
        notification.notify(
            title=title,
            message=message[:200] + "..." if len(message) > 200 else message,
            app_name="Code-to-Play Auditor",
            timeout=10
        )
    except Exception as e:
        print(f"Notification error: {e}")

def get_git_diff():
    try:
        # Get the diff of the last commit (HEAD vs HEAD~1)
        # Note: This is intended to be run AFTER the commit, so HEAD is the new commit.
        diff = subprocess.check_output(
            ["git", "diff", "HEAD^", "HEAD"], 
            stderr=subprocess.STDOUT
        ).decode("utf-8", errors="ignore")
        
        # Get commit message
        msg = subprocess.check_output(
            ["git", "log", "-1", "--pretty=%B"], 
            stderr=subprocess.STDOUT
        ).decode("utf-8", errors="ignore")
        
        return f"Commit Message: {msg}\n\nDiff:\n{diff}"
    except subprocess.CalledProcessError:
        return None

def audit_commit(diff_text):
    if not API_KEY:
        return False, "API Key missing. Set GEMINI_API_KEY."

    genai.configure(api_key=API_KEY)
    
    # Use the cutting-edge model as requested
    model = genai.GenerativeModel('gemini-3-flash-preview')

    prompt = f"""
    You are a strict code auditor for a gamified productivity system.
    Analyze the following git commit diff and message.
    Determine if this represents SUBSTANTIAL, MEANINGFUL work (e.g., adding logic, fixing bugs, refactoring, meaningful documentation).
    
    CRITERIA FOR REJECTION (Return FALSE):
    - Code formatting changes only (white space, indentation).
    - Adding meaningless comments or "padding".
    - Tweaking constants without explanation.
    - Very minor text changes in documentation.
    - Generated code that required no human thought.
    - Generic, textbook code that looks copied (without personal comments/modifications).
    
    CRITERIA FOR ACCEPTANCE (Return TRUE):
    - Logic changes that demonstrate understanding.
    - Bug fixes.
    - New features implementing specific project requirements.
    - Significant refactoring.
    - Detailed documentation updates explaining "Why".
    - Evidence of trial and error (e.g., experimental comments).

    Respond ONLY with the word "TRUE" or "FALSE". Do not add explanation.

    ---
    {diff_text}
    ---
    """

    try:
        response = model.generate_content(prompt)
        text = response.text.strip().upper()
        if "TRUE" in text:
            return True, "Substantial contribution detected."
        else:
            return False, "Low effort or trivial change detected."
    except Exception as e:
        return False, f"Audit Error: {e}"

def main():
    print("Auditing last commit...")
    
    diff_text = get_git_diff()
    if not diff_text:
        msg = "Could not fetch git diff. Make sure this is a git repo and has at least one parent commit."
        print(msg)
        send_notification("Audit Failed", msg)
        sys.exit(1)

    # Truncate if too long (save tokens/time)
    if len(diff_text) > 10000:
        diff_text = diff_text[:10000] + "\n...[TRUNCATED]..."

    success, reason = audit_commit(diff_text)

    if success:
        StateManager.grant_reward(REWARD_DURATION_MINUTES)
        msg = f"Commit Accepted! +{REWARD_DURATION_MINUTES}mins Playtime.\n({reason})"
        print(msg)
        send_notification("Code-to-Play: UNLOCKED", msg)
    else:
        # Note: Do NOT revoke time if failed? 
        # Requirement: "Block continues" -> implies we just don't grant new time.
        # If user ALREADY had time, a bad commit shouldn't necessarily penalize, but for strictness...
        # The prompt says: "Reject... Block continues".
        # We will simply NOT grant time.
        msg = f"Commit Rejected.\n{reason}"
        print(msg)
        send_notification("Code-to-Play: REJECTED", msg)

if __name__ == "__main__":
    main()
