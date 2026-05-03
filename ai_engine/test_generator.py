# ai_engine/test_generator.py

from pathlib import Path
from ai_engine.llm_client import PydanticAILLMClient
from utils.logger import get_logger


logger = get_logger()


class TestGenerator:
    """
    Converts natural language test scenarios into Playwright pytest scripts.
    """

    def __init__(self, llm_client: PydanticAILLMClient):
        self.llm_client = llm_client
        logger.debug("TestGenerator initialized")

    def generate_test_script(self, user_intent: str) -> str:
        """
        Returns generated Playwright test code as string.
        """

        result = self.llm_client.generate_test_script(user_intent)

        return result.code

    def generate_and_save_test(self, user_intent: str) -> Path:
        """
        Generates and saves Playwright test code.
        """

        result = self.llm_client.generate_test_script(user_intent)

        output_dir = Path("tests/generated")
        output_dir.mkdir(parents=True, exist_ok=True)

        file_path = output_dir / result.file_name

        file_path.write_text(result.code, encoding="utf-8")

        logger.success(f"Generated test saved at: {file_path}")

        return file_path