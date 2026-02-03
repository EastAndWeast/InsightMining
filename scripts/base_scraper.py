import asyncio
from playwright.async_api import async_playwright
import json

class BaseScraper:
    def __init__(self, headless=True):
        self.headless = headless

    async def get_page_content(self, url):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            try:
                # 减少等待时间，不强制 networkidle，改为 domcontentloaded + 固定延时
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(3) # 给 JS 渲染留点时间
                content = await page.content()
            except Exception as e:
                print(f"[BaseScraper] 访问超时或出错: {str(e)}", flush=True)
                content = ""
            finally:
                await browser.close()
            return content

    def save_json(self, data, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
