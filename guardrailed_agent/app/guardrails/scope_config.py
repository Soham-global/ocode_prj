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

BLOCKED_KEYWORDS = [
    "bypass captcha", "break captcha", "crack captcha", "solve captcha for free",
    "bypass paywall", "hack", "illegal", "without permission",
    "ddos", "exploit", "steal data", "credential stuffing",
    "diagnosis", "medical advice", "symptom", "lawsuit", "legal advice for me",
    "who should i vote", "election", "political opinion",
    "my relationship", "therapy", "depressed", "medication",
    "leetcode", "algorithm complexity", "machine learning model",
    "build a website", "frontend framework", "react component",
    "database design", "sql query optimization",
    "how are you", "what's up", "tell me a joke", "who are you",
    "good morning", "good evening", "thank you", "thanks",
]

REJECTION_REASON_OUT_OF_SCOPE = "Topic not allowed by agent guardrails"
REJECTION_REASON_AMBIGUOUS = "Request is ambiguous or unclear; rejected as out of scope"
REJECTION_REASON_BLOCKED = "Request involves disallowed or unethical/illegal content"
