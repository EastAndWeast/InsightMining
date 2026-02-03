import asyncio
from scripts.amazon_scraper import AmazonScraper
from scripts.analyzer import ReviewAnalyzer
import json

async def run_integration_test():
    print("--- 开始集成测试 ---")
    
    # 1. 模拟抓取过程
    # 注意：为了测试稳定性，这里可以使用 Mock 数据，但我先演示脚本逻辑
    print("[1/3] 模拟评价抓取...")
    sample_reviews = [
        {"platform": "Amazon", "body": "软件很好用，但是没有离线模式，出差很不方便。", "rating": "3星"},
        {"platform": "Amazon", "body": "客服响应太慢了，而且界面在 4K 屏幕上显示有 Bug。", "rating": "2星"}
    ]
    
    # 2. AI 分析
    print("[2/3] 启动 AI 引擎分析机会...")
    analyzer = ReviewAnalyzer()
    analysis_results = analyzer.classify_reviews(sample_reviews)
    print(f"分析结果摘要: {analysis_results['software_opportunity']['concept']}")
    
    # 3. 物料生成
    print("[3/3] 生成营销物料...")
    marketing = analyzer.generate_marketing_materials(analysis_results)
    
    # 汇总结果
    final_output = {
        "raw_data_count": len(sample_reviews),
        "analysis": analysis_results,
        "marketing": marketing
    }
    
    output_path = "任务和测试过程/integration_test_result.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, ensure_ascii=False, indent=4)
    
    print(f"--- 测试完成，结果已保存至: {output_path} ---")

if __name__ == "__main__":
    asyncio.run(run_integration_test())
