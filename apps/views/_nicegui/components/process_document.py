import asyncio
from nicegui import ui

async def fetch_main_document():
    await asyncio.sleep(1)
    return "<html><body>Main content with <a href='subpage1'>link1</a> and <a href='subpage2'>link2</a></body></html>"

async def parse_document(html=None):
    await asyncio.sleep(1)
    return ["Segment 1", "Segment 2"]

async def extract_sub_urls(html=None):
    await asyncio.sleep(1)
    return ["subpage1", "subpage2"]

async def fetch_sub_document(url):
    await asyncio.sleep(1)
    return f"<html><body>Content of {url}</body></html>"

async def process_sub_url(url, progress, progress_increment):
    await fetch_sub_document(url)
    await parse_document(url)
    progress.set_value(progress.get_value() + progress_increment)

async def process_document():
    progress = ui.linear_progress(0)
    status = ui.label("Starting...")

    steps = [
        (fetch_main_document, "Fetching main document..."),
        (parse_document, "Parsing main document..."),
        (extract_sub_urls, "Extracting sub URLs...")
    ]

    total_steps = len(steps)
    for i, (task, message) in enumerate(steps):
        status.set_text(message)
        await task()
        progress.set_value((i + 1) / total_steps)

    sub_urls = await extract_sub_urls(await fetch_main_document())
    progress_increment = 1 / (len(sub_urls) + total_steps)

    await asyncio.gather(*(process_sub_url(url, progress, progress_increment) for url in sub_urls))

    status.set_text("All tasks completed.")
    progress.set_value(1.0)

ui.button("Start Task", on_click=process_document)

ui.run(show=False, reload=False, title="PyInstaller Test")