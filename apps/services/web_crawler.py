import requests
from bs4 import BeautifulSoup

class WebCrawler:
    def __init__(self):
        self.visited_urls = set()

    def fetch_content(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_suburls(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        suburls = [a['href'] for a in soup.find_all('a', href=True)]
        return suburls

    def crawl(self, url):
        if url in self.visited_urls:
            return []
        self.visited_urls.add(url)
        content = self.fetch_content(url)
        if content is None:
            return []
        suburls = self.parse_suburls(content)
        all_contents = [content]
        for suburl in suburls:
            sub_content = self.crawl(suburl)
            if sub_content:
                all_contents.extend(sub_content)
        return all_contents

    def split_content(self, content, length):
        chunks = []
        for i in range(0, len(content), length):
            chunks.append(content[i:i + length])
        return chunks