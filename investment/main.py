import subprocess
import os

def run_agent(script_path):
    print(f"\n>> Executing Investment Agent: {script_path}")
    result = subprocess.run(["uv", "run", script_path], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error in {script_path}: {result.stderr}")
        return False
    print(result.stdout)
    return True

def main():
    print("=== Starting KOSPI Top 10 Investment Committee ===")
    
    # Run Agents 1, 2, 3 in sequence
    agents = [
        "investment/quant_agent/run.py",
        "investment/fundamental_agent/run.py",
        "investment/news_agent/run.py"
    ]
    
    for agent in agents:
        if not run_agent(agent):
            return

    # Run Manager Agent to finalize
    run_agent("investment/manager_agent/run.py")
    
    print("\n=== Investment Committee Session Closed ===")

if __name__ == "__main__":
    main()
