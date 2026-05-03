from pydantic_ai import Agent, Tool

from ai_engine.output_models import (
    GeneratedTestScript,
    LocatorHealingResult,
    FailureAnalysisResult,
)

from ai_engine.prompt_templates import (
    TEST_GENERATION_SYSTEM_PROMPT,
    LOCATOR_HEALING_SYSTEM_PROMPT,
    FAILURE_ANALYSIS_SYSTEM_PROMPT,
)

from config.settings import settings
from utils.logger import get_logger
from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.providers.mistral import MistralProvider

from ai_engine.agent_tools.page_object_tools import get_available_page_objects
from ai_engine.agent_tools.locator_healing_tools import suggest_locator_healing
from ai_engine.agent_tools.failure_analysis_tools import (
    analyse_failure_details,
    save_failure_analysis_report
)


logger = get_logger()


class PydanticAILLMClient:
    """
    LLM client implemented using Pydantic AI.

    This class keeps all agent execution logic in one place.
    The actual prompts are imported from prompt_templates.py.
    """

    mistral_model = MistralModel(
        model_name=settings.MISTRAL_MODEL,
        provider=MistralProvider(api_key=settings.MISTRAL_API_KEY)
    )

    def __init__(self):
        logger.info("Initializing Pydantic AI LLM client")

        self.test_generation_agent = Agent(
            model=self.mistral_model,
            output_type=GeneratedTestScript,
            system_prompt=TEST_GENERATION_SYSTEM_PROMPT,
            tools=[
                Tool(get_available_page_objects),
            ],
        )

        self.locator_healing_agent = Agent(
            model=self.mistral_model,
            output_type=LocatorHealingResult,
            system_prompt=LOCATOR_HEALING_SYSTEM_PROMPT,
            tools=[
                Tool(suggest_locator_healing),
            ],
        )

        self.failure_analysis_agent = Agent(
            model=self.mistral_model,
            output_type=FailureAnalysisResult,
            system_prompt=FAILURE_ANALYSIS_SYSTEM_PROMPT,
            tools=[
                Tool(analyse_failure_details),
            ],
        )

        logger.success("Pydantic AI LLM client initialized successfully")

    def generate_test_script(self, user_intent: str) -> GeneratedTestScript:
        """
        Generates a Playwright pytest test script from natural language intent.
        """

        logger.info("Generating test script using Pydantic AI")

        user_prompt = f"""
        Generate a Playwright pytest test for this scenario:

        {user_intent}

        If needed, use the available page object tool before generating the code.

        Return:
        - file_name
        - complete Python test code
        """

        try:
            result = self.test_generation_agent.run_sync(user_prompt)

            logger.success("Test script generated successfully")

            return result.output

        except Exception as error:
            logger.exception(f"Failed to generate test script: {error}")
            raise

    def heal_locator(
        self,
        failed_locator: str,
        error_message: str,
        html_snapshot: str
    ) -> LocatorHealingResult:
        """
        Suggests stable replacement locators for a failed Playwright locator.
        """

        logger.info("Generating locator healing suggestions using Pydantic AI")

        user_prompt = f"""
        A Playwright locator failed.

        Failed Locator:
        {failed_locator}

        Error Message:
        {error_message}

        Page HTML Snapshot:
        {html_snapshot}

        Use the locator healing tool if useful.

        Return:
        - failed_locator
        - suggested_locators
        - reason
        """

        try:
            result = self.locator_healing_agent.run_sync(user_prompt)

            logger.success("Locator healing suggestions generated successfully")

            return result.output

        except Exception as error:
            logger.exception(f"Failed to heal locator: {error}")
            raise

    def analyse_failure(
        self,
        test_name: str,
        error_log: str,
        screenshot_path: str | None = None
    ) -> FailureAnalysisResult:
        """
        Generates structured failure analysis for pytest/Playwright failures.
        """

        logger.info(f"Generating failure analysis for test: {test_name}")

        user_prompt = f"""
        Analyze this Playwright/pytest failure.

        Test Name:
        {test_name}

        Error Log:
        {error_log}

        Screenshot Path:
        {screenshot_path or "No screenshot available"}

        Use the failure analysis tool if useful.

        Return:
        - root_cause
        - possible_reasons
        - suggested_fix
        - locator_suggestion
        """

        try:
            result = self.failure_analysis_agent.run_sync(user_prompt)

            logger.success("Failure analysis generated successfully")

            return result.output

        except Exception as error:
            logger.exception(f"Failed to analyze failure: {error}")
            raise