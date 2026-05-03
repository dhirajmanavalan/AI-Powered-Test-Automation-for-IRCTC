# run_antigravity.py

from antigravity.discovery import TestDiscovery
from antigravity.prioritiser import TestPrioritiser
from antigravity.cloud_executor import CloudExecutor
from utils.logger import get_logger


logger = get_logger()


def main():
    """
    Antigravity runner.

    Flow:
    1. Discover tests
    2. Prioritise tests
    3. Execute tests
    4. Print report path
    """

    logger.info("Starting Antigravity test orchestration")

    discovery = TestDiscovery(
        test_roots=[
            "tests/generated",
            "tests/manual",
        ]
    )

    prioritiser = TestPrioritiser()

    executor = CloudExecutor(
        report_dir="reports",
        headed=True,
    )

    test_files = discovery.discover_tests()

    if not test_files:
        logger.warning("No tests discovered. Stopping execution.")
        print("No tests discovered.")
        return

    prioritised_tests = prioritiser.prioritise(test_files)

    result = executor.run_tests(prioritised_tests)

    print("\nAntigravity Execution Completed")
    print(f"Return Code: {result['return_code']}")
    print(f"HTML Report: {result['report_path']}")

    if result["return_code"] != 0:
        print("\nSome tests failed. Check the HTML report and logs.")


if __name__ == "__main__":
    main()