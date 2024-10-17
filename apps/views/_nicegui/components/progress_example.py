#!/usr/bin/env python3
import asyncio
import time
import re
import requests
import markdown
from multiprocessing import Manager
from queue import Empty, Queue
from typing import Callable, Generator

from nicegui import app, background_tasks, run, ui


class Worker:

    def __init__(self) -> None:
        self._queue: Queue
        self.progress: float = 0.0
        self.is_running: bool = False

        app.on_startup(self._create_queue)

    async def run(self, func: Callable[..., Generator[float, None, None]]) -> None:
        background_tasks.create(run.cpu_bound(self._run_generator, func, self._queue))
        background_tasks.create(self._consume_queue())

    @staticmethod
    def _run_generator(func: Callable[..., Generator[float, None, None]], queue: Queue) -> None:
        for progress in func():
            queue.put({'progress': progress})
        queue.put({'progress': 1.0})

    def _create_queue(self) -> None:
        self._queue = Manager().Queue()

    async def _consume_queue(self) -> None:
        self.is_running = True
        self.progress = 0.0
        while self.progress < 1.0:
            try:
                msg = self._queue.get_nowait()
            except Empty:
                await asyncio.sleep(0.1)
                continue
            self.progress = msg['progress']
        self.is_running = False


def crawl_and_process(url, is_sub_url=False):
    # 步骤 1：爬取指定 URL 的内容并解析页面获取子 URL
    response = requests.get(url)
    html_content = response.text
    if is_sub_url:
        # 如果是子 URL，不再处理其中的 URL
        sub_urls = []
    else:
        # 这里假设使用简单的正则表达式来提取子 URL，实际应用中可根据具体情况调整
        sub_urls = [u for u in re.findall(r'https?://[^\s]+', html_content) if u!= url]
    # 步骤 2：HTML 转 Markdown 并定长分段
    markdown_content = markdown.markdown(html_content)
    text_splitter = split_text(markdown_content)
    chunks = [chunk for chunk in text_splitter]
    # 步骤 3：将分段列表调用 embedding 函数并保存成本地向量
    # 这里使用假函数模拟 embedding
    fake_embed(chunks)
    progress = 0.3 if is_sub_url else 0.5
    yield progress
    if not is_sub_url and sub_urls:
        sub_progress = 0
        total_sub_urls = len(sub_urls)
        for index, sub_url in enumerate(sub_urls):
            # 处理子 URL
            crawl_and_process(sub_url, is_sub_url=True)
            sub_progress = (index + 1) / total_sub_urls * 0.5
            yield progress + sub_progress
    else:
        yield 1.0


def split_text(text):
    # 简单的文本分割函数，将文本分割成长度为 1024 的块
    chunks = []
    for i in range(0, len(text), 1024):
        chunks.append(text[i:i + 1024])
    return chunks


def fake_embed(chunks):
    # 假的 embedding 函数，仅打印信息
    for chunk in chunks:
        print(f"Fake embedding for chunk: {chunk}")


worker = Worker()


@ui.page('/')
def main_page():
    with ui.linear_progress(show_value=False, size='2em').props('instant-feedback') as progress_bar:
        label = ui.label('test') \
          .classes('text-lg text-black absolute-center') \
          .bind_text_from(worker, 'progress', backward=lambda v: f'Making progress... {v:.1%}')
    ui.button('compute', on_click=lambda: worker.run(crawl_and_process('https://example.com')))
    progress_bar.bind_value_from(worker, 'progress')


ui.run()