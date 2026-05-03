from ai_engine.llm_client import PydanticAILLMClient
from ai_engine.test_generator import TestGenerator
from utils.logger import get_logger


logger = get_logger()


def get_user_test_intent() -> str:
    print("\nEnter your test scenario in plain English:")
    user_intent = input("Test Scenario: ").strip()

    if not user_intent:
        raise ValueError("Test scenario cannot be empty")

    return user_intent


def main():
    logger.info("Starting AI test generation runner")

    try:
        user_intent = get_user_test_intent()

        llm_client = PydanticAILLMClient()
        test_generator = TestGenerator(llm_client=llm_client)

        saved_path = test_generator.generate_and_save_test(
            user_intent=user_intent
        )

        logger.success(f"Generated test saved successfully at: {saved_path}")

        print("\nTest generation completed successfully!")
        print(f"Generated test file: {saved_path}")

    except Exception as error:
        logger.exception(f"Test generation runner failed: {error}")

        print("\nTest generation failed.")
        print(f"Reason: {error}")


if __name__ == "__main__":
    main()