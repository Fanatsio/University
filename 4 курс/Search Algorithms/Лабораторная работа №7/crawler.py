import requests
from bs4 import BeautifulSoup
from collections import deque
import re
from urllib.parse import urlparse

class WebCrawler:
    """Handles web crawling to fetch page content and links."""
    
    def __init__(self, max_depth=2, max_pages=150, timeout=5):
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.timeout = timeout
        self.allowed_domain = "ru.wikipedia.org"  # Restrict crawling to this domain

    def clean_text(self, soup):
        """Remove script/style tags and normalize text."""
        for s in soup(['script', 'style']):
            s.decompose()
        return re.sub(r'\s+', ' ', soup.get_text(separator=' ')).strip()

    def crawl(self, seed_urls):
        """Crawl web pages starting from seed URLs."""
        visited = set()
        docs_content = {}
        adj_list = {}
        queue = deque([(url, 0) for url in seed_urls])

        while queue and len(docs_content) < self.max_pages:
            current_url, depth = queue.popleft()
            if current_url in visited or depth > self.max_depth:
                continue
            visited.add(current_url)

            try:
                resp = requests.get(current_url, timeout=self.timeout)
                if resp.status_code != 200:
                    continue
                html = resp.text
            except requests.RequestException:
                continue

            soup = BeautifulSoup(html, 'html.parser')
            text = self.clean_text(soup)
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else current_url

            docs_content[current_url] = {"title": title, "text": text}
            links_on_page = set()

            for link_tag in soup.find_all('a', href=True):
                href = link_tag['href']
                full_link = requests.compat.urljoin(current_url, href)
                full_link = re.split(r'#|\?', full_link)[0]
                if full_link.startswith('http'):
                    # Check if the link belongs to the allowed domain
                    parsed_url = urlparse(full_link)
                    if parsed_url.netloc == self.allowed_domain:
                        links_on_page.add(full_link)
                        if full_link not in visited:
                            queue.append((full_link, depth + 1))

            adj_list[current_url] = list(links_on_page)

        return docs_content, adj_list