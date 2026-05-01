"""Test report generation"""
import sys
sys.path.insert(0, "C:/Users/Administrator/WorkBuddy/20260501121650")

from equipmind.simulator.generator import seed_devices, seed_historical_data
from equipmind.reports.html_report import ReportGenerator

seed_devices()
seed_historical_data(hours=6)

report = ReportGenerator.generate_all(hours=6)
with open("C:/Users/Administrator/WorkBuddy/20260501121650/report_test.txt", "w", encoding="utf-8") as f:
    if report:
        f.write(f"SUCCESS: {report}")
    else:
        f.write("FAILED")
