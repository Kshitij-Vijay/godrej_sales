import os
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from tkinter import simpledialog, Tk
from playwright.sync_api import sync_playwright

EXTRACTED_FOLDER = "extracted_data"
TEXT_FOLDER = os.path.join(EXTRACTED_FOLDER, "texts")
IMAGES_FOLDER = os.path.join(EXTRACTED_FOLDER, "images")
PDFS_FOLDER = os.path.join(EXTRACTED_FOLDER, "pdfs")
LINKS_FOLDER = os.path.join(EXTRACTED_FOLDER, "links")

def ensure_folders():
    os.makedirs(TEXT_FOLDER, exist_ok=True)
    os.makedirs(IMAGES_FOLDER, exist_ok=True)
    os.makedirs(PDFS_FOLDER, exist_ok=True)
    os.makedirs(LINKS_FOLDER, exist_ok=True)

def download_file(url, folder, filename=None):
    try:
        r = requests.get(url)
        r.raise_for_status()
        if not filename:
            filename = os.path.basename(urlparse(url).path)
            if not filename:
                filename = "downloaded_file"
        path = os.path.join(folder, filename)
        with open(path, "wb") as f:
            f.write(r.content)
        print(f"Downloaded {url} to {path}")
        return path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def scrape_url(url):
    ensure_folders()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state("networkidle", timeout=60000)
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    # Extract from maincontent only: images, PDFs, all links
    maincontent = soup.find(id="maincontent")
    if not maincontent:
        print("No element with id 'maincontent' found.")
        maincontent = soup  # fallback to whole page

    images = []
    for img in maincontent.find_all("img"):
        src = img.get("src")
        if not src:
            continue
        img_url = urljoin(url, src)
        img_path = download_file(img_url, IMAGES_FOLDER)
        if img_path:
            images.append(img_url)

    pdfs = []
    for a in maincontent.find_all("a", href=True):
        href = a['href']
        if href.lower().endswith(".pdf"):
            pdf_url = urljoin(url, href)
            pdf_path = download_file(pdf_url, PDFS_FOLDER)
            if pdf_path:
                pdfs.append(pdf_url)

    all_links_list = [urljoin(url, a['href']) for a in maincontent.find_all("a", href=True)]

    # Extract full text from specific tabs by id
    tab_ids = [
        "tab-specifications",
        "tab-additionalinformation",
        "tab-materials",
        "tab-godrejcareinstructions"
    ]

    combined_sections = []

    for tab_id in tab_ids:
        tab_element = soup.find(id=tab_id)
        if not tab_element:
            combined_sections.append(f"=== {tab_id} ===\nNo element with id '{tab_id}' found.")
        else:
            full_text = tab_element.get_text(separator="\n", strip=True)
            combined_sections.append(f"=== {tab_id} ===\n{full_text}")

    # Extract all text from class 'slider-description'
    slider_elements = soup.find_all(class_="slider-description")
    for i, elem in enumerate(slider_elements, 1):
        text = elem.get_text(separator="\n", strip=True)
        combined_sections.append(f"=== slider-description {i} ===\n{text}")

    # Optional: add links/PDFs/images summary at the end for completeness
    combined_sections.append("=== Images Extracted ===\n" + "\n".join(images))
    combined_sections.append("=== PDFs Extracted ===\n" + "\n".join(pdfs))
    combined_sections.append("=== Maincontent Links Extracted ===\n" + "\n".join(all_links_list))

    # Save combined content into a single text file
    combined_filename = os.path.join(TEXT_FOLDER, "combined_content.txt")
    with open(combined_filename, "w", encoding="utf-8") as f:
        f.write("\n\n".join(combined_sections))
    print(f"Saved all combined content to {combined_filename}")

    # Save all links info from maincontent as JSON (unchanged)
    all_links = {
        "page_url": url,
        "images": images,
        "pdfs": pdfs,
        "all_links": all_links_list
    }
    links_path = os.path.join(LINKS_FOLDER, "links.json")
    with open(links_path, "w", encoding="utf-8") as f:
        json.dump(all_links, f, indent=2)
    print(f"Saved links info to {links_path}")

def get_url_from_user():
    root = Tk()
    root.withdraw()
    url = simpledialog.askstring(title="Input", prompt="Enter the URL to scrape:")
    root.destroy()
    return url

def handle_url():
    url = get_url_from_user()
    if url:
        print(f"Scraping URL: {url}")
        scrape_url(url)
    else:
        print("No URL provided.")

if __name__ == "__main__":
    handle_url()
