import pathlib, sys
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from utils.logger import setup_logger
from utils.driver_factory import create_driver

logger = setup_logger(__file__)

from selenium.webdriver.support.ui import WebDriverWait


class BaseClass:
    def __init__(self, use_proxy=False, headless=False):
        logger.info("🔧 Initializing base browser")
        self.driver = create_driver(use_proxy=use_proxy, headless=headless)
        logger.info("🚗 Driver created")

        self.driver.implicitly_wait(15)
        self.driver.set_page_load_timeout(60)


        self.wait = WebDriverWait(self.driver, 15)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()

    def shutdown(self):
        if self.driver:
            self.driver.quit()
            logger.info("🛑 Browser session closed")
