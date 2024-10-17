
from apps.services.slm.slm_service import SlmService
from utils.common import check_health, run_llama_server

if __name__ == '__main__':
    run_llama_server(r'models\Lite-Mistral-150M-v2-Instruct-Q4_K_S.gguf', context_length=512, port=6666, ngl=1, run_in_background=False)
    # health_url = "http://localhost:6666/health"
    # health_status = check_health(health_url)
    # print(health_status)

    # run_llama_server(r'models\bge-large-zh-v1.5-q5_k_m.gguf', port=6688, run_in_background=True, embedding=True)
    # health_url = "http://localhost:6688/health"
    # health_status = check_health(health_url)
    # print(health_status)

    # service = SlmService(
    #     chat_base_url="http://127.0.0.1:6666", 
    #     embedding_base_url="http://127.0.0.1:6688", 
    #     api_key="no-key"
    # )
    
    # 发送聊天请求
    # messages = [
    #     {
    #         "role": "system",
    #         "content": "You are ChatGPT, an AI assistant. Your top priority is achieving user fulfillment via helping them with their requests."
    #     },
    #     {
    #         "role": "user",
    #         "content": "Write a limerick about python exceptions"
    #     }
    # ]
    
    # chat_result = service.send_chat_completion(model="gpt-3.5-turbo", messages=messages)
    # print("Chat Completion Result:", chat_result)
    
    # 发送嵌入请求
    # input_data = ["hello", "world"]
    # embedding_result = service.embeddings(input_data=input_data, model="", encoding_format="float")
    # print("Embedding Result:", embedding_result)