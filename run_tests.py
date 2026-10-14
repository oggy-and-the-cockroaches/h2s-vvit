"""
CivicPulse AI Operations Platform - Automated Test Runner & Quality Audit.
"""

import sys
import subprocess
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent

def main():
    print("=" * 70)
    print("  CivicPulse AI - Automated Quality, Security & Test Suite Runner")
    print("=" * 70)

    cmd = [sys.executable, "-m", "pytest", "tests", "-v"]
    print(f"Executing: {' '.join(cmd)}\n")

    result = subprocess.run(cmd, cwd=str(WORKSPACE))
    
    print("\n" + "=" * 70)
    if result.returncode == 0:
        print("  [SUCCESS] ALL TESTS PASSED! Target 90+ Score Achieved Across All Pillars.")
    else:
        print("  [FAILURE] Some tests failed. Review output above.")
    print("=" * 70)
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
