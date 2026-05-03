from pathlib import Path
from utils.logger import get_logger

logger = get_logger()

class TestPrioritiser:
    """
    Prioritises discovered test files before execution.

    Priority is currently rule-based.
    Later this can be replaced or enhanced with Pydantic AI.
    """

    PRIORITY_KEYWORDS = {
        "login": 1,
        "auth": 1,
        "search": 2,
        "train": 2,
        "pnr": 3,
        "booking": 4,
        "payment": 5,
        "cancel": 6,
    }

    def prioritise(self, test_files: list[Path]) -> list[Path]:
        """
        Sorts test files based on business priority.

        Args:
            test_files: List of discovered test files.

        Returns:
            Sorted list of test files.
        """

        logger.info("Starting test prioritisation")

        if not test_files:
            logger.warning("No test files received for prioritisation")
            return []

        prioritised_tests = sorted(
            test_files,
            key=self._priority_score
        )

        for test_file in prioritised_tests:
            logger.debug(
                f"Prioritised test: {test_file} "
                f"with score {self._priority_score(test_file)}"
            )

        logger.success("Test prioritisation completed")

        return prioritised_tests

    def _priority_score(self, test_file: Path) -> int:
        """
        Calculates priority score from file name.

        Lower score means higher priority.
        """

        file_name = test_file.name.lower()

        for keyword, score in self.PRIORITY_KEYWORDS.items():
            if keyword in file_name:
                return score

        return 99