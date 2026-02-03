import os
import json
import sys
import requests
try:
    from scripts.credential_manager import credentials
except ImportError:
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from credential_manager import credentials

class ReviewAnalyzer:
    def __init__(self):
        # 切换到探测到的可用模型 gemini-2.5-flash
        self.gemini_url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent"

    def classify_reviews(self, raw_reviews):
        """
        调用 Gemini 1.5 Flash 真实 API 进行分类与分析。
        具备 API 故障时的 Mock 降级能力。
        """
        api_key = credentials.get_key("GEMINI")
        
        if not api_key:
            sys.stderr.write("INFO: No valid Gemini API Key found. Using Mock data fallback.\n")
            return self._mock_analysis(raw_reviews)

        try:
            prompt = self._build_prompt(raw_reviews)
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            
            response = requests.post(f"{self.gemini_url}?key={api_key}", json=payload, timeout=30)
            
            if response.status_code != 200:
                sys.stderr.write(f"ERROR: API Response {response.status_code}: {response.text}\n")
                if response.status_code in [401, 429]:
                    credentials.mark_failed("GEMINI", api_key)
                    return self.classify_reviews(raw_reviews)
                return self._mock_analysis(raw_reviews)
                
            result = response.json()
            
            # 解析 Gemini 返回的文本并提取 JSON
            if 'candidates' not in result or not result['candidates']:
                sys.stderr.write(f"ERROR: No candidates in API Response: {json.dumps(result)}\n")
                return self._mock_analysis(raw_reviews)

            content = result['candidates'][0]['content']['parts'][0]['text'].strip()
            sys.stderr.write(f"DEBUG: Raw AI Content: {content[:100]}...\n") 
            
            # 剥离 markdown 代码块标签 (```json ... ```)
            if content.startswith("```"):
                lines = content.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                content = "\n".join(lines).strip()

            return json.loads(content)

        except Exception as e:
            sys.stderr.write(f"ERROR: LLM Analysis failed ({str(e)}). Falling back to Mock.\n")
            return self._mock_analysis(raw_reviews)

    def _build_prompt(self, reviews):
        return f"""
        你是一个资深的市场分析师和产品经理。请分析以下用户评价数据：
        {json.dumps(reviews, ensure_ascii=False)}

        请输出以下 JSON 格式的分析结果：
        {{
            "categories": {{
                "pain_points": ["评价中反映的核心痛点1", "痛点2"],
                "missing_features": ["用户渴望但目前缺失的功能1", "功能2"],
                "highlights": ["产品的好评点1", "好评点2"]
            }},
            "software_opportunity": {{
                "concept": "基于这些反馈，你可以做一个什么样的软件来切入市场？给一个响亮的中文名字",
                "target_users": "目标用户群体是谁？",
                "value_prop": "核心价值主张（一句话描述）"
            }},
            "marketing": {{
                "ad_copy": "一段吸引人的营销短文案",
                "image_prompt": "一张展示该软件核心场景的 AI 生图提示词 (英文)",
                "video_script": "一段 15 秒的短视频脚本梗概"
            }}
        }}
        注意：仅输出 JSON，不要有任何多余解释。
        """

    def _mock_analysis(self, raw_reviews):
        """降级兜底方案代码"""
        return {
            "categories": {
                "pain_points": ["Mock: 配置复杂", "Mock: 价格偏高"],
                "missing_features": ["Mock: 离线模式", "Mock: 数据导出"],
                "highlights": ["Mock: 响应快"]
            },
            "software_opportunity": {
                "concept": "Mock: 极简效率助手",
                "target_users": "学生及白领",
                "value_prop": "虽然目前的分析是通过 Mock 数据生成的，但它展示了系统的完整流程。"
            },
            "marketing": {
                "ad_copy": "Mock: 让效率提升 200%！",
                "image_prompt": "Mock prompt: modern desk with a clock and a notebook",
                "video_script": "Mock: 镜头从混乱到有序的对比。"
            }
        }

    def generate_marketing_materials(self, opportunity_data):
        # 已经在 classify_reviews 中通过 LLM 直接生成了更贴合上下文的物料
        return opportunity_data.get("marketing", {})
