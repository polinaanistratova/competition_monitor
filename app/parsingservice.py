import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from config import COMPETITORS


class CompetitorParser:
    def __init__(self):
        self.history_file = "parsing_history.json"
    
    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        try:
            driver = webdriver.Chrome(options=chrome_options)
            return driver
        except Exception as e:
            print(f"Ошибка запуска драйвера: {e}")
            return None
    
    def parse_url(self, url):
        driver = self.setup_driver()
        if not driver:
            return {"error": "driver_failed", "url": url}
        
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            title = soup.find('title').text if soup.find('title') else ""
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc['content'] if meta_desc else ""
            
            h1_list = [h.text.strip() for h in soup.find_all('h1')[:3]]
            h2_list = [h.text.strip() for h in soup.find_all('h2')[:5]]
            
            texts = [p.text.strip() for p in soup.find_all('p')[:10]]
            combined_text = " ".join([title, description] + h1_list + h2_list + texts)
            
            result = {
                "url": url,
                "title": title,
                "description": description,
                "h1": h1_list,
                "h2": h2_list,
                "preview_text": combined_text[:1000],
                "parsed_at": datetime.now().isoformat(),
                "status": "success"
            }
            return result
        except Exception as e:
            return {"url": url, "error": str(e), "status": "failed", "parsed_at": datetime.now().isoformat()}
        finally:
            driver.quit()
    
    def parse_all(self):
        results = []
        for url in COMPETITORS:
            results.append(self.parse_url(url))
        self.save_history(results)
        return results
    
    def save_history(self, results):
        history = []
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            except:
                history = []
        history.append({"batch": results, "timestamp": datetime.now().isoformat()})
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    
    def get_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
