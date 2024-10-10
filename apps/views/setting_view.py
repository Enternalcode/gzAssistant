import customtkinter
import json

from services.wechat_automation.wechat_auto_responder import WeChatAutoResponder

config_path = 'apps\config.json'

class SettingView:
    def __init__(self):
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("blue")

        self.app = customtkinter.CTk()
        self.app.geometry("800x600")

        # Create labels for titles
        font = ("黑体", 24, "bold")
        page_title = customtkinter.CTkLabel(self.app, text="广智来也", fg_color="transparent", font=font)
        group_name_label = customtkinter.CTkLabel(self.app, text="监听群聊名称：")
        keyword_label = customtkinter.CTkLabel(self.app, text="触发关键词：")
        model_path_label = customtkinter.CTkLabel(self.app, text="大模型模型文件路径：")
        vector_path_label = customtkinter.CTkLabel(self.app, text="向量模型文件路径：")

        self.group_name_var = customtkinter.StringVar()
        self.keyword_var = customtkinter.StringVar()
        self.model_path_var = customtkinter.StringVar()
        self.vector_path_var = customtkinter.StringVar()

        self.group_name_entry = customtkinter.CTkEntry(self.app, textvariable=self.group_name_var, width=200)
        self.keyword_entry = customtkinter.CTkEntry(self.app, textvariable=self.keyword_var, width=200)
        self.model_path_entry = customtkinter.CTkEntry(self.app, textvariable=self.model_path_var, width=400)
        self.vector_path_entry = customtkinter.CTkEntry(self.app, textvariable=self.vector_path_var, width=400)
        self.save_button = customtkinter.CTkButton(self.app, text="保存配置", command=self.save_config)
        self.start_button = customtkinter.CTkButton(self.app, text="开始", command=self.start_function, state=customtkinter.DISABLED)


        page_title.pack(padx=20, pady=30)

        group_name_label.pack()
        self.group_name_entry.pack(padx=20, pady=10)

        keyword_label.pack()
        self.keyword_entry.pack(padx=20, pady=10)

        model_path_label.pack()
        self.model_path_entry.pack(padx=20, pady=10)

        vector_path_label.pack()
        self.vector_path_entry.pack(padx=20, pady=10)

        self.save_button.pack(padx=20, pady=20)
        self.start_button.pack(padx=20, pady=10)

        self.load_config()

        # Check initial configuration status
        self.check_config_status()

    def load_config(self):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                self.group_name_var.set(config.get('GROUP_NAME', ''))
                self.keyword_var.set(config.get('KEYWORD', ''))
                self.model_path_var.set(config.get('SLM_MODEL_PATH', ''))
                self.vector_path_var.set(config.get('EMBEDDING_MODEL_PATH', ''))
        except FileNotFoundError:
            pass

    def save_config(self):
        try:
            with open(config_path, 'r') as f:
                existing_config = json.load(f)
        except FileNotFoundError:
            existing_config = {}

        new_config = {
            'GROUP_NAME': self.group_name_var.get(),
            'KEYWORD': self.keyword_var.get(),
            'SLM_MODEL_PATH': self.model_path_var.get(),
            'EMBEDDING_MODEL_PATH': self.vector_path_var.get()
        }

        # Update existing config with new values
        existing_config.update(new_config)

        with open(config_path, 'w') as f:
            json.dump(existing_config, f)

        self.check_config_status()

    def start_function(self):
        print("开始执行相关任务")
        auto_responder  = WeChatAutoResponder()
        auto_responder.locate_group_and_check_keyword('arm64创新应用小赛', '@黑神话广智')

    def check_config_status(self):
        all_configured = all([self.group_name_var.get(), self.keyword_var.get(), self.model_path_var.get(), self.vector_path_var.get()])
        self.start_button.configure(state=customtkinter.NORMAL if all_configured else customtkinter.DISABLED)

    def run(self):
        self.app.mainloop()