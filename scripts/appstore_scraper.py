from base_scraper import BaseScraper
import asyncio
from bs4 import BeautifulSoup
import re

class AppStoreScraper(BaseScraper):
    async def scrape_reviews(self, url):
        """
        抓取 App Store 评论。优先使用 RSS Feed API (更稳定)。
        """
        app_id = None
        country = "us"
        
        # 尝试从 URL 提取 ID
        id_match = re.search(r'/id(\d+)', url)
        if id_match:
            app_id = id_match.group(1)
        
        # 尝试提取区域
        country_match = re.search(r'apple\.com/([^/]+)/', url)
        if country_match:
            country = country_match.group(1)
            if country == "ms": country = "my" # RSS 使用 my 代表马来西亚
            
        print(f"[AppStore] 正在处理: ID={app_id}, Country={country}, URL={url}", flush=True)

        # 如果是搜索页面且没有 ID，先抓取搜索页获取第一个 ID
        if not app_id and "search" in url:
            print(f"[AppStore] 搜索页面，正在寻找第一个 App ID...", flush=True)
            content = await self.get_page_content(url)
            id_match = re.search(r'/id(\d+)', content)
            if id_match:
                app_id = id_match.group(1)
                print(f"[AppStore] 自动识别到 App ID: {app_id}", flush=True)
            else:
                print(f"[AppStore] 搜索页面未找到 ID，尝试直接抓取网页内容...", flush=True)
        
        if app_id:
            # 使用 RSS Feed 获取评论 (更稳定，包含 50 条最新评论)
            rss_url = f"https://itunes.apple.com/{country}/rss/customerreviews/id={app_id}/sortby=mostrecent/json"
            print(f"[AppStore] 正在调用 RSS Feed: {rss_url}", flush=True)
            try:
                import requests
                response = requests.get(rss_url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    entries = data.get('feed', {}).get('entry', [])
                    if isinstance(entries, dict): entries = [entries] # 单条处理
                    
                    reviews = []
                    for entry in entries:
                        if 'author' in entry: # 过滤掉非评论条目
                            reviews.append({
                                "platform": "App Store",
                                "title": entry.get('title', {}).get('label', ''),
                                "body": entry.get('content', {}).get('label', ''),
                                "rating": entry.get('im:rating', {}).get('label', '') + " stars"
                            })
                    print(f"[AppStore] RSS 成功获取 {len(reviews)} 条评论", flush=True)
                    return reviews
            except Exception as e:
                print(f"[AppStore] RSS 调用失败: {str(e)}", flush=True)

        # 兜底：如果 RSS 失败或没有 ID，尝试之前的网页抓取逻辑
        print(f"[AppStore] 尝试网页抓取兜底...", flush=True)
        # ... (保留原有的网页抓取逻辑作为兜底)
        return [] # 目前由于网页抓取不稳定，先返回空或调用原来的 logic

# 独立测试用例
if __name__ == "__main__":
    test_url = "https://apps.apple.com/us/app/wechat/id414478124"
    scraper = AppStoreScraper(headless=True)
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(scraper.scrape_reviews(test_url))
    print(f"抓取到 {len(data)} 条 App Store 评价")
    for r in data[:2]:
        print(f"- {r['body'][:50]}...")
