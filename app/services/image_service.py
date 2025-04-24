# services/image_service.py
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

def extract_images(url: str) -> list[str]:
    headers = {"User-Agent":
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    res = requests.get(url, headers=headers, timeout=15)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    imgs = [urljoin(url, tag["src"])
            for tag in soup.find_all("img") if tag.get("src")]

    og = soup.find("meta", property="og:image")
    if og and og.get("content"):
        imgs.append(urljoin(url, og["content"]))
    return list(set(imgs))
