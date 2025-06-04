from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    InvalidSelectorException,
    ElementNotInteractableException,
    NoSuchWindowException,
    InvalidSessionIdException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import setup_logger

logger = setup_logger("selenium_helper")


# -------------------------------
# Safe driver.get()
# -------------------------------
def safe_get(driver, url):
    try:
        driver.get(url)
        logger.info(f"Navigated to {url}")
        return True
    except (WebDriverException, NoSuchWindowException, InvalidSessionIdException) as e:
        logger.error(f"Failed to navigate to {url}: {e}")
        return False


# -------------------------------
# Safe wait + find_element
# -------------------------------
def safe_find(driver, by, value, timeout=10):
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((by, value)))
        logger.debug(f"Element found: {value}")
        return element
    except TimeoutException:
        logger.warning(f"Timeout: Element not found – {value}")
    except InvalidSelectorException as e:
        logger.error(f"Invalid selector: {value} – {e}")
    except StaleElementReferenceException as e:
        logger.warning(f"Stale element: {value} – {e}")
    except Exception as e:
        logger.error(f"Error finding element {value}: {e}")
    return None


# -------------------------------
# Safe click with wait
# -------------------------------
def safe_click(driver, by=None, value=None, element=None, timeout=10):
    try:
        if element is None:
            wait = WebDriverWait(driver, timeout)
            element = wait.until(EC.element_to_be_clickable((by, value)))
        element.click()
        logger.info("Click successful")
        return True
    except (ElementClickInterceptedException, ElementNotInteractableException) as e:
        logger.warning(f"Click issue: {e}")
    except TimeoutException:
        logger.warning("Click timeout")
    except Exception as e:
        logger.error(f"Click failed: {e}")
    return False


# -------------------------------
# Safe send_keys with wait
# -------------------------------
def safe_send_keys(driver, keys, by=None, value=None, element=None, timeout=10):
    try:
        if element is None:
            wait = WebDriverWait(driver, timeout)
            element = wait.until(EC.presence_of_element_located((by, value)))
        element.clear()
        element.send_keys(keys)
        logger.info(f"Sent keys: {keys}")
        return True
    except (ElementNotInteractableException, StaleElementReferenceException) as e:
        logger.warning(f"⚠️ Send keys issue: {e}")
    except TimeoutException:
        logger.warning("⏳ Send keys timeout")
    except Exception as e:
        logger.error(f"Failed to send keys: {e}")
    return False
