import subprocess
import os
import sys

class KOSPI50Manager:
    def __init__(self):
        self.agents = {
            "daily_stock": "agents/daily_stock/run.py",
            "fundamentals": "agents/fundamentals/run.py",
            "validator": "agents/validator/run.py"
        }

    def run_agent(self, name):
        print(f"\n[Manager] Starting Agent: {name}...")
        script_path = self.agents[name]
        
        # uv를 사용하여 에이전트 실행
        result = subprocess.run(["uv", "run", script_path], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[Manager] Agent {name} completed successfully.")
            return True, result.stdout
        else:
            print(f"[Manager] Agent {name} failed with error.")
            print(result.stderr)
            return False, result.stderr

    def start_workflow(self):
        print("=== KOSPI50 Multi-Agent Workflow Started ===")
        
        # 1. 데이터 수집 에이전트들 병렬 또는 순차 실행
        success1, _ = self.run_agent("daily_stock")
        if not success1:
            print("[Critical] Workflow aborted due to Daily Stock Agent failure.")
            return

        success2, _ = self.run_agent("fundamentals")
        if not success2:
            print("[Critical] Workflow aborted due to Fundamental Agent failure.")
            return

        # 2. 검증 에이전트 실행
        success3, _ = self.run_agent("validator")
        
        # 3. 검증 결과 확인 및 피드백
        if success3:
            report_path = "data/validation_report.txt"
            if os.path.exists(report_path):
                with open(report_path, "r") as f:
                    report = f.read()
                    print("\n=== Final Validation Report ===")
                    print(report)
                    if "ISSUE" in report or "WARNING" in report:
                        print("\n[Manager] Feedback: Issues detected. Please check data source consistency.")
                    else:
                        print("\n[Manager] Success: All data collected and verified.")
        
        print("\n=== KOSPI50 Multi-Agent Workflow Finished ===")

if __name__ == "__main__":
    manager = KOSPI50Manager()
    manager.start_workflow()
