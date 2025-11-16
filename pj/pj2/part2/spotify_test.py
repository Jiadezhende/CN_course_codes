from playwright.sync_api import sync_playwright, TimeoutError
from pathlib import Path

# ---------- 配置 ----------
DOMAIN = "spotify.com"
LOAD_TIMEOUT_MS = 10000
BACKGROUND_TIMEOUT_MS = 3000
HAR_FOLDER = Path("har_test")
HAR_FOLDER.mkdir(parents=True, exist_ok=True)
HEADLESS = True

HAR_PATH = HAR_FOLDER / f"{DOMAIN}.har"

# ---------- 爬虫 ----------
with sync_playwright() as p:
    browser = p.chromium.launch(headless=HEADLESS)
    context = None
    try:
        context = browser.new_context(
            record_har_path=str(HAR_PATH),
            record_har_content="omit",  # 避免 embed 卡死
            record_har_mode="full"
        )
        page = context.new_page()
        page.set_default_navigation_timeout(LOAD_TIMEOUT_MS)

        url = f"https://{DOMAIN}"
        print(f"Visiting {url}")

        # 导航到页面
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=LOAD_TIMEOUT_MS)
        except TimeoutError:
            print("Navigation timeout, but continuing...")

        page.wait_for_timeout(1000)  # 等待 1 秒以确保初始请求完成

        # # 等待短时间的后台请求
        # try:
        #     page.wait_for_load_state("networkidle", timeout=BACKGROUND_TIMEOUT_MS)
        # except TimeoutError:
        #     pass

        # 强制停止页面的持续请求（例如 SPA 的长轮询）
        try:
            page.close()  # 强制关闭页面
            print(f"Stopped page load for {url}.")
        except Exception:
            pass

        # 关闭 context，写入 HAR
        try:
            context.close()
        except Exception as e:
            print(f"Warning: context.close() failed: {e}")
        print(f"HAR saved to {HAR_PATH}")

    finally:
        try:
            if context:
                context.close()
        except:
            pass
        try:
            browser.close()
        except Exception:
            pass
