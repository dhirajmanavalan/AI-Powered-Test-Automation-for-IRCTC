from playwright.sync_api import expect

def test_screenshot_demo(page):

    page.goto(
        "https://www.irctc.co.in/nget/train-search"
    )

    expect(page).to_have_title(
        "Google"
    )