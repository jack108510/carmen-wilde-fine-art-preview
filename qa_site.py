"""Prelaunch static and browser checks. Run against a local `python3 -m http.server 8766`."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
from bs4 import BeautifulSoup
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent
BASE = "http://127.0.0.1:8766/"
PAGES = sorted(ROOT.rglob("*.html"))
problems = []
for page in PAGES:
    soup = BeautifulSoup(page.read_text(), "html.parser")
    if len(soup.select("h1")) != 1:
        problems.append(f"{page.name}: expected one h1")
    if not soup.select_one('meta[name="robots"][content="noindex,nofollow"]'):
        problems.append(f"{page.name}: staging robots directive missing")
    for el, attr in (("a", "href"), ("img", "src"), ("link", "href")):
        for node in soup.select(f"{el}[{attr}]"):
            value = node[attr]
            if value.startswith(("https:", "http:", "mailto:", "tel:", "#", "data:")):
                continue
            local = page.parent / unquote(urlsplit(value).path)
            if not local.exists():
                problems.append(f"{page.relative_to(ROOT)}: missing {value}")
for asset in (ROOT / "assets").rglob("*.webp"):
    try:
        with Image.open(asset) as image:
            image.verify()
    except Exception as exc:
        problems.append(f"{asset.relative_to(ROOT)}: {exc}")

chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path=chrome, headless=True)
    for width in (390, 768, 1440):
        tab = browser.new_page(viewport={"width": width, "height": 900})
        errors = []
        tab.on("pageerror", lambda error: errors.append(str(error)))
        for page in PAGES:
            relative = page.relative_to(ROOT).as_posix()
            response = tab.goto(BASE + relative, wait_until="domcontentloaded")
            if response.status != 200:
                problems.append(f"{relative}: HTTP {response.status}")
            overflow = tab.evaluate("document.documentElement.scrollWidth > innerWidth")
            if overflow:
                problems.append(f"{relative}: horizontal overflow at {width}px")
            for error in errors:
                problems.append(f"{relative}: JS {error}")
            errors.clear()
        tab.goto(BASE + "contact.html?subject=Commission%20inquiry")
        tab.locator('input[name="name"]').fill("Website QA")
        tab.locator('input[name="email"]').fill("qa@example.invalid")
        tab.locator('textarea[name="message"]').fill("Test message")
        if not tab.locator("#contact-form").evaluate("el => el.checkValidity()"):
            problems.append(f"contact: form validation failed at {width}px")
        cdp = tab.context.new_cdp_session(tab)
        navigations = []
        cdp.on("Page.frameRequestedNavigation", lambda event: navigations.append(event["url"]))
        cdp.send("Page.enable")
        tab.locator('#contact-form button').click()
        tab.wait_for_timeout(200)
        if not any(url.startswith('mailto:cwildedesigns@shaw.ca?') and 'Commission%20inquiry' in url and 'Test%20message' in url for url in navigations):
            problems.append(f"contact: mailto compose failed at {width}px")
        if width <= 900:
            tab.goto(BASE)
            toggle = tab.locator(".menu-toggle")
            toggle.click()
            if not tab.locator(".nav").is_visible() or toggle.get_attribute("aria-expanded") != "true":
                problems.append(f"mobile menu did not open at {width}px")
        tab.close()
    browser.close()
print(f"Checked {len(PAGES)} pages × 3 viewports, local links, images, menu and form validation")
print("Problems:", len(problems))
for problem in problems[:50]:
    print("-", problem)
raise SystemExit(bool(problems))
