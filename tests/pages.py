from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # =========================
    # LOCATORS
    # =========================

    # Addresses
    FROM_INPUT = (By.ID, "from")
    TO_INPUT = (By.ID, "to")

    CALL_TAXI_BUTTON = (
        By.XPATH,
        "//button[contains(@class, 'button') and text()='Call a taxi']"
    )

    # Supportive tariff
    SUPPORTIVE_TARIFF = (
        By.XPATH,
        "//div[contains(@class, 'tcard-title') and text()='Supportive']"
    )

    SELECTED_SUPPORTIVE_TARIFF = (
        By.XPATH,
        "//div[contains(@class, 'tcard') and contains(@class, 'active')]"
        "[.//div[text()='Supportive']]"
    )

    # Phone
    PHONE_NUMBER_BUTTON = (
        By.XPATH,
        "//div[contains(@class, 'np-text') and contains(text(), 'Phone number')]"
    )

    PHONE_INPUT = (By.ID, "phone")

    PHONE_NEXT_BUTTON = (
        By.XPATH,
        "//button[contains(@class, 'button') and contains(text(), 'Next')]"
    )

    PHONE_CODE_INPUT = (By.ID, "code")

    PHONE_CONFIRM_BUTTON = (
        By.XPATH,
        "//button[contains(text(), 'Confirm')]"
    )

    # Payment
    PAYMENT_METHOD = (
        By.XPATH,
        "//div[contains(@class, 'pp-text') and contains(text(), 'Payment method')]"
    )

    PAYMENT_METHOD_CONTAINER = (
        By.XPATH,
        "//div[contains(@class, 'pp-text') and contains(text(), 'Payment method')]/.."
    )

    ADD_CARD_BUTTON = (
        By.XPATH,
        "//div[contains(@class, 'pp-title') and contains(text(), 'Add card')]"
    )

    CARD_NUMBER_INPUT = (By.ID, "number")

    CARD_CODE_INPUT = (
        By.XPATH,
        "//input[@id='code' and contains(@class, 'card-input')]"
    )

    LINK_BUTTON = (
        By.XPATH,
        "//button[contains(text(), 'Link')]"
    )

    CLOSE_PAYMENT_MODAL = (
        By.XPATH,
        "//div[contains(@class, 'payment-picker')]"
        "//button[contains(@class, 'close-button')]"
    )

    # Driver comment
    COMMENT_INPUT = (By.ID, "comment")

    # Blanket and handkerchiefs
    BLANKET_CLICK = (
        By.XPATH,
        "//div[@class='r-sw-label' and contains(text(), "
        "'Blanket and handkerchiefs')]"
        "/following-sibling::div[@class='r-sw']//span"
    )

    BLANKET_SWITCH = (
        By.XPATH,
        "//div[@class='r-sw-label' and contains(text(), "
        "'Blanket and handkerchiefs')]"
        "/following-sibling::div[@class='r-sw']//input"
    )

    # Ice cream
    ICE_CREAM_PLUS = (
        By.XPATH,
        "//div[text()='Ice cream']"
        "/following-sibling::div[@class='r-counter']"
        "//div[@class='counter-plus']"
    )

    ICE_CREAM_COUNT = (
        By.XPATH,
        "//div[text()='Ice cream']"
        "/following-sibling::div[@class='r-counter']"
        "//div[@class='counter-value']"
    )

    # Order
    ORDER_BUTTON = (By.CLASS_NAME, "smart-button")

    CAR_SEARCH_MODAL = (By.CLASS_NAME, "order-body")

    # =========================
    # ADDRESS METHODS
    # =========================

    def enter_from_address(self, address):
        self.wait.until(
            EC.visibility_of_element_located(self.FROM_INPUT)
        ).send_keys(address)

    def enter_to_address(self, address):
        self.wait.until(
            EC.visibility_of_element_located(self.TO_INPUT)
        ).send_keys(address)

    def click_call_taxi(self):
        sleep(1)

        button = self.wait.until(
            EC.presence_of_element_located(
                self.CALL_TAXI_BUTTON
            )
        )

        self.wait.until(
            lambda driver: (
                button.is_displayed()
                and button.is_enabled()
            )
        )

        # The physical Selenium click can be intercepted by
        # the tariff card. JavaScript triggers the button directly.
        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

        sleep(1)

    # =========================
    # SUPPORTIVE TARIFF
    # =========================

    def select_supportive_plan(self):
        if not self.driver.find_elements(
            *self.SELECTED_SUPPORTIVE_TARIFF
        ):
            self.wait.until(
                EC.element_to_be_clickable(
                    self.SUPPORTIVE_TARIFF
                )
            ).click()

    def is_supportive_selected(self):
        return bool(
            self.driver.find_elements(
                *self.SELECTED_SUPPORTIVE_TARIFF
            )
        )

    # =========================
    # PHONE
    # =========================

    def enter_phone_number(self, phone_number):
        self.wait.until(
            EC.element_to_be_clickable(
                self.PHONE_NUMBER_BUTTON
            )
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                self.PHONE_INPUT
            )
        ).send_keys(phone_number)

        self.wait.until(
            EC.element_to_be_clickable(
                self.PHONE_NEXT_BUTTON
            )
        ).click()

    def enter_phone_code(self, code):
        self.wait.until(
            EC.visibility_of_element_located(
                self.PHONE_CODE_INPUT
            )
        ).send_keys(code)

        self.wait.until(
            EC.element_to_be_clickable(
                self.PHONE_CONFIRM_BUTTON
            )
        ).click()

    # =========================
    # CREDIT CARD
    # =========================

    def add_credit_card(self, card_number, card_code):
        self.wait.until(
            EC.element_to_be_clickable(
                self.PAYMENT_METHOD
            )
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(
                self.ADD_CARD_BUTTON
            )
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(
                self.CARD_NUMBER_INPUT
            )
        ).send_keys(card_number)

        card_code_input = self.wait.until(
            EC.visibility_of_element_located(
                self.CARD_CODE_INPUT
            )
        )

        card_code_input.send_keys(card_code)

        # Move focus away from the CVV field so the Link
        # button can become enabled.
        card_code_input.send_keys(Keys.TAB)

        self.wait.until(
            EC.element_to_be_clickable(
                self.LINK_BUTTON
            )
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(
                self.CLOSE_PAYMENT_MODAL
            )
        ).click()

    # =========================
    # DRIVER COMMENT
    # =========================

    def enter_driver_comment(self, message):
        self.wait.until(
            EC.visibility_of_element_located(
                self.COMMENT_INPUT
            )
        ).send_keys(message)

    # =========================
    # BLANKET / HANDKERCHIEFS
    # =========================

    def order_blanket_and_handkerchiefs(self):
        self.wait.until(
            EC.element_to_be_clickable(
                self.BLANKET_CLICK
            )
        ).click()

    def is_blanket_and_handkerchiefs_selected(self):
        return self.driver.find_element(
            *self.BLANKET_SWITCH
        ).is_selected()

    # =========================
    # ICE CREAM
    # =========================

    def order_ice_creams(self, quantity):
        plus_button = self.wait.until(
            EC.element_to_be_clickable(
                self.ICE_CREAM_PLUS
            )
        )

        for _ in range(quantity):
            plus_button.click()

    def get_ice_cream_quantity(self):
        value = self.wait.until(
            EC.visibility_of_element_located(
                self.ICE_CREAM_COUNT
            )
        ).text

        return int(value)

    # =========================
    # FINAL ORDER
    # =========================

    def click_order(self):
        self.wait.until(
            EC.element_to_be_clickable(
                self.ORDER_BUTTON
            )
        ).click()

    def is_car_search_modal_visible(self):
        return self.wait.until(
            EC.visibility_of_element_located(
                self.CAR_SEARCH_MODAL
            )
        ).is_displayed()