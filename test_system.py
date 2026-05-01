"""Test EquipMind AI system"""
import sys, traceback

LOG = "C:/Users/Administrator/WorkBuddy/20260501121650/system_test.txt"

def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(str(msg) + "\n")

log("=== System Test ===")

# 1. Check imports
log("\n--- Import Check ---")
packages = {
    "click": "click",
    "rich": "rich",
    "sklearn": "sklearn",
    "pandas": "pandas",
    "numpy": "numpy",
    "matplotlib": "matplotlib",
}
for name, mod_name in packages.items():
    try:
        mod = __import__(mod_name)
        ver = getattr(mod, "__version__", "?")
        log(f"  {name}: OK ({ver})")
    except ImportError as e:
        log(f"  {name}: MISSING - {e}")

# 2. Import equipmind modules
log("\n--- EquipMind Import ---")
sys.path.insert(0, "C:/Users/Administrator/WorkBuddy/20260501121650")
try:
    from equipmind import __version__
    log(f"  equipmind version: {__version__}")
    
    from equipmind.data.models import Device, Metric
    log(f"  models: OK")
    
    from equipmind.data.database import db
    log(f"  database: OK")
    
    from equipmind.simulator.generator import seed_devices, generate_metrics
    log(f"  simulator: OK")
    
    from equipmind.ai.anomaly import AnomalyDetector
    log(f"  anomaly detector: OK")
    
    from equipmind.ai.forecaster import TrendForecaster
    log(f"  forecaster: OK")
    
    from equipmind.ai.health import HealthScorer
    log(f"  health scorer: OK")
    
    from equipmind.ai.failure import FailurePredictor
    log(f"  failure predictor: OK")
    
    from equipmind.ai.trainer import ModelTrainer
    log(f"  model trainer: OK")
    
    from equipmind.monitor.engine import MonitorEngine
    log(f"  monitor engine: OK")
    
    from equipmind.cli.main import cli
    from click.testing import CliRunner
    log(f"  CLI: OK")
    
except Exception as e:
    log(f"  ERROR: {traceback.format_exc()}")

# 3. Test data layer
log("\n--- Data Layer Test ---")
try:
    from equipmind.data.repository import DeviceRepository, MetricRepository, AlertRepository
    from equipmind.data.models import Device
    
    # Seed devices
    devices = seed_devices()
    log(f"  Seeded {len(devices)} devices")
    
    # Check devices in DB
    db_devices = DeviceRepository.list_all()
    log(f"  Devices in DB: {len(db_devices)}")
    if db_devices:
        d = db_devices[0]
        log(f"  First device: {d.id} - {d.name}")
    
    # Generate metrics
    from equipmind.simulator.generator import generate_and_store
    count = generate_and_store()
    log(f"  Generated {count} metrics")
    
except Exception as e:
    log(f"  ERROR: {traceback.format_exc()}")

# 4. Test AI engine
log("\n--- AI Engine Test ---")
try:
    from equipmind.ai.health import HealthScorer
    scorer = HealthScorer()
    score = scorer.calculate(cpu=45, memory=60, disk=55, network=30)
    log(f"  Health score: {score} ({scorer.get_level(score)})")
    
    score2 = scorer.calculate(cpu=95, memory=92, disk=88, network=85)
    log(f"  Critical score: {score2} ({scorer.get_level(score2)})")
    
    advice = scorer.get_advice(score2, cpu=95, memory=92, disk=88, network=85)
    log(f"  Advice: {len(advice)} suggestions")
    for a in advice:
        log(f"    - {a}")
    
    from equipmind.ai.anomaly import AnomalyDetector
    detector = AnomalyDetector()
    normal_vals = [45, 46, 44, 45, 47, 46, 44, 45, 46, 45, 44, 46]
    result = detector.analyze_window(normal_vals, 90)
    log(f"  Anomaly detection on spike (90): is_anomaly={result['is_anomaly']}, score={result['anomaly_score']}")
    
    from equipmind.ai.failure import FailurePredictor
    predictor = FailurePredictor()
    metrics = {
        "cpu": normal_vals + [85, 88, 92, 95],
        "memory": [60]*16 + [78, 82, 88, 95],
        "disk": [55]*16 + [56, 57, 58, 59],
        "network": [30]*16 + [45, 55, 65, 75]
    }
    pred_result = predictor.predict("test-device", metrics)
    log(f"  Failure prediction: risk={pred_result['risk_score']}, level={pred_result['risk_level']}")
    log(f"  Maintenance: {pred_result['maintenance_window']}")
    
    from equipmind.ai.trainer import ModelTrainer
    trainer = ModelTrainer()
    full_result = trainer.analyze_device("srv-web-01")
    log(f"  Full analysis for srv-web-01:")
    if "error" not in full_result:
        log(f"    Health: {full_result.get('health_score')}")
        log(f"    Risk: {full_result.get('failure_prediction',{}).get('risk_level')}")
        log(f"    Advice count: {len(full_result.get('advice',[]))}")
    
except Exception as e:
    log(f"  ERROR: {traceback.format_exc()}")

# 5. Test CLI
log("\n--- CLI Test ---")
try:
    from click.testing import CliRunner
    from equipmind.cli.main import cli
    
    runner = CliRunner()
    
    result = runner.invoke(cli, ["--help"])
    log(f"  equipmind --help: exit={result.exit_code}")
    
    result = runner.invoke(cli, ["devices", "list"])
    log(f"  devices list: exit={result.exit_code}, output_len={len(result.output)}")
    
    result = runner.invoke(cli, ["alerts", "list"])
    log(f"  alerts list: exit={result.exit_code}")
    
    result = runner.invoke(cli, ["predict", "run", "srv-web-01"])
    log(f"  predict srv-web-01: exit={result.exit_code}")
    
    # Test report generation
    from equipmind.reports.html_report import ReportGenerator
    report = ReportGenerator.generate_all(hours=6)
    if report:
        log(f"  Report generated: {report}")
    else:
        log(f"  Report: FAILED")
    
except Exception as e:
    log(f"  ERROR: {traceback.format_exc()}")

log("\n=== Test Complete ===")
