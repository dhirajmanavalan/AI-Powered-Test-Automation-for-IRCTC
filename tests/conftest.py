import os
import json
import platform
from datetime import datetime
from playwright.sync_api import sync_playwright
import allure
import pytest


def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """
    Creates timestamped pytest-html and Allure result paths.
    Also generates environment.properties and categories.json
    for Allure dashboard.
    """

    timestamp = get_timestamp()

    reports_dir = os.path.join(os.getcwd(), "reports")
    html_reports_dir = os.path.join(reports_dir, "html")
    allure_results_dir = os.path.join(
        reports_dir,
        "allure-results",
        f"run_{timestamp}"
    )

    os.makedirs(html_reports_dir, exist_ok=True)
    os.makedirs(allure_results_dir, exist_ok=True)

    # pytest-html report path
    if hasattr(config.option, "htmlpath"):
        config.option.htmlpath = os.path.join(
            html_reports_dir,
            f"API_Test_Report_{timestamp}.html"
        )

    # allure result directory
    if hasattr(config.option, "allure_report_dir"):
        config.option.allure_report_dir = allure_results_dir

    # ──────────────────────────────────────────
    # AUTO-GENERATE environment.properties
    # ──────────────────────────────────────────
    env_file = os.path.join(allure_results_dir, "environment.properties")

    with open(env_file, "w") as f:
        f.write(f"Project=AI-Powered Test Automation for IRCTC\n")
        f.write(f"Browser=Chromium\n")
        f.write(f"Browser.Mode=Headed\n")
        f.write(f"Platform={platform.system()} {platform.release()}\n")
        f.write(f"Python.Version={platform.python_version()}\n")
        f.write(f"Framework=Playwright + pytest\n")
        f.write(f"AI.Model=mistral-small-latest\n")
        f.write(f"Environment=Local\n")
        f.write(f"Run.Timestamp={timestamp}\n")
        f.write(f"Test.Type=UI Automation\n")
        f.write(f"Application.URL=https://www.irctc.co.in\n")

    # ──────────────────────────────────────────
    # AUTO-GENERATE categories.json
    # ──────────────────────────────────────────
    categories = [
        {
            "name": "Product Bugs",
            "matchedStatuses": ["failed"],
            "messageRegex": ".*AssertionError.*"
        },
        {
            "name": "Locator Failures",
            "matchedStatuses": ["broken"],
            "messageRegex": ".*locator.*|.*TimeoutError.*|.*strict mode.*"
        },
        {
            "name": "Test Defects",
            "matchedStatuses": ["broken"],
            "messageRegex": ".*Error.*"
        },
        {
            "name": "Timeout Errors",
            "matchedStatuses": ["broken", "failed"],
            "messageRegex": ".*Timeout.*|.*timed out.*"
        },
        {
            "name": "Skipped Tests",
            "matchedStatuses": ["skipped"]
        }
    ]

    categories_file = os.path.join(allure_results_dir, "categories.json")

    with open(categories_file, "w") as f:
        json.dump(categories, f, indent=2)

    print(f"\nHTML Report Path     : {getattr(config.option, 'htmlpath', None)}")
    print(f"Allure Results Dir   : {getattr(config.option, 'allure_report_dir', None)}")
    print(f"Environment File     : {env_file}")
    print(f"Categories File      : {categories_file}\n")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Attaches screenshot to Allure report when test fails.
    """

    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")

        if page:
            screenshot = page.screenshot(full_page=True)

            allure.attach(
                screenshot,
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )


@pytest.fixture(scope="function")
def page():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        yield page

        context.close()
        browser.close()


@pytest.fixture(scope="function")
def mobile_page():
    with sync_playwright() as p:
        iphone_12 = p.devices['iPhone 12']
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(**iphone_12)
        page = context.new_page()

        yield page

        context.close()
        browser.close()