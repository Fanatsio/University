import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import os
import json

START_URL = "https://ru.wikipedia.org/wiki/Поисковая_система"
MAX_PAGES = 200
SAVE_DIR = "wiki_docs"
LINKS_FILE = "links.json"

os.makedirs(SAVE_DIR, exist_ok=True)
visited_urls = set()
links_mapping = {}

class WikipediaSpider(scrapy.Spider):
    name = "wiki_spider"
    start_urls = [START_URL]
    page_count = 0

    def parse(self, response):
        global visited_urls, links_mapping

        if self.page_count >= MAX_PAGES:
            return

        url = response.url
        if url in visited_urls:
            return
        visited_urls.add(url)
        self.page_count += 1

        soup = BeautifulSoup(response.text, "html.parser")
        content = soup.find("div", {"id": "mw-content-text"})
        text = content.get_text(separator=" ", strip=True) if content else ""

        title = soup.find("h1").get_text()

        filename = f"page_{self.page_count}.txt"
        file_path = os.path.join(SAVE_DIR, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)

        links_mapping[filename] = {"title": title, "url": url}
        with open(LINKS_FILE, "w", encoding="utf-8") as f:
            json.dump(links_mapping, f, ensure_ascii=False, indent=4)

        links = [a["href"] for a in soup.select("a[href^='/wiki/']") if ":" not in a["href"]]
        for link in links:
            full_link = response.urljoin(link)
            if full_link not in visited_urls and self.page_count < MAX_PAGES:
                yield scrapy.Request(full_link, callback=self.parse)

process = CrawlerProcess(settings={"LOG_LEVEL": "INFO"})
process.crawl(WikipediaSpider)
process.start()
