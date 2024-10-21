import asyncio
import sqlite3
import time
from uiautomation import WindowControl
from apps.services.slm.slm_service import SlmService
from apps.services.vector_search.hnswlib_vectordb import HnswlibVectorDB
from apps.utils.config import APPLICATION_DATA_PATH

class WeChatAutoResponder:
    def __init__(self, ai_service: SlmService, logger, window_title='Weixin', fixed_dim: int = 1024):
        self.wechat_window = WindowControl(Name=window_title)
        self.session_list = None
        self.answered_messages = set()
        self.ai_service = ai_service
        self.vector_db = HnswlibVectorDB(ai_service=ai_service, fixed_dim=fixed_dim)
        self.logger = logger
        self.is_generating_response = False

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

    def get_answer_by_question(self, question: str, db_file: str = f"{APPLICATION_DATA_PATH}/data/gz.db") -> str:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT answer FROM questions_answers WHERE question = ?', (question,))
            result = cursor.fetchone()

            if result is not None:
                return result[0]
            else:
                return ""
        finally:
            conn.close()

    async def generate_response(self, 
                                last_message: str, 
                                is_use_web_data: bool = True, 
                                is_use_qa_data: bool = False,
                                distance_threshold: float | str = 0.47) -> str:
        if isinstance(distance_threshold, str):
            distance_threshold = float(distance_threshold)
        web_knowledge = ""

        system_prompt = """你是AI助手，用中文回答,回答要简洁，字数控制在50字"""
        if is_use_web_data:
            self.vector_db.load("url_index.bin", "url_texts.json")
            web_knowledge, web_distance = await self.vector_db.search_async(last_message, k=5, distance_threshold=distance_threshold)
            self.logger.info(f"匹配到文档知识库内容:\n{web_knowledge}\n分数:{web_distance}")
            system_prompt += f"""\n使用知识库信息回答用户:{web_knowledge}"""
        
        if is_use_qa_data:
            self.vector_db.load("qa_index.bin", "qa_texts.json")
            qa_question, qa_distance = await self.vector_db.search_async(last_message, k=10, distance_threshold=distance_threshold)
            # 找到最相似的问题，并查找预设的答案
            qa_answer = self.get_answer_by_question(question=qa_question)
            self.logger.info(f"匹配问答知识库:\n问题:\n{qa_question}\n回答:\n{qa_answer}\n分数:{qa_distance}")
            system_prompt  += """\n使用预设答案回答用户: {qa_answer}"""
        
        print(f"system_prompt: \n{system_prompt}")

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": last_message}
        ]
        response = await self.ai_service.chat_async(messages)
        return response

    def send_response(self, response):
        """Send the response message."""
        # Replace newline symbols
        response = response.replace('{br}', '{Shift}{Enter}')
        # Input the response
        self.wechat_window.SendKeys(response, waitTime=0)
        # Send the message
        self.wechat_window.SendKeys('{Enter}', waitTime=0)

    async def locate_group_and_check_keyword(self, group_name: str, keyword: str, detection_frequency: int = 5):
        self.switch_to_wechat()
        self.bind_session_list()
        self.logger.info("监听中...")
        self.logger.info(f"检测频率：{detection_frequency}s/次")
        lock = asyncio.Lock()
        while True:
            if not self.is_generating_response:
                async with lock:
                    for session in self.session_list.GetChildren()[:5]:
                        session_name = session.Name
                        if session_name == group_name:
                            last_message_control = self.wechat_window.ListControl(Name = '消息').GetChildren()[-1]
                            last_message = last_message_control.Name
                            message_id = id(last_message_control)
                            if keyword in last_message and message_id not in self.answered_messages:
                                self.logger.info(f"用户问题: {last_message}")
                                try:
                                    start_time = time.time()  # 记录开始时间
                                    self.is_generating_response = True
                                    clean_last_message = last_message.replace(keyword, "")  # 去掉keyword
                                    self.send_response(f"AI已收到问题:\n{clean_last_message}\n思考中...")
                                    await asyncio.sleep(1)
                                    response = await self.generate_response(clean_last_message)
                                    end_time = time.time()  # 记录结束时间
                                    duration = end_time - start_time  # 计算耗时
                                    self.logger.info(f"AI生成回答耗时：{duration:.2f}秒")
                                    self.send_response(response)
                                    self.answered_messages.add(message_id)
                                    self.is_generating_response = False
                                except Exception as e:
                                    self.logger.error(f"生成响应时出错: {e}")
                                    self.is_generating_response = False
            else:
                # 限流，AI正在生成问题
                self.logger.info("限流，AI正在回答中跳过此次检测， 检测频率：{detection_frequency}s/次")

            await asyncio.sleep(detection_frequency)
                