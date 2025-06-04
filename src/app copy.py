import pathlib, sys
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

import csv
import time
from pathlib import Path

from selenium.webdriver.common.by import By
from core.BaseClass import BaseClass
from utils.logger import setup_logger
from utils.selenium_helper import safe_get, safe_click, safe_find

from selenium.webdriver.common.by import By

logger = setup_logger(__file__)




# Config paths
INPUT_FILE = "src/data/parcel_ids.txt"
OUTPUT_FILE = "src/data/parcels_tax_data.csv"

from utils.selenium_helper import safe_find
from selenium.webdriver.common.by import By

def extract_property_info(driver):

    fields = [
        "Property ID",
        "Tax Year",
        "Township",
        "Site Address",
        "Property Use",
        "Land Use",
        "Tax Status",
        "Clean & Green"
    ]

    info = {field: "" for field in fields}

    for label in fields:
        xpath = f"//div[normalize-space(text())='{label}']/following-sibling::div"
        value_el = safe_find(driver, By.XPATH, xpath, timeout=5)
        if value_el:
            info[label] = value_el.text.strip()

    return info




def extract_delinquent_taxes(driver):
    if not safe_click(driver, By.LINK_TEXT, "Delinquent Taxes"):
        return []

    rows_xpath = "//table[contains(@class, 'table')]/tbody/tr"
    rows = driver.find_elements(By.XPATH, rows_xpath)

    data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) == 4:
            tax_year = cells[0].text.strip()
            due = cells[1].text.strip()
            paid = cells[2].text.strip()
            total_due = cells[3].text.strip()

            if total_due != "$0.00":
                data.append({
                    "Tax Year": tax_year,
                    "Due": due,
                    "Paid": paid,
                    "Total Due": total_due
                })

    return data



def main():
    parcel_ids = Path(INPUT_FILE).read_text().splitlines()
    logger.info(f"📥 Loaded {len(parcel_ids)} parcel IDs")

    results = []

    with BaseClass(use_proxy=True, headless=False) as bot:
        for idx, parcel_id in enumerate(parcel_ids, 1):
            url = f"https://lancasterpa.devnetwedge.com/parcel/view/{parcel_id}/2023"
            logger.info(f"🔎 [{idx}/{len(parcel_ids)}] Checking parcel {parcel_id}")

            if not safe_get(bot.driver, url):
                continue

            time.sleep(3)  # Let page load

            prop_info = extract_property_info(bot.driver)
            if prop_info:
                prop_info["Parcel ID"] = parcel_id
                results.append(prop_info)

    if results:
        keys = [
            "Parcel ID", "Property ID", "Tax Year", "Township", "Site Address",
            "Property Use", "Land Use", "Tax Status", "Clean & Green"
        ]
        with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)
        logger.info(f"✅ Saved {len(results)} records to {OUTPUT_FILE}")
    else:
        logger.info("🚫 No property info found for any parcel.")

if __name__ == "__main__":
    main()
