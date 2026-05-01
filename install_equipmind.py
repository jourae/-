import subprocess
import sys

result = subprocess.run(
    [sys.executable, "-m", "pip", "install", "-e", r"C:\Users\Administrator\WorkBuddy\20260501121650"],
    capture_output=True, text=True, timeout=120
)
with open(r"C:\Users\Administrator\WorkBuddy\20260501121650\pip_out.txt", "w") as f:
    f.write("STDOUT:\n" + result.stdout + "\nSTDERR:\n" + result.stderr + "\nRETURNCODE: " + str(result.returncode))
print(result.stdout)
print(result.stderr)
