# scripts/run_pr_audit.py
import subprocess
import sys
from pathlib import Path

# Important: We need to add the project root to the Python path
# so we can import our huggingface_tasks module.
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from huggingface_tasks.classify_text import analyze_code_snippet

def get_changed_files(branch: str) -> list[str]:
    """Gets a list of files changed compared to the target branch."""
    print(f"Finding files changed against branch: {branch}")
    # This git command gets the list of files that have been added (A) or modified (M)
    cmd = ["git", "diff", "--name-only", "--diff-filter=AM", f"origin/{branch}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error getting git diff: {result.stderr}")
        return []
    
    files = result.stdout.strip().split("\n")
    return [f for f in files if f] # Filter out empty lines

def main():
    """Main function to run the audit on changed files in a PR."""
    # In a GitHub Actions PR workflow, the target branch is typically 'main' or 'master'
    TARGET_BRANCH = "main" 
    
    files_to_check = get_changed_files(TARGET_BRANCH)
    
    if not files_to_check:
        print("No changed files to analyze. Exiting.")
        sys.exit(0)

    print("\n--- Starting SmartAuditOps Analysis ---")
    high_risk_found = False
    
    for file_path in files_to_check:
        path = Path(file_path)
        # We only want to analyze text-based files, not images or other binaries
        if path.suffix not in ['.py', '.js', '.ts', '.java', '.go', '.yaml', '.yml', '.json', '.env', '.sh', '.rb']:
            print(f"Skipping non-code file: {file_path}")
            continue

        print(f"\nAnalyzing file: {file_path}")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if not content.strip():
                print("File is empty. Skipping.")
                continue

            analysis = analyze_code_snippet(content)
            
            # Print the results in a readable format for the CI log
            print("Analysis Results:")
            for label, score in analysis['analysis'].items():
                print(f"  - {label}: {score:.4f}")
            
            # --- The Gatekeeper Logic ---
            # Check if the 'secret exposed' score is dangerously high
            if analysis['analysis'].get("secret exposed", 0.0) > 0.9:
                print(f"🚨🚨🚨 HIGH-RISK ALERT: Potential secret detected in {file_path}! 🚨🚨🚨")
                high_risk_found = True

        except Exception as e:
            print(f"Could not analyze file {file_path}. Error: {e}")

    print("\n--- Analysis Complete ---")

    if high_risk_found:
        print("Failing CI check due to high-risk issues found.")
        sys.exit(1) # Exit with a non-zero code to fail the workflow
    else:
        print("No high-risk issues found. Audit passed!")
        sys.exit(0) # Exit with zero for success

if __name__ == "__main__":
    main()