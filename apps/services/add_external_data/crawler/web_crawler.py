import html2text
import httpx
from bs4 import BeautifulSoup
import asyncio

class WebCrawler:
    def __init__(self):
        self.visited_urls = set()

    def fetch_content_sync(self, url: str) -> str:
        response = httpx.get(url)
        return response.text

    async def fetch_content_async(self, url: str) -> str:
        response = await httpx.get(url)
        return response.text

    def get_pure_text_content(self, html_content: str) -> str:
        soup = BeautifulSoup(html_content, 'html.parser')

        # 找到所有的图片标签并移除
        for img in soup.body.find_all('img'):
            img.decompose()

        body_elements = soup.body.find_all()
        h = html2text.HTML2Text()
        return h.handle(body_elements)
        # print(f"body_elements: {body_elements}")
        # text_content = ""
        # for element in body_elements:
        #     # 如果是链接标签，保留其内容
        #     if element.name == 'a':
        #         text_content += element.get_text()
        #     else:
        #         text_content += element.get_text(strip=True) + " "

    def parse_suburls(self, content: str) -> list[str]:
        soup = BeautifulSoup(content, 'html.parser')
        suburls = [a['href'] for a in soup.find_all('a', href=True)]
        return suburls

    def crawl_sync(self, url: str) -> list[str]:
        if url in self.visited_urls:
            return []
        self.visited_urls.add(url)
        content = self.fetch_content_sync(url)
        if content is None:
            return []
        suburls = self.parse_suburls(content)
        all_contents = [content]
        for suburl in suburls:
            sub_content = self.crawl_sync(suburl)
            if sub_content:
                all_contents.extend(sub_content)
        return all_contents

    async def crawl_async(self, url: str) -> list[str]:
        if url in self.visited_urls:
            return []
        self.visited_urls.add(url)
        content = await self.fetch_content_async(url)
        if content is None:
            return []
        suburls = self.parse_suburls(content)
        all_contents = [content]
        tasks = [self.crawl_async(suburl) for suburl in suburls]
        sub_contents = await asyncio.gather(*tasks)
        for sub_content in sub_contents:
            if sub_content:
                all_contents.extend(sub_content)
        return all_contents

    def split_content(self, content: str, length: int) -> list[str]:
        chunks = []
        for i in range(0, len(content), length):
            chunks.append(content[i:i + length])
        return chunks

# # 使用同步方法
# crawler = WebCrawler()
# contents = crawler.crawl_sync('http://example.com')

# # 使用异步方法
# async def main():
#     crawler = WebCrawler()
#     contents = await crawler.crawl_async('http://example.com')
#     print(contents)

# # 运行异步主函数
# asyncio.run(main())