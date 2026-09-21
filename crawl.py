from urllib.parse import urlsplit
from bs4 import BeautifulSoup, Tag

def normalize_url(url:str)-> str:
    split_url = urlsplit(url)
    normalized_url = split_url.netloc + split_url.path.rstrip(" /")
    return normalized_url

def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    heading = soup.find("h1") or soup.find("h2")
    heading_text: str = heading.get_text(strip=True) if isinstance(heading, Tag) else ""
    return heading_text


def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    paragraph = soup.find("main").find("p") if soup.find("main") else soup.find("p")
    paragraph_text: str = paragraph.get_text(strip=True) if isinstance(paragraph, Tag) else ""
    print(f"DEBUG A: {paragraph_text}")
    return paragraph_text