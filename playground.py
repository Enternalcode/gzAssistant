import re
from llama_cpp import Llama
from apps.services.add_external_data.crawler.web_crawler import WebCrawler
from apps.services.add_external_data.crawler.fork import Fork, ForkManage, split_by_fixed_length_optimized
from apps.services.embedding import EmbeddingModel
from apps.services.log_service import clogger
from typing import List, Dict

from apps.services.slm.slm_service import SlmService
from apps.services.vector_search.hnswlib_vectordb import HnswlibVectorDB
from apps.utils.common import Models, download_file, download_file_sync, run_llama_server
from apps.utils.config import init_set_config, APPLICATION_DATA_PATH


ai_service = SlmService(
    base_url="http://localhost:8866",
    api_key="no key",
    logger=clogger
)

def handler(base_url, response: Fork.Response):
    init_set_config()
    result =  split_by_fixed_length_optimized(response.content, 512)
    vector_db = HnswlibVectorDB(ai_service=ai_service)
    vector_db.initialize_index(max_elements=1000)
    
    # 添加文本
    for seg in result:
        print(seg)
        vector_db.add_text(seg)

    # 搜索相似文本
    query = "比赛能使用哪些推理框架"
    results = vector_db.search(query, k=3)
    print("Search results:")
    for text, score in results:
        print(f"Text: {text}, Similarity: {score}")

    # # 保存向量和文本
    vector_db.save("url_index.bin", "url_texts.json")

    # # 加载向量和文本
    vector_db.load("url_index.bin", "url_texts.json")

ForkManage('https://img-bss.csdnimg.cn/armdasai/Armaipc.html', [], clogger).fork(1, set(), handler)
# test_content = """# 初赛提交作品说明
# 1、提交文件为word格式，[点击下载初赛作品模板](https://img-
# operation.csdnimg.cn/csdn/silkroad/img/1724391598271.docx)。请按照模板进行内容的足量补充。
# 2、作品提交请[点击此处](https://jsj.top/f/PUM7Bs)上传提交，在初赛截止前，如您已提交过初赛作品，想进行二次补充更新，可联系群管理员更新自己的作品。      
# 3、初赛作品应符合大赛官方提供的任一底层构建思路，还可从官方提供的赛题任务中进行主题选择，具体参见下文档。
# 4、原则上初赛仅需提供思路即可，在决赛阶段主办方会提供硬件设备，决赛人选可在决赛阶段完成作品开发。**也鼓励大家在初赛期间实现代码的编译和调试，初赛作品的附加材料中提供相关材料可加分！**
# 虚拟环境使用参考资料： <https://learn.microsoft.com/zh-cn/windows/arm/create-arm-vm>"""
test_content = """# 初赛提交作品说明
1、提交文件为word格式，[点击下载初赛作品模板](https://img-
operation.csdnimg.cn/csdn/silkroad/img/1724391598271.docx)。请按照模板进行内容的足量补充。
"""
# res = ai_service.embeddings_sync("hello")

# res = ai_service.chat_sync([
#     {"role": "system", "content": f"你是AI助手,回复内容要简介。相关信息: {test_content}"},
#     {"role": "user", "content": "初赛作品有什么需要注意的地方"}
# ])
# print(res)
# html_content = "<html><body><h1>Hello, world!</h1></body></html>"

# llm = Llama(
#     model_path=r"C:\Users\966\Projects\GuangZhiAssistant-main\models\reader-lm-0.5b-Q4_0_4_4.gguf",
#     n_gpu_layers=-1,  # Uncomment to use GPU acceleration
#     # seed=1337, # Uncomment to set a specific seed
#     n_ctx=1024,  # Uncomment to increase the context window
#     verbose=True
# )

# print(
#     llm.create_chat_completion(messages=[
#         {"role": "system", "content": str(body_content_without_images)},
#         {"role": "user", "content": "比赛能使用什么推理框架"}
#     ])
# )

# print(
#     llm.create_chat_completion(messages=[
#         # {"role": "system", "content": "你是AI助手"},
#         {"role": "user", "content": html_content}
#     ])
# )

# run_llama_server(run_in_background=True)