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

processed_repos = []
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
            
    processed_repos.append({
        "name": name,
        "title": clean_name,
        "description": description,
        "language": language,
        "stars": stars,
        "forks": forks,
        "url": r["url"],
        "category": category
    })

# Write to yaml file manually to avoid external yaml library dependencies
os.makedirs(os.path.dirname(output_yaml_path), exist_ok=True)
with open(output_yaml_path, "w", encoding="utf-8") as f:
    for item in processed_repos:
        f.write(f"- name: \"{item['name']}\"\n")
        f.write(f"  title: \"{item['title']}\"\n")
        # escape double quotes in description
        desc_escaped = item['description'].replace('"', '\\"')
        f.write(f"  description: \"{desc_escaped}\"\n")
        f.write(f"  language: \"{item['language']}\"\n")
        f.write(f"  stars: \"{item['stars']}\"\n")
        f.write(f"  forks: \"{item['forks']}\"\n")
        f.write(f"  url: \"{item['url']}\"\n")
        f.write(f"  category: \"{item['category']}\"\n")
        f.write("\n")

print(f"Successfully processed {len(processed_repos)} repos and generated {output_yaml_path}")
