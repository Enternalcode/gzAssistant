import asyncio
from apps.services.add_external_data.crawler.web_crawler import WebCrawler
from services.wechat_automation.wechat_auto_responder import WeChatAutoResponder
from services.vector_search.hnswlib_vectordb import HnswlibVectorDB
from utils.config import default_config

def test_crawler():
    crawler = WebCrawler()
    url = "https://img-bss.csdnimg.cn/armdasai/Armaipc.html"
    contents = crawler.crawl(url)
    all_content = "".join(contents)
    split_contents = crawler.split_content(all_content, 100)
    print(split_contents)

# def test_hnswlib_vectordb():
#     embedding_model = EmbeddingModel.get_model()
#     db = HnswlibVectorDB(embedding_model)
#     db.initialize_index(max_elements=1000)

#     # 添加文本
#     texts = [
#         "你好",
#         "今天天气很好",
#         "我喜欢学习编程",
#         "这是一条测试信息",
#         "生活充满了挑战"
#     ]
#     db.add_texts(texts)

#     # 搜索相似文本
#     query = "今天是个好日子"
#     results = db.search(query, k=3)
#     print("Search results:")
#     for text, score in results:
#         print(f"Text: {text}, Similarity: {score}")

#     # 保存向量和文本
#     db.save("vector_index.bin", "texts.json")

#     # 加载向量和文本
#     db.load("vector_index.bin", "texts.json")

# def test_second_time_vectordb():
#     # 加载模型和数据库
#     embedding_model = EmbeddingModel.get_model()
#     db = HnswlibVectorDB(embedding_model)

#     # 加载已经保存的向量和文本
#     db.load("vector_index.bin", "texts.json")

#     # 进行搜索
#     query = "今天是个好日子"
#     results = db.search(query, k=3)
#     print("Search results:")
#     for text, score in results:
#         print(f"Text: {text}, Similarity: {score}")


def test_wechat_auto():
    auto_responder  = WeChatAutoResponder()
    auto_responder.locate_group_and_check_keyword('arm64创新应用小赛', '@黑神话广智')

# def test_setting_view():
#     main_view = SettingView()
#     main_view.run()



if __name__ == '__main__':
    # SYNC
    # test_embedding()
    # test_llama_cpp_python()
    # test_wecom_robot()
    # test_hnswlib_vectordb()
    # test_second_time_vectordb()
    test_wechat_auto()
    # test_setting_view()

    # ASYNC
    

