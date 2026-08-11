import subprocess
import sys
import os

SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'python-web-scraper', 'src')


def run_step(step_name, script, cwd=SRC_DIR):
    print("=" * 60)
    print(f"Running {step_name}...")
    result = subprocess.run([sys.executable, script], cwd=cwd)
    if result.returncode != 0:
        print(f"ERROR: {script} failed with exit code {result.returncode}")
        sys.exit(1)
    print(f"{step_name} done.\n")


def main():
    print("=" * 60)
    print("MAIMAI SONG NAME SCRAPING - Pipeline Runner")
    print("=" * 60)
    print()
    print("Ensure maimai-songDatabase.json exists in python-web-scraper/")
    print("(Step 1: download it from maimaisonglist online manually)\n")

    run_step("Step 2: getTitle", "getTitle.py")

    print("=" * 60)
    print("Step 3: botRequesting (optional)")
    choice = input("Run botRequesting.py? (y/n): ").strip().lower()
    if choice == 'y':
        print("IMPORTANT: Make sure Discord is open and the XD bot DM is focused!")
        input("Press Enter to start botRequesting.py...")
        run_step("Step 3: botRequesting", "botRequesting.py")
    else:
        print("Skipping botRequesting.py")

    run_step("Step 4: extractData", "extractData.py")
    run_step("Step 5: modifyData", "modifyData.py")
    run_step("Step 6: replaceData", "replaceData.py")
    run_step("Step 7: splitData", "splitData.py")
    run_step("Step 8: diffReduction", "diffReduction.py")
    run_step("Step 9: replaceImageURL", "replaceImageURL.py")
    run_step("Step 10: purgeNoConstant", "purgeNoConstant.py")
    run_step("Step 11: merge_versions", "merge_versions.py")

    print("=" * 60)
    print("All steps completed successfully!")


if __name__ == "__main__":
    main()
