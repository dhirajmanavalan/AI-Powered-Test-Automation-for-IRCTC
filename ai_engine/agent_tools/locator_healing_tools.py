from typing import Any
from utils.logger import get_logger

logger = get_logger()
def suggest_locator_healing(
    failed_locator: str,
    error_message: str,
    html_snapshot: str
) -> dict[str, Any]:
    """
    Suggests fallback locator strategies based on the failed locator,
    error message, and page HTML.

    This tool does not call the LLM. It gives deterministic fallback
    suggestions that the agent can use in its final answer.
    """

    logger.info("Tool called: suggest_locator_healing")
    logger.debug(f"Failed locator: {failed_locator}")
    logger.debug(f"Error message: {error_message}")

    suggestions: list[str] = []

    lower_html = html_snapshot.lower()

    if "login" in lower_html:
        suggestions.extend([
            "text=LOGIN",
            "button:has-text('LOGIN')",
            "button:has-text('Login')",
            "[data-testid='login-button']",
            "[aria-label='Login']",
        ])

    if "user" in lower_html or "username" in lower_html:
        suggestions.extend([
            "input[placeholder='User Name']",
            "input[placeholder='Username']",
            "input[name='userName']",
            "input[name='username']",
            "[data-testid='username-input']",
        ])

    if "password" in lower_html:
        suggestions.extend([
            "input[placeholder='Password']",
            "input[name='password']",
            "[data-testid='password-input']",
        ])

    if "sign in" in lower_html or "signin" in lower_html:
        suggestions.extend([
            "button:has-text('SIGN IN')",
            "button:has-text('Sign In')",
            "text=SIGN IN",
            "[data-testid='sign-in-button']",
        ])

    unique_suggestions = list(dict.fromkeys(suggestions))

    return {
        "failed_locator": failed_locator,
        "suggested_locators": unique_suggestions,
        "reason": "Suggested stable Playwright locators using visible text, placeholder, name, aria-label, and data-testid patterns."
    }


