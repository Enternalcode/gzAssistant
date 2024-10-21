from nicegui import ui

@ui.page('/qa')
async def faq_page():
    # https://nicegui.io/documentation/section_pages_routing
    ui.label('FAQ')