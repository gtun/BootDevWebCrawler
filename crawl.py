from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup, Tag
from typing import TypedDict

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

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
    return paragraph_text


def get_urls_from_html(html, base_url) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")
    anchor_tags = soup.find_all("a")
    href_list = []

    for anchor_tag in anchor_tags:
        href = anchor_tag.get("href")
        if href is None:
            raise ValueError("anchor tag has no href attribute")
        href_list.append(urljoin(base_url, href))
        
    return href_list

def get_images_from_html(html, base_url) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")
    img_tags = soup.find_all("img")
    src_list = []

    for img_tag in img_tags:
        src = img_tag.get("src")
        if src is None:
            raise ValueError("img has no src attribute")
        src_list.append(urljoin(base_url, src))
    return src_list

def extract_page_data(html: str, pageurl: str) -> dict:
    page_data: PageData = {
        "url": pageurl,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, pageurl),
        "image_urls": get_images_from_html(html, pageurl)
    }
    
    return page_data