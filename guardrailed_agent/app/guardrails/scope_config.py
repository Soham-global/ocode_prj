"""
Scope configuration for the Guardrailed AI Agent.

This module defines the ALLOWED topics, BLOCKED/disallowed topics, and
keyword sets used by the programmatic guardrail (scope_checker.py) to
decide whether an incoming query is in-scope or out-of-scope.

Per assignment requirements:
- Guardrails must be enforced programmatically (not just via prompts).
- The system must fail closed: if unsure, REJECT.
"""

# -----------------------------------------------------------------------
# Allowed scope description (returned by GET /agent/scope)
# -----------------------------------------------------------------------
ALLOWED_SCOPE = {
    "topics": [
        "Web scraping concepts",
        "JavaScript-rendered websites",
        "CAPTCHA detection and high-level handling strategies (no illegal bypass)",
        "Headless browsers used for scraping",
        "Ethical and legal considerations of web scraping",
    ],
    "response_style": "High-level and explanatory only",
}

# -----------------------------------------------------------------------
# Keywords that indicate a query IS likely about web scraping (in-scope)
# These are used as positive signals.
# -----------------------------------------------------------------------
ALLOWED_KEYWORDS = [
    "scrape", "scraping", "scraper", "crawler", "crawling",
    "headless browser", "headless", "playwright", "selenium", "puppeteer",
    "javascript-rendered", "js-rendered", "dynamic content", "dom",
    "captcha", "recaptcha", "rate limit", "rate limiting",
    "robots.txt", "user agent", "proxy", "proxies",
    "web scraping", "data extraction", "html parsing",
    "ethical scraping", "legal scraping", "terms of service",
    "anti-bot", "anti-scraping", "render", "rendering",
]

# -----------------------------------------------------------------------
# Keywords/phrases that indicate the query is explicitly OUT OF SCOPE,
# even if it superficially mentions an allowed keyword.
# These take priority over ALLOWED_KEYWORDS (fail closed).
# -----------------------------------------------------------------------
BLOCKED_KEYWORDS = [
    # Illegal / unethical bypass requests
    "bypass captcha", "break captcha", "crack captcha", "solve captcha for free",
    "bypass paywall", "hack", "illegal", "without permission",
    "ddos", "exploit", "steal data", "credential stuffing",

    # Personal / medical / legal / political
    "diagnosis", "medical advice", "symptom", "lawsuit", "legal advice for me",
    "who should i vote", "election", "political opinion",
    "my relationship", "therapy", "depressed", "medication",

    # General programming / unrelated tech (non-scraping)
    "leetcode", "algorithm complexity", "machine learning model",
    "build a website", "frontend framework", "react component",
    "database design", "sql query optimization",

    # Casual conversation / greetings
    "how are you", "what's up", "tell me a joke", "who are you",
    "good morning", "good evening", "thank you", "thanks",
]

# -----------------------------------------------------------------------
# Standard rejection reason strings
# -----------------------------------------------------------------------
REJECTION_REASON_OUT_OF_SCOPE = "Topic not allowed by agent guardrails"
REJECTION_REASON_AMBIGUOUS = "Request is ambiguous or unclear; rejected as out of scope"
REJECTION_REASON_BLOCKED = "Request involves disallowed or unethical/illegal content"