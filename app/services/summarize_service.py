# services/summarize_service.py
from newspaper import Article
import requests
from app.core.config import openai_client
from bs4 import BeautifulSoup  # optional for fallback cleaning

import nltk
nltk.download("punkt", quiet=True)

def fetch_article(url: str) -> str:
    headers = {"User-Agent":
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    res = requests.get(url, headers=headers, timeout=15)
    res.raise_for_status()
    art = Article(url)
    art.set_html(res.text)
    art.parse()
    return art.text

def summarize(url: str) -> str:
    text = fetch_article(url)
    prompt = f"以下の文章を日本語で3行に要約してください：\n\n{text}"
    resp = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip()
