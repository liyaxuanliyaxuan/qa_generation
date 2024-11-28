import os
import json
import logging
from pathlib import Path
from pydantic import BaseModel
from openai import OpenAI
import tiktoken
from prompt import one_shot_prompt

# OpenAI API密钥
api_key = ''

# 初始化OpenAI客户端
client = OpenAI(api_key=api_key)

# 初始化token计数器和费用计算器
total_input_tokens = 0
total_output_tokens = 0
total_cost = 0

# GPT-4的价格（每1000个token）
PRICE_PER_1K_TOKENS = 0.03  # 请根据实际价格调整

# 设置日志
logging.basicConfig(filename='qa_generation_4o.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class QAPair(BaseModel):
    question: str
    real_answer: str

class QACollections(BaseModel):
    data: list[QAPair]

def count_tokens(text):
    encoding = tiktoken.encoding_for_model("gpt-4")
    return len(encoding.encode(text))

def read_md_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def generate_qa_pairs(content, output_file, file_name):
    global total_input_tokens, total_output_tokens, total_cost
    try:
        # 计算输入token
        input_tokens = count_tokens(f"{one_shot_prompt}\n\n{content}")
        
        response = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一个专业的物理学家，请根据以下要求帮助生成问题和答案"},
                {"role": "user", "content": f"{one_shot_prompt}\n\n{content}"}
            ],
            temperature=0.7,
            response_format=QACollections
        )
        
        # 解析响应
        qa_pairs = json.loads(response.choices[0].message.content)
        
        # 计算输出token
        output_tokens = response.usage.completion_tokens
        
        # 计算token使用量和成本
        tokens_used = response.usage.total_tokens
        cost = (tokens_used / 1000) * PRICE_PER_1K_TOKENS
        
        total_input_tokens += input_tokens
        total_output_tokens += output_tokens
        total_cost += cost
        
        # 记录日志
        logging.info(f"文件: {file_name}")
        logging.info(f"输入tokens: {input_tokens}")
        logging.info(f"输出tokens: {output_tokens}")
        logging.info(f"本次请求总tokens: {tokens_used}")
        logging.info(f"本次请求成本: ${cost:.4f}")
        logging.info(f"累计成本: ${total_cost:.4f}")
        logging.info("-" * 50)


        # 将Pydantic模型转换为可序列化的字典
        print(response.choices[0].message.parsed.data)
        qa_pairs = [qa_pair.dict() for qa_pair in response.choices[0].message.parsed.data]
    
        qas_directory = Path('qas')
        qas_directory.mkdir(exist_ok=True)
        
        # 更新输出文件路径到新的文件夹
        output_file = qas_directory / output_file.name
        
        # 保存QA对到指定的JSON文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(qa_pairs, f, ensure_ascii=False, indent=2)
        
        return qa_pairs
        
    except Exception as e:
        logging.error(f"生成QA对时出错: {str(e)}")
        return []

def process_directory(directory):
    md_files = list(Path(directory).rglob('*.md'))
    total_files = len(md_files)
    
    for index, file_path in enumerate(md_files, 1):
        print(f"正在处理文件 {index}/{total_files}: {file_path}")
        
        content = read_md_file(file_path)
        output_file = file_path.with_name(f"{file_path.stem}_qa_pairs.json")
        qa_pairs = generate_qa_pairs(content, output_file, file_path.name)
        
        print(f"为 {file_path.name} 生成了 {len(qa_pairs)} 个QA对")
        print(f"进度: {index}/{total_files}")
        print("-" * 50)

if __name__ == "__main__":
    input_dir = "md/"
    process_directory(Path(input_dir))
    print("所有.md文件处理完成")
    print(f"总输入tokens: {total_input_tokens}")
    print(f"总输出tokens: {total_output_tokens}")
    print(f"总成本: ${total_cost:.4f}")
    
    # 记录最终总结到日志
    logging.info("处理完成总结")
    logging.info(f"总输入tokens: {total_input_tokens}")
    logging.info(f"总输出tokens: {total_output_tokens}")
    logging.info(f"总成本: ${total_cost:.4f}")
