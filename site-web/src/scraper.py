"""
CyberDailyWatch - Scraper d'actualités cybersécurité
Récupère les derniers articles de TheHackerNews.com
"""

import requests
from bs4 import BeautifulSoup

URL_SOURCE = "https://thehackernews.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
TIMEOUT = 15


def scrape_hackernews(num_articles: int = 3) -> list[dict]:
    """Récupère les dernières actualités de TheHackerNews.com."""
    try:
        response = requests.get(URL_SOURCE, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Erreur scraping: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []

    for link in soup.find_all("a", class_="story-link")[:num_articles]:
        try:
            article_url = link.get("href", "")
            title_el = link.find("h2", class_="home-title")
            if not title_el:
                continue

            title = title_el.get_text(strip=True)
            parent = link.find_parent("div", class_="body-post")
            summary = ""
            if parent:
                desc_el = parent.find("div", class_="home-desc")
                summary = desc_el.get_text(strip=True) if desc_el else ""

            if title and article_url:
                articles.append({"title": title, "url": article_url, "summary": summary})
        except Exception as e:
            print(f"⚠️ Erreur parsing article: {e}")
            continue

    return articles


if __name__ == "__main__":
    import json
    print("🔍 Test scraper...")
    news = scrape_hackernews(3)
    print(json.dumps(news, indent=2, ensure_ascii=False) if news else "❌ Aucun article")
