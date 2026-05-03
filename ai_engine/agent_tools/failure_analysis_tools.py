from pathlib import Path
from typing import Any
from utils.logger import get_logger

logger = get_logger()

def analyse_failure_details(
    test_name: str,
    error_log: str,
    screenshot_path: str | None = None
) -> dict[str, Any]:
    """
    Analyzes failure details using deterministic rules.

    This tool does not call the LLM. It extracts useful hints from
    the error log and gives structured debugging information to the agent.
    """

    logger.info("Tool called: analyse_failure_details")
    logger.debug(f"Test name: {test_name}")

    error_lower = error_log.lower()

    possible_reasons: list[str] = []
    suggested_fix = "Review the failure log, screenshot, and page object locators."

    if "timeout" in error_lower:
        root_cause = "The test timed out while waiting for an element or action to complete."
        possible_reasons.extend([
            "The element was not visible within the timeout.",
            "The page may have loaded slowly.",
            "The locator may be incorrect or outdated.",
            "A popup, captcha, or overlay may be blocking the element.",
        ])
        suggested_fix = (
            "Add proper waits, verify the locator, check screenshots, "
            "and ensure the page or popup is fully loaded before interacting."
        )

    elif "strict mode violation" in error_lower:
        root_cause = "The locator matched multiple elements instead of one."
        possible_reasons.extend([
            "The locator is too generic.",
            "Multiple buttons or inputs have similar text.",
            "The page contains duplicate matching elements.",
        ])
        suggested_fix = (
            "Make the locator more specific using role, text, parent container, "
            "placeholder, or data-testid."
        )

    elif "not visible" in error_lower:
        root_cause = "The target element exists but is not visible to the user."
        possible_reasons.extend([
            "The element is hidden behind another UI layer.",
            "The wrong page state is active.",
            "The modal or popup did not open correctly.",
        ])
        suggested_fix = (
            "Wait for visibility, verify the popup is open, and check if another "
            "overlay is blocking the element."
        )

    elif "not found" in error_lower or "no element" in error_lower:
        root_cause = "The element could not be found on the current page."
        possible_reasons.extend([
            "The locator is wrong.",
            "The page did not navigate to the expected screen.",
            "The element appears only after a user action.",
        ])
        suggested_fix = (
            "Check the current page, validate locator strategy, and confirm all "
            "previous steps completed successfully."
        )

    elif "assert" in error_lower:
        root_cause = "An assertion failed because the actual result did not match the expected result."
        possible_reasons.extend([
            "The expected UI state did not appear.",
            "The test data may be invalid.",
            "The assertion may be too strict.",
        ])
        suggested_fix = (
            "Check the expected condition, review the actual UI response, "
            "and update the assertion if needed."
        )

    else:
        root_cause = "The failure requires further investigation."
        possible_reasons.extend([
            "The error may be application-related.",
            "The error may be automation-related.",
            "The error may be caused by unstable test data or environment.",
        ])

    locator_suggestion = None

    if any(keyword in error_lower for keyword in ["locator", "element", "strict mode", "not visible", "not found"]):
        locator_suggestion = (
            "Prefer Playwright role, label, placeholder, text, or data-testid locators. "
            "Avoid brittle absolute XPath and dynamic CSS classes."
        )

    if screenshot_path:
        possible_reasons.append(
            f"Screenshot available for debugging: {screenshot_path}"
        )

    return {
        "test_name": test_name,
        "root_cause": root_cause,
        "possible_reasons": possible_reasons,
        "suggested_fix": suggested_fix,
        "locator_suggestion": locator_suggestion,
    }


def save_failure_analysis_report(
    test_name: str,
    analysis_text: str,
    output_dir: str = "reports/failure_analysis"
) -> str:
    """
    Saves failure analysis text into a file.
    """

    logger.info("Tool called: save_failure_analysis_report")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    safe_test_name = (
        test_name
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )

    file_path = output_path / f"{safe_test_name}_failure_analysis.txt"
    file_path.write_text(analysis_text, encoding="utf-8")

    logger.success(f"Failure analysis saved at: {file_path}")

    return str(file_path)


