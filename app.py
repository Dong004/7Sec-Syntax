import streamlit as st
import json
import subprocess
import os
from pathlib import Path
from thefuzz import fuzz

# 1. 页面配置
st.set_page_config(page_title="Goooolden fish:oooooo", page_icon="🐟", layout="wide")

# 2. 路径配置
BASE_DIR = Path(__file__).resolve().parent
JSON_PATH = BASE_DIR / "Database" / "snippets.json"
GENERATOR_PATH = BASE_DIR / "Catcher" / "generator.py"

# 3. 数据加载 (增加清除缓存的功能)
@st.cache_data
def load_database():
    if not JSON_PATH.exists():
        return []
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# 4. 模糊搜索引擎 (保持我们上次升级的版本)
def search_engine(query, database, threshold=65):
    if not query: return database 
    current_threshold = 85 if len(query.strip()) <= 2 else threshold
    results = []
    for item in database:
        if "python" not in item: continue
        concept_score = fuzz.partial_ratio(query.lower(), item.get("concept", "").lower())
        tags_score = max([fuzz.partial_ratio(query.lower(), t.lower()) for t in item.get("tags", [])]) if item.get("tags") else 0
        code_scores = []
        for lang in ["python", "r", "sql"]:
            if lang in item and isinstance(item[lang], dict):
                code_scores.append(fuzz.partial_ratio(query.lower(), item[lang].get("code", "").lower()))
        final_score = max(concept_score, tags_score, max(code_scores) if code_scores else 0)
        if final_score >= current_threshold:
            results.append((final_score, item))
    results.sort(key=lambda x: x[0], reverse=True)
    return [item for score, item in results]

# 5. UI 侧边栏：添加新功能
with st.sidebar:
    st.header("✨ 管理知识库")
    st.markdown("发现不会写的语法？在这里输入概念，AI 自动为你补全。")
    
    new_concept = st.text_input("输入新概念 (例如: '计算移动平均'):")
    
    if st.button("🚀 添加并自动生成用法"):
        if new_concept:
            # Step A: 读取并写入新概念
            db = load_database()
            # 检查是否已存在
            if any(item.get("concept") == new_concept for item in db):
                st.error("该概念已存在！")
            else:
                with st.spinner("正在写入数据库..."):
                    db.append({"concept": new_concept})
                    with open(JSON_PATH, "w", encoding="utf-8") as f:
                        json.dump(db, f, ensure_ascii=False, indent=2)
                
                # Step B: 调用后端 generator.py
                with st.spinner("正在呼叫 AI 生成多语言代码..."):
                    try:
                        # 构建自定义环境变量，强制后台 Python 使用 UTF-8 打印输出
                        custom_env = os.environ.copy()
                        custom_env["PYTHONIOENCODING"] = "utf-8"
                        
                        # 运行脚本，并显式指定环境与编码
                        result = subprocess.run(
                            ["python", str(GENERATOR_PATH)], 
                            capture_output=True, 
                            text=True, 
                            env=custom_env,
                            encoding="utf-8"
                        )
                        
                        if result.returncode == 0:
                            st.success(f"成功添加: {new_concept}")
                            # Step C: 强制刷新缓存
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error(f"生成失败: {result.stderr}")
                    except Exception as e:
                        st.error(f"运行脚本出错: {e}")
        else:
            st.warning("请输入概念名称")


# 6. 主界面渲染
def main():
    st.title("记不住函数名吗小金鱼")
    database = load_database()
    
    search_query = st.text_input("🔍 搜索概念、标签或具体指令 (中英文都可以):")
    matched_results = search_engine(search_query, database)
    
    if not matched_results:
        st.info("没找到？在左侧侧边栏添加它！")
    
    for item in matched_results:
        with st.container():
            st.subheader(item["concept"])
            st.caption(f"🏷️ Tags: {', '.join(item.get('tags', []))}")
            
            col1, col2, col3 = st.columns(3)
            for lang_key, lang_name, col in [("python", "Python", col1), ("r", "R (Base)", col2), ("sql", "SQL", col3)]:
                with col:
                    st.markdown(f"**{lang_name}**")
                    lang_data = item.get(lang_key, {})
                    st.code(lang_data.get("code", "N/A"), language="python" if lang_key != "sql" else "sql")
                    if lang_data.get("arguments"):
                        with st.expander("参数说明"):
                            for arg, desc in lang_data["arguments"].items():
                                st.markdown(f"- **`{arg}`**: {desc}")
            
            # 【核心修复 1】：用不可变的 Python 代码字符串作为绝对主键
            # 如果没有代码（空壳），就用概念名兜底
            primary_key = item.get("python", {}).get("code", item.get("concept"))
            
            op_col1, op_col2 = st.columns([0.9, 0.1])
            
            with op_col1:
                with st.expander("✏️ 编辑词条 (Edit Concept & Tags)"):
                    # 所有的 UI 状态 key 都绑定在这个绝对主键上，彻底消灭幽灵状态
                    new_concept = st.text_input("修改概念名称", value=item.get("concept", ""), key=f"concept_{primary_key}")
                    current_tags_str = ", ".join(item.get("tags", []))
                    new_tags_str = st.text_input("修改标签 (用英文逗号分隔)", value=current_tags_str, key=f"tags_{primary_key}")
                    
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button("💾 保存修改", key=f"save_{primary_key}"):
                            for db_item in database:
                                # 【核心修复 2】：使用 Python Code 作为匹配基准去存库
                                if db_item.get("python", {}).get("code") == item.get("python", {}).get("code"):
                                    db_item["concept"] = new_concept
                                    db_item["tags"] = [t.strip() for t in new_tags_str.split(",") if t.strip()]
                                    break
                            
                            with open(JSON_PATH, "w", encoding="utf-8") as f:
                                json.dump(database, f, ensure_ascii=False, indent=2)
                            st.success("修改已同步！")
                            st.cache_data.clear()
                            st.rerun()
                    
                    with btn_col2:
                        # 【新功能】：取消修改并重置状态
                        if st.button("❌ 放弃修改", key=f"cancel_{primary_key}"):
                            # 强行从会话缓存中把刚刚敲错的字删掉
                            if f"concept_{primary_key}" in st.session_state:
                                del st.session_state[f"concept_{primary_key}"]
                            if f"tags_{primary_key}" in st.session_state:
                                del st.session_state[f"tags_{primary_key}"]
                            st.rerun() # 重新刷新页面，恢复原状

            with op_col2:
                with st.popover("🗑️"):
                    st.error(f"确定删除吗？")
                    st.write(f"概念: {item['concept']}")
                    if st.button("✅ 确定删除", key=f"real_del_{primary_key}"):
                        # 【核心修复 3】：删除时同样认准 Python Code
                        updated_db = [i for i in database if i.get("python", {}).get("code") != item.get("python", {}).get("code")]
                        with open(JSON_PATH, "w", encoding="utf-8") as f:
                            json.dump(updated_db, f, ensure_ascii=False, indent=2)
                        
                        st.cache_data.clear()
                        st.rerun()

            st.divider()

if __name__ == "__main__":
    main()
