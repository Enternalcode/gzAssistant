from nicegui import ui
from apps.services.slm.slm_service import SlmService
from apps.services.wechat_automation.wechat_auto_responder import WeChatAutoResponder
from apps.utils.common import Models, check_health, download_file, kill_llama_servers, run_llama_server
from apps.views._nicegui.components.document_input import document_input
from apps.services.log_service import clogger
from contextlib import contextmanager
import asyncio

DEBUG = True

ai_service = SlmService(
    base_url="http://127.0.0.1:8866",
    api_key="no key",
    logger=clogger
)

@contextmanager
def disable(button: ui.button):
    button.disable()
    try:
        yield
    finally:
        button.enable()

async def start_slm_services(button: ui.button):
    with disable(button):
        run_llama_server(run_in_background=True)
        clogger.info("启动AI服务")

def stop_all_models():
    kill_llama_servers()
    clogger.info("已停止所有模型")

async def check_slm_service(button: ui.button, user_content: str) -> None:
    with disable(button):
        messages = [
            {"role": "system", "content": "You are guangzhi"},
            {"role": "user", "content": user_content}
        ]
        res = await ai_service.chat_async(messages=messages)
        clogger.info(res)

async def check_embed_service(button: ui.button, user_content: str) -> None:
    with disable(button):
        res = await ai_service.embeddings_async(input_data=[user_content])
        clogger.info(res)
        clogger.info(len(res))

def get_preview_slm_question():
    return {"value": "hi"}

async def start_listening(button: ui.button):
    with disable(button):
        auto_responder  = WeChatAutoResponder()
        auto_responder.locate_group_and_check_keyword('arm64创新应用小赛', '@黑神话广智')
        ui.notify("启动成功，开始监听", type="positive")
        await asyncio.sleep(0.5)

def main_content():
    with ui.stepper().props("vertical").classes("w-full") as stepper:
        with ui.step("配置AI模型"):
            with ui.row():
                with ui.column():
                    ui.label("为保证最优使用效果, 请使用专门为本软件优化的模型。").classes("text-gray-400")
                    ui.label("请将本软件附带的models文件, 拷贝到指定文件夹下：`C:\\GZAssistantAppData`").classes("text-gray-400")
            with ui.stepper_navigation():
                ui.button("下一步", on_click=stepper.next)
        with ui.step("启动本地AI"):
            with ui.column():
                with ui.row():
                    ui.button("启动AI", on_click=lambda e: start_slm_services(e.sender))
                    ui.button("停止AI", on_click=stop_all_models)
            with ui.stepper_navigation():
                ui.button("下一步", on_click=stepper.next)
                ui.button("上一步", on_click=stepper.previous).props("flat")
        with ui.step("输入文档地址"):
            document_input().classes("w-full py-6")
            with ui.stepper_navigation():
                ui.button("下一步", on_click=stepper.next)
                ui.button("上一步", on_click=stepper.previous).props("flat")
        with ui.step("AI爬取并学习文档内容"):
            ui.button("开始训练AI")
            ui.spinner(size='lg')
            with ui.stepper_navigation():
                ui.button("下一步", on_click=stepper.next)
                ui.button("上一步", on_click=stepper.previous).props("flat")         
        with ui.step("开始运行"):
            ui.label("预览与AI进行对话").classes("text-gray-400")
            with ui.row():
                chat_input = ui.input().bind_value(get_preview_slm_question()).props(
                        "rounded outlined dense",
                ).classes("w-64")
                ui.button(
                    "发送",
                    on_click=lambda e: check_slm_service(e.sender, chat_input.value)
                )
                if DEBUG:
                    ui.button(
                        "向量化",
                        on_click=lambda e: check_embed_service(e.sender, chat_input.value)
                    )
            with ui.row():
                ui.button("运行程序", on_click=lambda e: start_listening(e.sender))
            with ui.stepper_navigation():
                
                ui.button("上一步", on_click=stepper.previous).props("flat")


    # 运行日志模块
    run_log_view = ui.log(max_lines=100).classes("w-full h-100")
    clogger.add_log_view(run_log_view)
    clogger.info("我来助你~")


@ui.page("/")
def main_page():
    with ui.header(elevated=True).style("background-color: #3874c8").classes(
        "items-center justify-center"
    ):
        ui.markdown("### 微信运营助手")
        # ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')
    with ui.left_drawer(top_corner=True, bottom_corner=True).style(
        "background-color: #d7e3f4"
    ):
        ui.label("菜单")
    # with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
    #     ui.label('RIGHT DRAWER')
    with ui.footer().style("background-color: #3874c8").classes(
        "items-center justify-center"
    ):
        ui.label("Power by 黑神话广智队")

    main_content()
