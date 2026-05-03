import os
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

    print(f"\nHTML Report Path: {getattr(config.option, 'htmlpath', None)}")
    print(f"Allure Results Dir: {getattr(config.option, 'allure_report_dir', None)}\n")


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
        # Apply the pre-configured device profile
        context = browser.new_context(**iphone_12)
        page = context.new_page()

        yield page

        context.close()
        browser.close()
