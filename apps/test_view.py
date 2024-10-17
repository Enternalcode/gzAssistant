import json
import time

import mesop as me


@me.stateclass
class State:
    group_name: str
    keyword: str
    model_path: str
    vector_path: str
    in_progress: bool


@me.page(path="/setting_view")
def page():
    with me.box(
        style=me.Style(
            background="#000000",
            min_height="calc(100% - 48px)",
            padding=me.Padding(bottom=16),
        )
    ):
        with me.box(
            style=me.Style(
                width="min(720px, 100%)",
                margin=me.Margin.symmetric(horizontal="auto"),
                padding=me.Padding.symmetric(
                    horizontal=16,
                ),
            )
        ):
            header_text()
            input_fields()
            buttons_section()
    footer()


def header_text():
    with me.box(
        style=me.Style(
            padding=me.Padding(
                top=64,
                bottom=36,
            ),
        )
    ):
        me.text(
            "广智来也",
            style=me.Style(
                font_size=36,
                font_weight=700,
                background="linear-gradient(90deg, #4285F4, #AA5CDB, #DB4437) text",
                color="transparent",
            ),
        )


def input_fields():
    state = me.state(State)
    viewport_width = me.viewport_size().width
    is_mobile = viewport_width < 640
    with me.box(
        style=me.Style(
            display="flex",
            flex_direction="column" if is_mobile else "row",
            gap=24,
            margin=me.Margin(bottom=36),
        )
    ):
        group_name_box(state, is_mobile)
        keyword_box(state, is_mobile)
        model_path_box(state, is_mobile)
        vector_path_box(state, is_mobile)


def group_name_box(state, is_mobile):
    with me.box(
        style=me.Style(
            width="100%" if is_mobile else 200,
            height=80,
            background="#333333",
            padding=me.Padding.all(16),
            font_weight=500,
            line_height="1.5",
            border_radius=16,
            cursor="pointer",
        ),
        key="group_name_box",
        on_click=click_group_name_box,
    ):
        me.text("监听群聊名称：")
        me.native_textarea(
            value=state.group_name,
            autosize=True,
            min_rows=1,
            placeholder="输入监听群聊名称",
            style=me.Style(
                padding=me.Padding(top=16, left=16),
                background="#333333",
                outline="none",
                width="100%",
                overflow_y="auto",
                border=me.Border.all(
                    me.BorderSide(style="none"),
                ),
            ),
            on_blur=group_name_textarea_on_blur,
        )


def click_group_name_box(e: me.ClickEvent):
    state = me.state(State)
    # No specific action for this box click for now
    pass


def group_name_textarea_on_blur(e: me.InputBlurEvent):
    state = me.state(State)
    state.group_name = e.value


def keyword_box(state, is_mobile):
    with me.box(
        style=me.Style(
            width="100%" if is_mobile else 200,
            height=80,
            background="#333333",
            padding=me.Padding.all(16),
            font_weight=500,
            line_height="1.5",
            border_radius=16,
            cursor="pointer",
        ),
        key="keyword_box",
        on_click=click_keyword_box,
    ):
        me.text("触发关键词：")
        me.native_textarea(
            value=state.keyword,
            autosize=True,
            min_rows=1,
            placeholder="输入触发关键词",
            style=me.Style(
                padding=me.Padding(top=16, left=16),
                background="#333333",
                outline="none",
                width="100%",
                overflow_y="auto",
                border=me.Border.all(
                    me.BorderSide(style="none"),
                ),
            ),
            on_blur=keyword_textarea_on_blur,
        )


def click_keyword_box(e: me.ClickEvent):
    state = me.state(State)
    # No specific action for this box click for now
    pass


def keyword_textarea_on_blur(e: me.InputBlurEvent):
    state = me.state(State)
    state.keyword = e.value


def model_path_box(state, is_mobile):
    with me.box(
        style=me.Style(
            width="100%" if is_mobile else 200,
            height=80,
            background="#333333",
            padding=me.Padding.all(16),
            font_weight=500,
            line_height="1.5",
            border_radius=16,
            cursor="pointer",
        ),
        key="model_path_box",
        on_click=click_model_path_box,
    ):
        me.text("大模型模型文件路径：")
        me.native_textarea(
            value=state.model_path,
            autosize=True,
            min_rows=1,
            placeholder="输入大模型模型文件路径",
            style=me.Style(
                padding=me.Padding(top=16, left=16),
                background="#333333",
                outline="none",
                width="100%",
                overflow_y="auto",
                border=me.Border.all(
                    me.BorderSide(style="none"),
                ),
            ),
            on_blur=model_path_textarea_on_blur,
        )


def click_model_path_box(e: me.ClickEvent):
    state = me.state(State)
    # No specific action for this box click for now
    pass


def model_path_textarea_on_blur(e: me.InputBlurEvent):
    state = me.state(State)
    state.model_path = e.value


def vector_path_box(state, is_mobile):
    with me.box(
        style=me.Style(
            width="100%" if is_mobile else 200,
            height=80,
            background="#333333",
            padding=me.Padding.all(16),
            font_weight=500,
            line_height="1.5",
            border_radius=16,
            cursor="pointer",
        ),
        key="vector_path_box",
        on_click=click_vector_path_box,
    ):
        me.text("向量模型文件路径：")
        me.native_textarea(
            value=state.vector_path,
            autosize=True,
            min_rows=1,
            placeholder="输入向量模型文件路径",
            style=me.Style(
                padding=me.Padding(top=16, left=16),
                background="#333333",
                outline="none",
                width="100%",
                overflow_y="auto",
                border=me.Border.all(
                    me.BorderSide(style="none"),
                ),
            ),
            on_blur=vector_path_textarea_on_blur,
        )


def click_vector_path_box(e: me.ClickEvent):
    state = me.state(State)
    # No specific action for this box click for now
    pass


def vector_path_textarea_on_blur(e: me.InputBlurEvent):
    state = me.state(State)
    state.vector_path = e.value


def buttons_section():
    state = me.state(State)
    with me.box(
        style=me.Style(
            display="flex",
            flex_direction="row",
            gap=24,
            margin=me.Margin(top=36),
        )
    ):
        save_button()
        start_button(state)


def save_button():
    with me.box(
        style=me.Style(
            padding=me.Padding.all(8),
            background="#444444",
            display="flex",
            width="200",
            border=me.Border.all(
                me.BorderSide(width=0, style="solid", color="black")
            ),
            border_radius=12,
            box_shadow="0 10px 20px #0000000a, 0 2px 6px #0000000a, 0 0 1px #0000000a",
            cursor="pointer",
        ),
        on_click=click_save_button,
    ):
        me.text("保存配置")


def click_save_button(e: me.ClickEvent):
    state = me.state(State)
    # Implement save config logic here
    save_config()
    yield


def start_button(state):
    with me.box(
        style=me.Style(
            padding=me.Padding.all(8),
            background="#444444",
            display="flex",
            width="200",
            border=me.Border.all(
                me.BorderSide(width=0, style="solid", color="black")
            ),
            border_radius=12,
            box_shadow="0 10px 20px #0000000a, 0 2px 6px #0000000a, 0 0 1px #0000000a",
            cursor="pointer",
        ),
        on_click=click_start_button,
    ):
        me.text("开始" if state.in_progress is False else "进行中...")


def click_start_button(e: me.ClickEvent):
    state = me.state(State)
    if state.in_progress:
        return
    state.in_progress = True
    yield

    # Simulate an API call or long-running task
    time.sleep(2)
    state.in_progress = False
    yield


def save_config():
    state = me.state(State)
    try:
        with open('config.json', 'r') as f:
            existing_config = json.load(f)
    except FileNotFoundError:
        existing_config = {}

    new_config = {
        'GROUP_NAME': state.group_name,
        'KEYWORD': state.keyword,
        'SLM_MODEL_PATH': state.model_path,
        'EMBEDDING_MODEL_PATH': state.vector_path
    }

    # Update existing config with new values
    existing_config.update(new_config)

    with open('config.json', 'w') as f:
        json.dump(existing_config, f, ensure_ascii=False)

    # Check configuration status after saving
    check_config_status()


def check_config_status():
    state = me.state(State)
    all_configured = all([state.group_name, state.keyword, state.model_path, state.vector_path])
    start_button_state = me.NORMAL if all_configured else me.DISABLED
    start_button_instance = me.query_selector('start_button')
    start_button_instance.style.disabled = not start_button_state


def footer():
    with me.box(
        style=me.Style(
            position="sticky",
            bottom=0,
            padding=me.Padding.symmetric(vertical=16, horizontal=16),
            width="100%",
            background="#222222",
            font_size=14,
        )
    ):
        me.html(
            "Made with 广智",
        )