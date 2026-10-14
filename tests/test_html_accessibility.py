"""
Test Suite: Frontend WCAG 2.1 AA Accessibility & HTML Semantic Landmark Compliance.
"""

from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent

HTML_FILES = [
    "index.html",
    "incident-intelligence.html",
    "resolution-verification.html",
    "public-transparency.html"
]


def test_html_files_exist():
    for f in HTML_FILES:
        path = WORKSPACE / f
        assert path.exists(), f"Missing HTML file: {f}"


def test_html_accessibility_and_seo_requirements():
    for f in HTML_FILES:
        content = (WORKSPACE / f).read_text(encoding="utf-8")

        # 1. DOCTYPE and HTML lang
        assert "<!DOCTYPE html>" in content, f"{f} missing <!DOCTYPE html>"
        assert 'lang="en"' in content, f"{f} missing lang='en'"

        # 2. Document title & meta description
        assert "<title>" in content, f"{f} missing <title>"
        assert 'name="description"' in content, f"{f} missing meta description"
        assert 'name="viewport"' in content, f"{f} missing viewport meta"

        # 3. Skip to main content link
        assert 'class="skip-link"' in content, f"{f} missing accessible skip-to-content link"
        assert 'href="#main-content"' in content, f"{f} skip-link must target #main-content"

        # 4. Semantic landmarks
        assert 'role="banner"' in content, f"{f} missing role='banner' header"
        assert 'id="main-content"' in content, f"{f} missing id='main-content'"
        assert 'role="main"' in content, f"{f} missing role='main'"
        assert 'role="navigation"' in content, f"{f} missing role='navigation'"

        # 5. Images must have non-empty alt text and NOT data-alt
        assert 'data-alt="' not in content, f"{f} contains illegal data-alt attribute instead of alt"
        assert 'alt=""' not in content, f"{f} has empty alt attribute"

        # 6. Buttons & Notifications accessibility
        assert 'aria-label="Operational alerts' in content, f"{f} missing operational alerts aria-label"
