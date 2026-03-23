"""Playwright diagnostic script to investigate Enter key behavior in the Streamlit guessing game."""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print("=== Navigating to app ===")
    page.goto("http://localhost:8501")
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Check what input elements exist
    print("\n=== Input elements on page ===")
    inputs = page.query_selector_all("input")
    for i, inp in enumerate(inputs):
        print(f"  [{i}] type={inp.get_attribute('type')!r}  "
              f"placeholder={inp.get_attribute('placeholder')!r}  "
              f"aria-label={inp.get_attribute('aria-label')!r}")

    # Find the guess input
    guess_input = page.query_selector("input[aria-label='Enter your guess:']")
    if not guess_input:
        # fallback: first text input
        guess_input = page.query_selector("input[type='text'], input:not([type])")

    if not guess_input:
        print("\nERROR: Could not find the guess input field!")
        browser.close()
        exit(1)

    print(f"\n=== Found guess input ===")
    print(f"  aria-label: {guess_input.get_attribute('aria-label')!r}")
    print(f"  placeholder: {guess_input.get_attribute('placeholder')!r}")

    # --- Test 1: type a value and press Enter ---
    print("\n=== Test 1: Type '42' then press Enter ===")

    # Capture network requests to detect Streamlit websocket messages
    history_before = page.query_selector_all("[data-testid='stText'], .stAlert, [data-testid='stAlert']")
    alerts_before = [el.inner_text() for el in history_before]
    print(f"  Alerts/messages before: {alerts_before}")

    guess_input.click()
    guess_input.fill("42")
    page.keyboard.press("Enter")
    time.sleep(2)  # wait for potential rerun

    history_after = page.query_selector_all("[data-testid='stText'], .stAlert, [data-testid='stAlert']")
    alerts_after = [el.inner_text() for el in history_after]
    print(f"  Alerts/messages after Enter: {alerts_after}")

    # Check attempts counter to see if a guess was processed
    info_boxes = page.query_selector_all("[data-testid='stInfo'], .stAlert")
    for box in info_boxes:
        print(f"  Info box: {box.inner_text()!r}")

    # --- Test 2: type a value and click Submit ---
    print("\n=== Test 2: Type '43' then click Submit button ===")
    guess_input.click()
    guess_input.fill("43")

    submit_btn = page.query_selector("button:has-text('Submit Guess')")
    if submit_btn:
        submit_btn.click()
        time.sleep(2)
        history_click = page.query_selector_all("[data-testid='stText'], .stAlert, [data-testid='stAlert']")
        alerts_click = [el.inner_text() for el in history_click]
        print(f"  Alerts/messages after button click: {alerts_click}")
        info_boxes2 = page.query_selector_all("[data-testid='stInfo'], .stAlert")
        for box in info_boxes2:
            print(f"  Info box: {box.inner_text()!r}")
    else:
        print("  ERROR: Could not find Submit Guess button!")

    # --- Inspect the form/input DOM structure ---
    print("\n=== DOM structure around the guess input ===")
    dom_snippet = page.evaluate("""() => {
        const inp = document.querySelector("input[aria-label='Enter your guess:']")
            || document.querySelector("input[type='text']");
        if (!inp) return 'INPUT NOT FOUND';
        // Walk up to find form ancestor
        let el = inp;
        let path = [];
        for (let i = 0; i < 8; i++) {
            if (!el) break;
            path.push(el.tagName + (el.getAttribute('data-testid') ? '['+el.getAttribute('data-testid')+']' : ''));
            el = el.parentElement;
        }
        const inForm = !!inp.closest('form');
        return {
            path: path.join(' > '),
            inForm: inForm,
            formAction: inp.closest('form') ? inp.closest('form').getAttribute('action') : null,
        };
    }""")
    print(f"  {dom_snippet}")

    browser.close()
    print("\n=== Done ===")
