import os
from datetime import datetime

import allure
import pytest
from playwright.sync_api import sync_playwright


def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """
    Creates timestamped pytest-html report,
    Allure results folder,
    and Screenshots folder.
    """

    timestamp = get_timestamp()

    reports_dir = os.path.join(
        os.getcwd(),
        "reports"
    )

    html_reports_dir = os.path.join(
        reports_dir,
        "html"
    )

    screenshots_dir = os.path.join(
        reports_dir,
        "screenshots"
    )

    allure_results_dir = os.path.join(
        reports_dir,
        "allure-results",
        f"run_{timestamp}"
    )

    os.makedirs(
        html_reports_dir,
        exist_ok=True
    )

    os.makedirs(
        screenshots_dir,
        exist_ok=True
    )

    os.makedirs(
        allure_results_dir,
        exist_ok=True
    )

    # pytest-html report path
    if hasattr(config.option, "htmlpath"):
        config.option.htmlpath = os.path.join(
            html_reports_dir,
            f"API_Test_Report_{timestamp}.html"
        )

    # allure result directory
    if hasattr(config.option, "allure_report_dir"):
        config.option.allure_report_dir = allure_results_dir

    print(
        f"\nHTML Report Path: "
        f"{getattr(config.option, 'htmlpath', None)}"
    )

    print(
        f"Allure Results Dir: "
        f"{getattr(config.option, 'allure_report_dir', None)}\n"
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Save screenshot + attach to Allure
    whenever a test fails.
    """

    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        page = item.funcargs.get("page")

        if page:

            screenshots_dir = os.path.join(
                os.getcwd(),
                "reports",
                "screenshots"
            )

            os.makedirs(
                screenshots_dir,
                exist_ok=True
            )

            screenshot_path = os.path.join(
                screenshots_dir,
                f"{item.name}.png"
            )

            page.screenshot(
                path=screenshot_path,
                full_page=True
            )

            with open(
                screenshot_path,
                "rb"
            ) as screenshot_file:

                allure.attach(
                    screenshot_file.read(),
                    name=item.name,
                    attachment_type=allure.attachment_type.PNG
                )

            print(
                f"\nScreenshot saved: {screenshot_path}"
            )


@pytest.fixture(scope="function")
def page():

    with sync_playwright() as playwright:
        headless_mode = bool(
            os.getenv("RAILWAY_ENVIRONMENT")
        )

        browser = playwright.chromium.launch(
            headless=headless_mode
        )

        context = browser.new_context()

        page = context.new_page()

        yield page

        context.close()
        browser.close()


@pytest.fixture(scope="function")
def mobile_page():

    with sync_playwright() as playwright:

        iphone_12 = playwright.devices["iPhone 12"]

        headless_mode = bool(
            os.getenv("RAILWAY_ENVIRONMENT")
        )

        browser = playwright.chromium.launch(
            headless=headless_mode
        )

        context = browser.new_context(
            **iphone_12
        )

        page = context.new_page()

        yield page

        context.close()
        browser.close()