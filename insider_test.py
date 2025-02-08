import pytest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


HOME_PAGE = "https://useinsider.com/"
QA_PAGE = "https://useinsider.com/careers/quality-assurance/"
TIMEOUT = 10
SELENIUM_HUB_URL = "http://selenium-hub:4444/wd/hub"


@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--headless")
    prefs = {"profile.default_content_setting_values.notifications": 1}
    chrome_options.add_experimental_option("prefs", prefs)

    __driver = webdriver.Chrome(options=chrome_options)
    # __driver = webdriver.Remote(command_executor=SELENIUM_HUB_URL, options=chrome_options)

    yield __driver
    __driver.quit()


def _accept_cookies(driver: webdriver.Chrome):
    actions = ActionChains(driver)
    try:
        cookies = WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "wt-cli-accept-all-btn"))
        )
        actions.move_to_element(cookies).perform()
        cookies.click()
    except NoSuchElementException as e:
        print("No cookies popup found", e)


def _go_to_careers_page(driver: webdriver.Chrome):
    actions = ActionChains(driver)

    company_element = WebDriverWait(driver, TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//li[@class='nav-item dropdown']/a[@class='nav-link dropdown-toggle' and contains(text(), 'Company')]"))
    )

    actions.move_to_element(company_element).perform()
    company_element.click()

    # Click on the "Careers" link
    careers_link = WebDriverWait(driver, TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='https://useinsider.com/careers/' and contains(text(), 'Careers')]"))
    )

    actions.move_to_element(careers_link).perform()
    careers_link.click()

    WebDriverWait(driver, TIMEOUT).until(
        EC.url_to_be("https://useinsider.com/careers/")
    )


def apply_location_filter(driver: webdriver.Chrome):
    actions = ActionChains(driver)

    location_dropdown = WebDriverWait(driver, TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "select2-filter-by-location-container"))
    )

    actions.move_to_element(location_dropdown).perform()
    location_dropdown.click()

    locations = WebDriverWait(driver, TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "select2-container--open"))
    )

    actions.move_to_element(locations).perform()

    WebDriverWait(driver, TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//ul[contains(@class, 'select2-results__options')]"))
    )

    locations = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'select2-results__option')]"))
    )

    for option in locations:
        if option.text.strip() == "Istanbul, Turkiye":
            option.click()
            break  # Stop after selecting


def apply_department_filter(driver: webdriver.Chrome):
    actions = ActionChains(driver)

    department_dropdown = WebDriverWait(driver, TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "select2-filter-by-department-container"))
    )

    actions.move_to_element(department_dropdown).perform()
    department_dropdown.click()

    departments = WebDriverWait(driver, TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//ul[contains(@class, 'select2-results__options')]"))
    )

    WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'select2-results__option')]"))
    )

    departments = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'select2-results__option')]"))
    )

    for option in departments:
        if option.text.strip() == "Quality Assurance":
            option.click()
            break  # Stop after selecting


def get_jobs_from_jobs_list(driver: webdriver.Chrome):
    actions = ActionChains(driver)

    # Wait for the job list to load
    job_list = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "jobs-list"))
    )

    actions.move_to_element(job_list).perform()

    jobs = []

    for _ in range(5):
        try:
            job_elements = WebDriverWait(driver, TIMEOUT).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "position-list-item"))
            )

            for job in job_elements:

                view_role_button = job.find_element(By.TAG_NAME, "a")
                jobs.append({
                    "location": job.get_attribute("data-location"),
                    "team": job.get_attribute("data-team"),
                    "title": job.find_element(By.CLASS_NAME, "position-title").text,
                    "view_role_button": view_role_button
                })
            return jobs
        except StaleElementReferenceException as err:
            print("err ->", err)
            sleep(1)


def test_homepage(driver: webdriver.Chrome):
    driver.get(HOME_PAGE)
    _accept_cookies(driver)
    assert "Insider" in driver.title, "Homepage did not load correctly"


def test_blocks_in_careers_page(driver: webdriver.Chrome):
    driver.get(HOME_PAGE)
    _accept_cookies(driver)

    _go_to_careers_page(driver=driver)

    assert "Careers" in driver.title

    # Locations
    locations_block = WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.XPATH, "//h3[contains(text(), 'Our Locations')]"))
    )
    assert locations_block.is_displayed(), "Locations block is not displayed"

    # Teams
    teams_block = WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.XPATH, "//h3[contains(text(), 'Find your calling')]"))
    )
    assert teams_block.is_displayed(), "Teams block is not displayed"

    # Life at Insider
    life_at_insider_block = WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Life at Insider')]"))
    )
    assert life_at_insider_block.is_displayed(), "Life at Insider block is not displayed"


def test_QA_page(driver: webdriver.Chrome):
    driver.get(QA_PAGE)
    actions = ActionChains(driver)
    _accept_cookies(driver=driver)

    # Go to See all QA jobs
    qa_jobs_button = WebDriverWait(driver, TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='https://useinsider.com/careers/open-positions/?department=qualityassurance' and contains(text(), 'See all QA jobs')]"))
    )

    actions.move_to_element(qa_jobs_button).perform()
    qa_jobs_button.click()

    # Wait to load data
    sleep(10)

    # Filter by Location menu -> Getting Country to select

    apply_location_filter(driver)
    apply_department_filter(driver)

    # Wait filters to be applied
    sleep(5)

    jobs = get_jobs_from_jobs_list(driver)

    original_window = driver.current_window_handle

    for job in jobs:
        assert job.get("location") == "istanbul-turkiye"
        assert job.get("team") == "qualityassurance"

        actions.click(job.get("view_role_button")).perform()

        # Wait for a new tab to appear
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])

        # Wait for redirect and check if it's a Lever page
        WebDriverWait(driver, TIMEOUT).until(
            EC.url_contains("jobs.lever.co")
        )
        assert "jobs.lever.co" in driver.current_url
        print("driver.current_url ->", driver.current_url)
        driver.switch_to.window(original_window)


if __name__ == "__main__":
    pytest.main()
