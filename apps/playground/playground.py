import openai

client = openai.OpenAI(
    base_url="http://localhost:6666/v1", # "http://<Your api-server IP>:port"
    api_key = "sk-no-key-required"
)

completion = client.chat.completions.create(
# stream=True,
model="Lite-Mistral-150M-v2-Instruct-Q4_K_S.gguf",
messages=[
    {"role": "system", "content": "You are a customer service person that everyone likes."},
    {"role": "user", "content": "How are you?"}
]
)

print(completion.choices[0].message.content)