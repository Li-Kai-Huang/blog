import json
import os

repos_json_path = r"C:\Users\moray\.gemini\antigravity\brain\427bec0c-4214-44d3-973f-2d0cfd1c201d\scratch\repos.json"
output_yaml_path = r"C:\Users\moray\Documents\blog\_data\projects.yml"

with open(repos_json_path, "r", encoding="utf-8") as f:
    repos = json.load(f)

# Define categorizations
ai_ml = ["PersonaLlama-3", "Intelligent_System_2026", "2024AI-Cross-Comain-Healthy-Class"]
robotics = ["cheesy-arena", "frc_choose_alliance_2025offseason", "ri3d-2023-command", "frc-docs"]
tools = ["calendar_assistant", "openspoolman", "odoo-project"]
academic = ["2025Algorithm", "2024class", "2026_navigazione_class"]
web = ["blog", "blogs", "li-kai-huang.github.io", "tunKuo_web", "test_web"]

# Descriptions mapping for empty ones
desc_map = {
    "2026_navigazione_class": "船舶導航課程相關專案與實作，包含軌跡模擬與控制。",
    "frc_choose_alliance_2025offseason": "FRC 2025 季後賽聯盟選擇（Alliance Selection）輔助與決策系統，基於 ASP.NET 開發。",
    "blogs": "個人網頁與部落格早期靜態版面與排版設計實作。",
    "odoo-project": "基於 Odoo 框架的企業資源規劃 (ERP) 系統客製化模組開發與系統整合專案。",
    "li-kai-huang.github.io": "個人 GitHub Pages 主網頁與作品集入口網站來源碼。",
    "2025Algorithm": "2025 年演算法課程程式碼與作業實作，包含多種經典演算法與資料結構分析。",
    "tunKuo_web": "為合作對象設計的響應式網頁前端專案與商業形象展示版面。",
    "2024class": "2024 年學科課程程式實作，包含 C++ 基礎與進階物件導向練習。",
    "test_web": "網頁前端技術測試、API 串接與實驗性互動功能專案。",
    "2024AI-Cross-Comain-Healthy-Class": "2024 年跨領域 AI 健康應用課程之數據分析與機器學習模型實作 Jupyter Notebook。"
}

def clean_metric(val):
    if not val:
        return "0"
    if "</svg>" in val:
        parts = val.split("</svg>")
        val = parts[-1].strip()
    val = "".join(filter(str.isdigit, val))
    return val if val else "0"

processed_projects = []

# 1. Add GitHub repos
for r in repos:
    name = r["name"]
    # Skip template training repository
    if name == "github-slideshow":
        continue
        
    # Clean name
    clean_name = name.replace("_", " ").replace("-", " ")
    # Capitalize first letters, keep acronyms
    if clean_name.lower().startswith("frc"):
        clean_name = "FRC" + clean_name[3:]
    if clean_name.lower().startswith("ai"):
        clean_name = "AI" + clean_name[2:]
        
    clean_name = clean_name.title()
    
    # Handle acronym replacements
    clean_name = clean_name.replace("Frc", "FRC").replace("Ai", "AI").replace("Odoo", "Odoo").replace("Llama", "Llama")
    
    category = "other"
    if name in ai_ml:
        category = "ai_ml"
    elif name in robotics:
        category = "robotics_frc"
    elif name in tools:
        category = "tools_utilities"
    elif name in academic:
        category = "academic_coursework"
    elif name in web:
        category = "web_dev"
        
    description = r["description"]
    if not description:
        description = desc_map.get(name, "個人開發與學習專案。")
        
    # Language cleaning
    language = r["language"]
    if not language:
        if name in ["2026_navigazione_class"]:
            language = "MATLAB"
        elif name in ["blogs"]:
            language = "HTML"
        else:
            language = "Unknown"
            
    stars = clean_metric(r["stars"])
    forks = clean_metric(r["forks"])
            
    processed_projects.append({
        "title": clean_name,
        "description": description,
        "language": language,
        "stars": stars,
        "forks": forks,
        "github": r["url"],
        "article": "",
        "category": category
    })

# 2. Add blog post articles as projects
blog_articles = [
    {
        "title": "6-Instruction CPU",
        "description": "設計並實作一顆單週期 6 指令 CPU，使用 Verilog 進行電路與行為模擬，包含 ROM, RAM, ALU, Register File 及控制器模組之架構設計與波形測試驗證。",
        "language": "Verilog",
        "stars": "0",
        "forks": "0",
        "github": "",
        "article": "/verilog/2025/06/17/verilog-final-report.html",
        "category": "academic_coursework"
    },
    {
        "title": "AI 輔助分類回收系統",
        "description": "基於 Realtek AMB82_mini 與 Google Gemini Vision API 開發的輔助回收系統，整合影像辨識與語音互動，實現垃圾分類自動辨識與語音指引。",
        "language": "C++",
        "stars": "0",
        "forks": "0",
        "github": "",
        "article": "/AI-Class/project1/",
        "category": "ai_ml"
    },
    {
        "title": "AI 智慧監視錄影系統",
        "description": "智慧型影像監測系統。利用 AMB82_mini 每分鐘捕捉影像並傳送至 Google Gemini Vision 進行智慧分析，僅在偵測到環境實質性變化時才記錄並儲存文字描述與影像。",
        "language": "C++",
        "stars": "0",
        "forks": "0",
        "github": "",
        "article": "/AI-Class/project2/",
        "category": "ai_ml"
    },
    {
        "title": "AI 看圖說故事",
        "description": "結合影像捕捉與生成式 AI 的創作系統。使用者按下按鈕拍照後，系統會將圖像傳送至 Google Gemini Vision，由 AI 即時生成童話故事並透過語音喇叭播放。",
        "language": "C++",
        "stars": "0",
        "forks": "0",
        "github": "",
        "article": "/AI-Class/project3/",
        "category": "ai_ml"
    },
    {
        "title": "AI 輔助英語教學家教",
        "description": "智慧英文學習助手。拍攝單字卡影像後透過 Google Gemini Vision 進行單字辨識，隨後發送至 Gemini LLM 生成英文例句，最終以 TTS 語音進行發音教學。",
        "language": "C++",
        "stars": "0",
        "forks": "0",
        "github": "",
        "article": "/AI-Class/project4/",
        "category": "ai_ml"
    },
    {
        "title": "AI 情緒感知音樂播放器",
        "description": "捕捉用戶面部表情並傳送至 Google Gemini 進行情緒分析（喜怒哀樂），自動從本地 SD 卡中挑選並播送最符合當前情感的音樂，提供溫暖的情緒陪伴。",
        "language": "C++",
        "stars": "0",
        "forks": "0",
        "github": "",
        "article": "/AI-Class/project5/",
        "category": "ai_ml"
    },
    {
        "title": "AI 盲人定位導航系統",
        "description": "專為視障人士設計的定位輔助系統。透過鏡頭掃描二維碼 (QR Code) 讀取地點資訊，並透過文字轉語音 (TTS) 技術即時播放語音位置指引。",
        "language": "C++",
        "stars": "0",
        "forks": "0",
        "github": "",
        "article": "/AI-Class/project6/",
        "category": "tools_utilities"
    },
    {
        "title": "AI 盲人多模態視覺輔助系統",
        "description": "整合觸摸、影像、RTC 時間與語音的多模態盲人輔助設備。拍攝環境影像與語音提問傳送給 Google Gemini 進行綜合解析，最終將環境語意透過 TTS 播報出來。",
        "language": "C++",
        "stars": "0",
        "forks": "0",
        "github": "",
        "article": "/AI-Class/project7/",
        "category": "ai_ml"
    }
]

processed_projects.extend(blog_articles)

# Write to yaml file manually to avoid external yaml library dependencies
os.makedirs(os.path.dirname(output_yaml_path), exist_ok=True)
with open(output_yaml_path, "w", encoding="utf-8") as f:
    for item in processed_projects:
        f.write(f"- title: \"{item['title']}\"\n")
        desc_escaped = item['description'].replace('"', '\\"')
        f.write(f"  description: \"{desc_escaped}\"\n")
        f.write(f"  language: \"{item['language']}\"\n")
        f.write(f"  stars: \"{item['stars']}\"\n")
        f.write(f"  forks: \"{item['forks']}\"\n")
        f.write(f"  github: \"{item['github']}\"\n")
        f.write(f"  article: \"{item['article']}\"\n")
        f.write(f"  category: \"{item['category']}\"\n")
        f.write("\n")

print(f"Successfully processed {len(processed_projects)} projects and generated {output_yaml_path}")
