from uiautomation import WindowControl, MenuControl
import time
from apps.services.log_service import clogger

class WeChatAutoResponder:
    def __init__(self, window_title='Weixin', ):
        self.wechat_window = WindowControl(Name=window_title)
        self.session_list = None
        self.answered_messages = set()

    def switch_to_wechat(self):
        """Switch to the WeChat window."""
        self.wechat_window.SwitchToThisWindow()

    def bind_session_list(self, element_name: str = '会话'):
        """Bind the WeChat session list control."""
        self.session_list = self.wechat_window.ListControl(Name=element_name)

    def read_last_message(self, element_name: str = '消息'):
        """Read the last message."""
        last_message_control = self.wechat_window.ListControl(Name=element_name).GetChildren()[-1]
        return last_message_control.Name

    def generate_response(self, last_message):
        """Generate a response based on the last message."""
        response = """
            在比赛中，可以使用以下推理框架：\n\n
            基于Arm CPU的端侧大模型推理框架：\n\n
            1. **llama.cpp**: 这是一个用于推理大型语言模型的C++库，支持在端侧设备上运行。\n\n
            2. **MNN**: Mobile Neural Network，是百度开发的用于移动设备的神经网络框架，支持多种硬件平台。\n\n
            3. **mlc-llm**: 这是一个用于推理大型语言模型的库，可能需要结合其他框架或工具使用。\n\n
            结合RAG和Agent实现的小程序评判标准：\n\n
            除了上述推理框架，还可以考虑以下组件：\n\n
            - **RAG**: Retriever-Augmented Generator，用于增强生成模型的检索能力，可以结合在模型中以提高生成内容的质量和相关性。\n\n
            - **Agent**: 可以指代用于执行特定任务的智能代理，结合RAG使用时，Agent可以用于执行基于生成内容的后续操作或决策。\n\n
            评判标准：\n\n
            评判标准通常包括：\n\n
            - **性能优化**: 包括推理速度、资源使用效率、延迟时间等。
            \n\n- **功 能完善**: 如模型的准确性和多样性、用户交互体验等。\n\n
            - **创意**: 包括模型的创新性、应用的多样性、用户界面设计等。\n\n
            在实际比赛中，评判标准可能会根据具体要求和目标进行调整，比如在特定场景下，可能更侧 重于性能优化或创意表现。参赛者需要根据比赛规则和目标，选择合适的推理框架和组件，并优化其性能和功能，同时展示其创意解决方案。
        """
        return response

    def send_response(self, response):
        """Send the response message."""
        # Replace newline symbols
        response = response.replace('{br}', '{Shift}{Enter}')
        # Input the response
        self.wechat_window.SendKeys(response, waitTime=0)
        # Send the message
        self.wechat_window.SendKeys('{Enter}', waitTime=0)

    def locate_group_and_check_keyword(self, group_name, keyword):
        """Locate a group by name and check for a keyword in messages continuously."""
        self.switch_to_wechat()
        self.bind_session_list()
        clogger.info("监听中...")
        while True:
            for session in self.session_list.GetChildren()[:5]:
                session_name = session.Name
                if session_name == group_name:
                    last_message_control = self.wechat_window.ListControl(Name='消息').GetChildren()[-1]
                    last_message = last_message_control.Name
                    message_id = id(last_message_control)
                    if keyword in last_message and message_id not in self.answered_messages:
                        clogger.info("有人呼唤广智...")
                        response = self.generate_response(last_message)
                        time.sleep(1)
                        self.send_response(response)
                        self.answered_messages.add(message_id)
                        break
            time.sleep(1)

    def main_loop(self):
        """Main loop to listen and automatically respond to messages."""
        self.switch_to_wechat()
        self.bind_session_list()

        while True:
            # Check for unread messages
            unread_message_control = self.session_list.TextControl(searchDepth=4)

            # Infinite loop to maintain, no timeout error
            while not unread_message_control.Exists(0):
                pass

            # If there are unread messages
            if unread_message_control.Name:
                # Click on the unread message
                unread_message_control.Click(simulateMove=False)

                # Read the last message
                last_message = self.read_last_message()

                # Generate a response
                response = self.generate_response(last_message)

                # Send the response
                self.send_response(response)

                # Right-click on the message sender
                sender_name = last_message[:5]
                self.wechat_window.TextControl(SubName=sender_name).RightClick()