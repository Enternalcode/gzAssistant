
from nicegui import ui
from apps.services.add_external_data.crawler.fork import ForkManage, split_by_fixed_length_optimized
from apps.services.slm.slm_service import SlmService
from apps.services.vector_search.hnswlib_vectordb import HnswlibVectorDB
from apps.services.wechat_automation.wechat_auto_responder import WeChatAutoResponder
from apps.utils.common import check_server_status, run_llama_server_async, stop_llama_server
from apps.views._nicegui.components.cosin_distance_threshold_input import cosin_distance_threshold_input
from apps.views._nicegui.components.document_input import document_input
from apps.services.log_service import clogger
from contextlib import contextmanager
from apps.views._nicegui.components.listening_group_name_input import listening_group_name_input
from apps.views._nicegui.components.listening_keyword import listening_keyword_input
from apps.views._nicegui.components.utils import get_stored_content


ai_service = SlmService(
    base_url="http://127.0.0.1:7864",
    api_key="no key",
    logger=clogger
)

class MainPageState:
    def __init__(self) -> None:
        self.processing_document: bool = False
        self.ai_thinking: bool = False
        self.chat_content: str = "比赛可以使用哪些推理框架"
        self.whether_use_web_data: bool = True
        self.distance_threshold: float = 0.47

main_page_state = MainPageState()

def main_content():
    # 运行日志模块
    run_log_view = ui.log(max_lines=100).classes("w-full")
    clogger.add_log_view(run_log_view)
    clogger.info("欢迎使用AI广智")

    with ui.column():
        with ui.column().classes("pt-2 w-full"):
            ui.separator()
            ui.markdown("##### ① 启动AI:")
            ui.label("为保证最优使用效果, 请使用专门为本软件优化的模型。请将本软件附带的models文件, 拷贝到指定文件夹下：`C:\\GZAssistantAppData`。").classes("text-gray-400")
            with ui.row().classes('w-full'):
                ui.button("启动AI", on_click=lambda e: start_slm_services(e.sender))

            ui.label("进行后续步骤之前, 请确保AI服务已成功启动。(AI服务启动需要2-3秒左右时间)").classes("text-gray-400")
            with ui.row().classes('w-full justify-start items-center'):
                ui.label("AI服务状态:")
                ai_server_status_icon = ui.icon("fiber_manual_record", size="1em")
            ui.button("检查AI服务状态", on_click=lambda e: check_ai_server_status(e.sender, ai_server_status_icon))
        with ui.column().classes("py-2 w-full"):
            ui.markdown("##### ② 添加知识库:")
            document_input().classes("w-full")
            with ui.row().classes('w-full'):
                ui.button("训练 AI", on_click=lambda e: crawler_and_embeding(button=e.sender)).tooltip("第一次需要训练，之后如果文档没有更新不需要再进行训练")
                ui.spinner(size='lg').bind_visibility_from(main_page_state, 'processing_document')
        
        with ui.column().classes("pb-2 w-full"):
            ui.markdown("##### ③ 配置:")
            with ui.row().classes('w-full justify-start items-center'):
                cosin_distance_threshold_input()
                ui.switch('使用文档网址知识库').bind_value(main_page_state, 'whether_use_web_data')
            chat_input = ui.input(label="发送给AI").bind_value(main_page_state, 'chat_content').classes("w-full")
            with ui.row().classes('w-full'):
                ui.button(
                    "预览AI效果",
                    on_click=lambda e: check_slm_service(e.sender, chat_input.value)
                )
                ui.spinner(size='lg').bind_visibility_from(main_page_state, 'ai_thinking')
            with ui.row().classes('w-full'):
                listening_group_name_input().classes("w-1/2")
                listening_keyword_input().classes("w-1/4")
            
            ui.label("运行前请确保已打开需要监听的微信群聊，运行后键盘鼠标将交由AI控制，为避免异常请不要继续操作。").classes("text-red-400 text-bold")
            ui.button("运行程序", on_click=lambda e: start_listening(e.sender))


@contextmanager
def disable(button: ui.button):
    button.disable()
    try:
        yield
    finally:
        button.enable()

async def check_ai_server_status(button: ui.button, ai_server_status_icon: ui.icon):
    status = await check_server_status()
    if status:
        clogger.info("AI服务: 在线")
        ai_server_status_icon.style("color: green")
    else:
        clogger.info("AI服务: 已离线")
        ai_server_status_icon.style("color: red")


async def crawler_and_embeding(button: ui.button):
    """
    爬取页面，分段并向量化
    """
    with disable(button):
        main_page_state.processing_document = True
        try:
            document_url = get_stored_content("document_url")
            clogger.info(f"document_url: {document_url}")
            clogger.info("开始爬取目标网页...")
            url_content = ForkManage(document_url, [], clogger).pure_fork()
            clogger.info("正在处理爬取到的数据...")
            segments = split_by_fixed_length_optimized(url_content, 512)
            vector_db = HnswlibVectorDB(ai_service=ai_service, fixed_dim=1024)
            vector_db.initialize_index(max_elements=1000)
            clogger.info("向量化处理中...")
            await vector_db.add_texts_async(segments)
            vector_db.save("url_index.bin", "url_texts.json")
            clogger.info("数据处理完毕")
            ui.notify("AI已学习文档内容, 训练结果已保存。", type="positive")
        finally:
            main_page_state.processing_document = False

async def start_slm_services(button: ui.button):
    with disable(button):
        await run_llama_server_async(run_in_background=True)
        clogger.info("已启动AI服务")

async def check_slm_service(button: ui.button, user_content: str) -> None:
    with disable(button):
        main_page_state.ai_thinking = True
        try:
            auto_responder  = WeChatAutoResponder(ai_service=ai_service, logger=clogger)
            distance_threshold = get_stored_content('cosin_distance_threshold_input')
            print("distance_threshold:", distance_threshold, type(distance_threshold))
            ai_response = await auto_responder.generate_response(last_message=user_content, is_use_web_data=main_page_state.whether_use_web_data, distance_threshold=distance_threshold)
            clogger.info(f"ai回复:\n{ai_response}")
        finally:
            main_page_state.ai_thinking = False

async def start_listening(button: ui.button):
    with disable(button):
        auto_responder  = WeChatAutoResponder(ai_service=ai_service, logger=clogger)
        listening_group_name = get_stored_content('listening_group_name')
        listening_keyword = get_stored_content('listening_keyword')
        await auto_responder.locate_group_and_check_keyword(listening_group_name, listening_keyword)
        clogger.info(f"开始监听, 群名：{listening_group_name}, 关键词：{listening_keyword}")
        ui.notify("开始监听", type="positive")


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
        ui.markdown("#### 菜单")
    # with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
    #     ui.label('RIGHT DRAWER')
    with ui.footer().style("background-color: #3874c8").classes(
        "items-center justify-center"
    ):
        ui.label("Power by 黑神话广智队")

    main_content()
