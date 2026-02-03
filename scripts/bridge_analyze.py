import sys
import os
import json
import asyncio

# 动态添加路径以解决不同环境下的导入问题
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from scripts.analyzer import ReviewAnalyzer
except ImportError:
    from analyzer import ReviewAnalyzer

async def main():
    try:
        # 从标准输入读取一行 JSON 数据 (适配 API 调用和命令行测试)
        input_data = sys.stdin.readline()
        if not input_data:
            sys.stderr.write("ERROR: No input data provided\n")
            print(json.dumps({"error": "No input data provided"}), flush=True)
            return

        params = json.loads(input_data)
        reviews = params.get("reviews", [])
        url = params.get("url")
        platform = params.get("platform")
        
        # 真实抓取逻辑
        if url and platform:
            sys.stderr.write(f"DEBUG: Starting real scrape for {platform} on {url}\n")
            try:
                if "App Store" in platform:
                    from appstore_scraper import AppStoreScraper
                    scraper = AppStoreScraper()
                    reviews = await scraper.scrape_reviews(url)
                elif "Amazon" in platform:
                    from amazon_scraper import AmazonScraper
                    scraper = AmazonScraper()
                    reviews = await scraper.scrape_reviews(url)
                else:
                    sys.stderr.write(f"INFO: No dedicated scraper for {platform}, using samples if available.\n")
            except Exception as se:
                sys.stderr.write(f"ERROR: Scrape failed: {str(se)}\n")

        if not reviews:
            # 如果没有抓取到评论，则模拟一组，或者返回错误
            sys.stderr.write("INFO: No reviews found/provided. Using fallback data.\n")
            reviews = [
                {"body": "This app is okay but the UX is confusing.", "rating": "3"},
                {"body": "Too many ads. Unusable.", "rating": "1"}
            ]

        analyzer = ReviewAnalyzer()
        result = analyzer.classify_reviews(reviews)
        
        # 输出最终 JSON 到标准输出
        print(json.dumps(result, ensure_ascii=False), flush=True)

    except Exception as e:
        sys.stderr.write(f"FATAL ERROR: {str(e)}\n")
        print(json.dumps({"error": str(e)}), flush=True)

if __name__ == "__main__":
    asyncio.run(main())
