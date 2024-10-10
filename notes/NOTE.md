# Install hnswlib
pip install C:\Users\966\Projects\2024.6.15-experimental-cp312-win_arm64.whl\numpy-2.0.0-cp312-cp312-win_arm64.whl
remove numpy in install_requires
```
setup(
    name='hnswlib',
    version=__version__,
    description='hnswlib',
    author='Yury Malkov and others',
    url='https://github.com/yurymalkov/hnsw',
    long_description="""hnsw""",
    ext_modules=ext_modules,
    install_requires=[],
    cmdclass={'build_ext': BuildExt},
    zip_safe=False,
)
```
python setup.py install 

# qwen llama.cpp compile instruction
https://qwen.readthedocs.io/zh-cn/latest/run_locally/llama.cpp.html

# wechat
https://www.jb51.net/python/299112c3b.html
https://crm.bytell.cn/blog/yyqf/book/22662

# 企业微信机器人接收消息的回调服务框架
https://github.com/easy-wx/wecom-bot-svr
https://panzhongxian.cn/cn/2023/12/deploy-wecom-bot-svr-in-10-minutes/

20240916 mac最新版本4.1.28暂不支持@机器人发送回调
改用企业应用方式交互
https://open.work.weixin.qq.com/wwopen/manual/detail?t=selfBuildApp

# 企微机器人配置说明
https://developer.work.weixin.qq.com/document/path/91770

# 用轻量搭建自己的企业微信AI机器人
https://linux.do/t/topic/180815

# Package
https://github.com/brentvollebregt/auto-py-to-exe
https://github.com/Nuitka/Nuitka
https://github.com/pyinstaller/pyinstaller

# Massive Text Embedding Benchmark (MTEB) Leaderboard
https://huggingface.co/spaces/mteb/leaderboard

# Crawl4ai
https://github.com/unclecode/crawl4ai

# Get clean requirements
pip install pipreqs
pipreqs ./ --savepath requirements.txt

# Run Llama, Phi, Gemma, Mistral with ONNX Runtime.
This API gives you an easy, flexible and performant way of running LLMs on device.
onnxruntime-genai
https://github.com/microsoft/onnxruntime-genai


# 参赛指南
https://img-bss.csdnimg.cn/armdasai/Armaipc.html
更多点击活动详情了解 
https://marketing.csdn.net/p/34a48478fffb3594b186a32a4c73dbc6?pId=2684





# Prompt
**info** 
任务2：从正常对话速度，实时从中抓取时间信息
基于端侧大模型推理框架，如llama.cpp、MNN、mc-lm等(使用ArmCPU)，结合如RAG、Agent等，实现具备一个提取连续对话内容中准确时间的时间提取助手
**question**
有哪些端侧大模型推理框架可以使用 