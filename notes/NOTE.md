# FunClip
https://github.com/modelscope/FunClip?tab=readme-ov-file#Install

# llvm llama env
C:\Users\966\Projects\llama.cpp-master-llvm\build-arm64-windows-llvm-release\bin

# llama_cpp/server/settings.py
https://llama-cpp-python.readthedocs.io/en/latest/server/#configuration-and-multi-model-support

# gpustack/bge-reranker-v2-m3-GGUF
https://huggingface.co/gpustack/bge-reranker-v2-m3-GGUF/blob/main/bge-reranker-v2-m3-Q4_0.gguf

# converted to GGUF format from openbmb/MiniCPM3-4B using llama.cpp
https://huggingface.co/ibrahimkettaneh/MiniCPM3-4B-IQ4_NL-GGUF

# Here is an example how you can place a custom label inside a linear progress bar:
https://github.com/zauberzeug/nicegui/discussions/1613

# WOA packages
https://linaro.atlassian.net/wiki/spaces/WOAR/pages/28658270210/Packages

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
llama-cpp-python -C cmake.args="-DGGML_BLAS=ON;-DGGML_BLAS_VENDOR=OpenBLAS"

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

# Install llama-cpp-python
pip install llama-cpp-python -C cmake.args="-DGGML_BLAS=ON;-DGGML_BLAS_VENDOR=OpenBLAS"

# Llama.cpp inference config
AVX = 0 | AVX_VNNI = 0 | AVX2 = 0 | AVX512 = 0 | AVX512_VBMI = 0 | AVX512_VNNI = 0 | AVX512_BF16 = 0 | FMA = 0 | NEON = 1 | SVE = 0 | ARM_FMA = 1 | F16C = 0 | FP16_VA = 0 | RISCV_VECT = 0 | WASM_SIMD = 0 | BLAS = 0 | SSE3 = 0 | SSSE3 = 0 | VSX = 0 | MATMUL_INT8 = 1 | LLAMAFILE = 0 |

# 需求
场景 + 诱因 + 目的 + 结果