import subprocess
from pathlib import Path
from datetime import datetime

from utils.logger import get_logger


logger = get_logger()


class CloudExecutor:
    """
    Executes pytest tests and generates reports.

    Currently runs tests locally using subprocess.
    can be extended for Jenkins, Docker, or cloud execution.
    """

    def __init__(
        self,
        report_dir: str = "reports",
        headed: bool = True,
    ):
        self.report_dir = Path(report_dir)
        self.headed = headed

        self.report_dir.mkdir(parents=True, exist_ok=True)

        logger.debug(
            f"CloudExecutor initialized with report_dir={self.report_dir}, headed={self.headed}"
        )

    def run_tests(self, test_files: list[Path]) -> dict[str, str | int]:
        """
        Runs pytest for given test files.

        Args:
            test_files: List of test files to execute.

        Returns:
            Dictionary containing return code, stdout, stderr, and report path.
        """

        logger.info("Starting test execution")

        if not test_files:
            logger.warning("No test files found for execution")

            return {
                "return_code": 1,
                "stdout": "",
                "stderr": "No test files found for execution",
                "report_path": "",
            }

        report_path = self._build_report_path()

        command = self._build_pytest_command(
            test_files=test_files,
            report_path=report_path,
        )

        logger.info("Executing pytest command")
        logger.debug(f"Command: {' '.join(command)}")

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        logger.info(f"Pytest execution completed with return code: {result.returncode}")

        if result.returncode == 0:
            logger.success("All selected tests passed")
        else:
            logger.error("Some selected tests failed")

        return {
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "report_path": str(report_path),
        }

    def _build_report_path(self) -> Path:
        """
        Creates timestamped HTML report path.
        """

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        report_path = self.report_dir / f"API_Test_Report_{timestamp}.html"

        return report_path

    def _build_pytest_command(
        self,
        test_files: list[Path],
        report_path: Path,
    ) -> list[str]:
        """
        Builds pytest command.
        """

        test_paths = [str(test_file) for test_file in test_files]

        command = [
            "pytest",
            *test_paths,
            f"--html={report_path}",
            "--self-contained-html",
        ]

        if self.headed:
            command.append("--headed")

        return command