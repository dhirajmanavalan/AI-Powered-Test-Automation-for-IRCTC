from pathlib import Path
from utils.logger import get_logger


logger = get_logger()


class TestDiscovery:
    """
    Discovers pytest test files from selected test directories.

    This class does not execute tests.
    It only finds test files that match pytest naming conventions.
    """

    def __init__(self, test_roots: list[str] | None = None):
        """
        Args:
            test_roots: List of folders where tests should be searched.
                        Default searches tests/generated and tests/manual.
        """

        self.test_roots = test_roots or [
            "tests/generated",
            "tests/manual",
        ]

        logger.debug(f"TestDiscovery initialized with roots: {self.test_roots}")

    def discover_tests(self) -> list[Path]:
        """
        Finds all pytest files matching test_*.py.

        Returns:
            List of test file paths.
        """

        logger.info("Starting test discovery")

        discovered_tests: list[Path] = []

        for root in self.test_roots:
            root_path = Path(root)

            if not root_path.exists():
                logger.warning(f"Test root does not exist: {root_path}")
                continue

            test_files = list(root_path.rglob("test_*.py"))

            logger.info(f"Found {len(test_files)} test files in {root_path}")

            discovered_tests.extend(test_files)

        unique_tests = sorted(set(discovered_tests))

        logger.success(f"Total discovered test files: {len(unique_tests)}")

        return unique_tests

    def discover_tests_by_marker(self, marker_keyword: str) -> list[Path]:
        """
        Optional helper to discover tests whose file name contains a keyword.

        Example:
            marker_keyword='login'
            returns files like test_irctc_login.py
        """

        logger.info(f"Discovering tests using keyword: {marker_keyword}")

        all_tests = self.discover_tests()

        filtered_tests = [
            test_file
            for test_file in all_tests
            if marker_keyword.lower() in test_file.name.lower()
        ]

        logger.info(f"Found {len(filtered_tests)} tests matching keyword: {marker_keyword}")

        return filtered_tests