import asyncio
import os
import sys

# 确保能导入 scripts 下的模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.analyzer import ReviewAnalyzer
import json

async def test_real_analysis():
    print("--- 真实 API 集成测试 (Gemini 1.5 Flash) ---")
    
    # 手动设置一个测试 Key (用户运行前需要设置)
    # os.environ["GEMINI_API_KEY"] = "YOUR_KEY_HERE"
    
    analyzer = ReviewAnalyzer()
    
    sample_reviews = [
        {"platform": "AppStore", "body": "Web3 wallet is too hard to use. I lost my seed phrase and cannot recover funds. No support at all.", "rating": "1 star"},
        {"platform": "AppStore", "body": "Love the NFT display, but gas fees are confusing. Is it Ethereum or Polygon?", "rating": "3 stars"}
    ]
    
    print("正在调用 AI 进行分析 (如果未设置 Key 将进入 Mock 降级)...")
    result = analyzer.classify_reviews(sample_reviews)
    
    print("\n--- 分析结果预览 ---")
    print(json.dumps(result, indent=4, ensure_ascii=False))
    
    # 检查是否是降级数据
    if "Mock:" in result['software_opportunity']['concept']:
        print("\n[状态] 当前正处于 MOCK 降级状态 (未检测到有效 API Key)。")
    else:
        print("\n[状态] 成功获取真实 AI 分析结果！")

if __name__ == "__main__":
    asyncio.run(test_real_analysis())
