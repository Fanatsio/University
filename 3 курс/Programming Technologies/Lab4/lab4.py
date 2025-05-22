import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import time
from typing import Set, Deque, Tuple, Optional, Dict

class BaseURLFinder:
    def __init__(self, url: str, depth: int, max_urls: int = 5000):
        self.url = url
        self.depth = depth
        self.urls: Set[str] = set()
        self.visited: Set[str] = set()
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})
        self.max_urls = max_urls
        self.domain_limits: Dict[str, int] = {}

    def fetch_url(self, url: str) -> Optional[str]:
        domain = urlparse(url).netloc

        if self.domain_limits.get(domain, 0) > 100:
            print(f"Skipping {domain} due to request limit")
            return None

        self.domain_limits[domain] = self.domain_limits.get(domain, 0) + 1

        try:
            response = self.session.get(url, timeout=5)
            if response.status_code == 200:
                return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
        return None

    def parse_urls(self, html_content: str, base_url: str) -> Set[str]:
        if not html_content:
            return set()

        soup = BeautifulSoup(html_content, 'html.parser')
        urls_found = {urljoin(base_url, link.get('href')) for link in soup.find_all('a', href=True)}
        return {url for url in urls_found if url.startswith('http')}

    def normalize_url(self, url: str) -> str:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    def save_urls_to_file(self, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            for url in self.urls:
                f.write(url + '\n')

class NaiveURLFinder(BaseURLFinder):
    def run(self):
        queue: Deque[Tuple[str, int]] = deque([(self.url, self.depth)])
        while queue:
            current_url, current_depth = queue.popleft()
            if current_url in self.visited or current_depth == 0 or len(self.urls) >= self.max_urls:
                continue

            self.visited.add(current_url)
            html_content = self.fetch_url(current_url)
            if html_content:
                urls_found = self.parse_urls(html_content, current_url)
                for url_found in urls_found:
                    norm_url = self.normalize_url(url_found)
                    if norm_url not in self.urls:
                        print(f"Naive: {norm_url}")
                        self.urls.add(norm_url)
                        queue.append((norm_url, current_depth - 1))

class URLStateMachine(BaseURLFinder):
    class State:
        INITIAL = 'INITIAL'
        FETCHING = 'FETCHING'
        PARSING = 'PARSING'
        END = 'END'

    def __init__(self, url: str, depth: int, max_urls: int = 5000):
        super().__init__(url, depth, max_urls)
        self.state = self.State.INITIAL

    def transition(self, new_state: str):
        print(f"Transitioning to {new_state}")
        self.state = new_state

    def run(self):
        queue: Deque[Tuple[str, int]] = deque([(self.url, self.depth)])
        while queue:
            current_url, current_depth = queue.popleft()

            if self.state == self.State.INITIAL:
                if current_url in self.visited or current_depth == 0 or len(self.urls) >= self.max_urls:
                    continue

                self.visited.add(current_url)
                self.transition(self.State.FETCHING)

            if self.state == self.State.FETCHING:
                html_content = self.fetch_url(current_url)
                if html_content:
                    self.transition(self.State.PARSING)
                    queue.append((current_url, current_depth - 1))

            if self.state == self.State.PARSING:
                urls_found = self.parse_urls(html_content, current_url)
                for url_found in urls_found:
                    norm_url = self.normalize_url(url_found)
                    if norm_url not in self.urls:
                        print(f"FSM: {norm_url}")
                        self.urls.add(norm_url)
                        queue.append((norm_url, current_depth - 1))

                self.transition(self.State.INITIAL)

url = "https://en.wikipedia.org/wiki/List_of_Hindi_songs_recorded_by_Asha_Bhosle"
depth = 2

naive_finder = NaiveURLFinder(url, depth, max_urls=5000)
fsm_finder = URLStateMachine(url, depth, max_urls=5000)

start_time = time.time()
naive_finder.run()
naive_time = time.time() - start_time

start_time = time.time()
fsm_finder.run()
fsm_time = time.time() - start_time

print("-" * 20)
print(f"Naive algorithm found: {len(naive_finder.urls)} URLs in {naive_time:.2f} sec")
print(f"FSM found: {len(fsm_finder.urls)} URLs in {fsm_time:.2f} sec")
