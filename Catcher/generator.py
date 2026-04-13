import json
import requests
from pathlib import Path
import os
import sys
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# 1. Configuration (配置)
BASE_DIR = Path(__file__).resolve().parent
JSON_FILE_PATH = BASE_DIR.parent / 'Database' / 'snippets.json'
ENV_PATH = BASE_DIR.parent / '.env'
load_dotenv(dotenv_path=ENV_PATH)
#获取环境变量  避免明文密码
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY") 
if not DEEPSEEK_API_KEY:
    print("FATAL ERROR: 找不到 DEEPSEEK_API_KEY！请检查 .env 文件是否配置正确。", file=sys.stderr)
    sys.exit(1) # 强行以错误状态退出
DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

def generate_rosetta_entry(concept):
    """直接让 LLM 根据一个概念，生成所有语言的代码和用法"""
    
    system_prompt = """
    你是一个精通 Python (Pandas), 原生 R 语言 (Base R), 和 SQL 的资深数据科学家。
    用户会提供一个数据处理的【中文概念】。
    请你直接生成这三种语言对应的最标准写法，提取核心参数解释，并提供搜索标签。
    
    【极其重要的格式要求】：
    R 语言部分，绝对不要使用 dplyr、tidyr 包，绝对不要出现 %>% 管道符！
    必须使用纯粹的原生 R 语言 (Base R) 写法，例如 merge(), aggregate(), reshape() 或者 [] 索引。
    
    必须严格返回以下结构的 JSON 对象（绝对不要加 ```json 等 markdown 标记）：
    {
      "tags": ["同义词1", "英文词2"],
      "python": {
        "code": "具体的单行代码",
        "arguments": {"参数名": "一句话中文解释"}
      },
      "r": {
        "code": "原生的单行R代码，比如 merge(df1, df2, by='id', all.x=TRUE)",
        "arguments": {"参数名": "一句话中文解释"}
      },
      "sql": {
        "code": "具体的单行代码",
        "arguments": {"关键字": "一句话中文解释"}
      }
    }
    """
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"概念: {concept}"}
        ],
        "temperature": 0.1
    }
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    print(f"[*] 正在呼叫大模型为你编写: {concept} ...")
    response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        result_text = response.json()['choices'][0]['message']['content']
        result_text = result_text.strip().lstrip('```json').rstrip('```').strip()
        
        try:
            return json.loads(result_text)
        except json.JSONDecodeError:
            # 格式错误也抛出
            print(f"ERROR: 大模型返回格式错误: {result_text}", file=sys.stderr)
            sys.exit(1) 
    else:
        # API 报错也抛出
        print(f"ERROR: API 请求失败，状态码: {response.status_code}，请检查额度或网络。", file=sys.stderr)
        sys.exit(1)

def main():
    # 读取你写的极简 JSON
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
        database = json.load(f)
    
    # 遍历你的词条
    for entry in database:
        if not isinstance(entry, dict):
            continue
        
        concept = entry.get("concept")
        
        # 核心逻辑：如果这个词条只有 concept，没有 python 字段，说明它是你刚加的“空壳”
        if concept and "python" not in entry:
            print(f"\n[+] 发现新任务: {concept}")
            
            # 让大模型直接生成一切
            generated_data = generate_rosetta_entry(concept)
            
            if generated_data:
                # 把大模型生成的内容，完美合并到当前的 entry 里
                entry.update(generated_data)
                print(f"[v] 成功！已自动补全 Python, R, SQL 的代码和参数。")

    # 把补全后的数据写回 JSON 保存
    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=2)
    print("\n[🚀] 数据库自动扩充完毕！快去看看你的 json 文件吧！")

if __name__ == "__main__":
    main()