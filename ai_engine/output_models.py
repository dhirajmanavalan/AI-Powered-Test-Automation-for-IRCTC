from pydantic import BaseModel, Field

class GeneratedTestScript(BaseModel):
    """
    Structured output for AI-generated Playwright test scripts.
    """

    file_name: str = Field(
        description="Suggested Python test file name, for example test_train_search.py"
    )

    code: str = Field(
        description="Complete pytest-compatible Playwright Python test code"
    )


class LocatorHealingResult(BaseModel):
    """
    Structured output for locator healing suggestions.
    """

    failed_locator: str = Field(
        description="The original locator that failed during execution"
    )

    suggested_locators: list[str] = Field(
        description="List of stable replacement Playwright locators"
    )

    reason: str = Field(
        description="Reason why the suggested locators may work better"
    )


class FailureAnalysisResult(BaseModel):
    """
    Structured output for AI-powered failure analysis.
    """

    root_cause: str = Field(
        description="Most likely root cause of the failure"
    )

    possible_reasons: list[str] = Field(
        description="Possible reasons that may have caused the failure"
    )

    suggested_fix: str = Field(
        description="Practical steps to fix the failure"
    )

    locator_suggestion: str | None = Field(
        default=None,
        description="Better locator strategy if the failure is locator-related"
    )