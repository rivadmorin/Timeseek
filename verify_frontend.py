import asyncio
from playwright.async_api import async_playwright
import os
import signal
import subprocess
import time

async def verify():
    # Start the server in the background
    # Use a dummy embedding and OCR to avoid heavy dependencies in test
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    process = subprocess.Popen(["python3", "-m", "timeseek.app", "--port", "8083"], env=env)

    time.sleep(10) # Wait for server to start

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await p.new_page()

        try:
            # Check Dashboard
            await page.goto("http://localhost:8083/dashboard")
            await page.screenshot(path="dashboard_verify.png")
            print("Dashboard screenshot taken.")

            # Check Timeline
            await page.goto("http://localhost:8083/timeline")
            await page.screenshot(path="timeline_verify.png")
            print("Timeline screenshot taken.")

            # Check Search
            await page.goto("http://localhost:8083/search")
            await page.screenshot(path="search_verify.png")
            print("Search screenshot taken.")

        except Exception as e:
            print(f"Error during verification: {e}")
        finally:
            await browser.close()
            process.terminate()

if __name__ == "__main__":
    asyncio.run(verify())
