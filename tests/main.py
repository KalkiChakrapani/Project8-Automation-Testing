from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

import data
import helpers as h
from pages import UrbanRoutesPage

class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability(
            "goog:loggingPrefs",
            {"performance": "ALL"}
        )

        cls.driver = webdriver.Chrome(options=options)

        if h.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Urban Routes server is reachable")
        else:
            print("Urban Routes server is not reachable")

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        urban_routes_page = UrbanRoutesPage(self.driver)
        sleep(2)
        urban_routes_page.enter_from_address(data.ADDRESS_FROM)
        urban_routes_page.enter_to_address(data.ADDRESS_TO)
        urban_routes_page.click_call_taxi()
        sleep(2)
        assert urban_routes_page.get_from_address() == data.ADDRESS_FROM
        assert urban_routes_page.get_to_address() == data.ADDRESS_TO

    def test_select_supportive_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        urban_routes_page = UrbanRoutesPage(self.driver)

        urban_routes_page.enter_from_address(data.ADDRESS_FROM)
        urban_routes_page.enter_to_address(data.ADDRESS_TO)
        urban_routes_page.click_call_taxi()

        urban_routes_page.select_supportive_plan()

        assert "active" in urban_routes_page.is_supportive_selected()

    def test_fill_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        urban_routes_page = UrbanRoutesPage(self.driver)

        urban_routes_page.enter_from_address(data.ADDRESS_FROM)
        urban_routes_page.enter_to_address(data.ADDRESS_TO)
        urban_routes_page.click_call_taxi()
        urban_routes_page.select_supportive_plan()

        urban_routes_page.enter_phone_number(data.PHONE_NUMBER)

        code = h.retrieve_phone_code(self.driver)

        urban_routes_page.enter_phone_code(code)

        sleep(2)

        result = urban_routes_page.get_phone_number()
        assert result == data.PHONE_NUMBER

    def test_add_credit_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        urban_routes_page = UrbanRoutesPage(self.driver)

        urban_routes_page.enter_from_address(data.ADDRESS_FROM)
        urban_routes_page.enter_to_address(data.ADDRESS_TO)
        urban_routes_page.click_call_taxi()
        urban_routes_page.select_supportive_plan()

        urban_routes_page.add_credit_card(
            data.CARD_NUMBER,
            data.CARD_CODE
        )
        sleep(5)
        assert "Card" in urban_routes_page.get_payment_method_text()

    def test_comment_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        urban_routes_page = UrbanRoutesPage(self.driver)

        urban_routes_page.enter_from_address(data.ADDRESS_FROM)
        urban_routes_page.enter_to_address(data.ADDRESS_TO)
        urban_routes_page.click_call_taxi()
        urban_routes_page.select_supportive_plan()

        urban_routes_page.enter_driver_comment(
            data.MESSAGE_FOR_DRIVER
        )

        assert urban_routes_page.get_driver_comment() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        urban_routes_page = UrbanRoutesPage(self.driver)

        urban_routes_page.enter_from_address(data.ADDRESS_FROM)
        urban_routes_page.enter_to_address(data.ADDRESS_TO)
        urban_routes_page.click_call_taxi()
        urban_routes_page.select_supportive_plan()

        urban_routes_page.order_blanket_and_handkerchiefs()

        assert urban_routes_page.is_blanket_and_handkerchiefs_selected()

    def test_order_2_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        urban_routes_page = UrbanRoutesPage(self.driver)

        urban_routes_page.enter_from_address(data.ADDRESS_FROM)
        urban_routes_page.enter_to_address(data.ADDRESS_TO)
        urban_routes_page.click_call_taxi()
        urban_routes_page.select_supportive_plan()

        urban_routes_page.order_ice_creams(2)

        assert urban_routes_page.get_ice_cream_quantity() == 2

    def test_order_taxi(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        urban_routes_page = UrbanRoutesPage(self.driver)

        urban_routes_page.enter_from_address(data.ADDRESS_FROM)
        urban_routes_page.enter_to_address(data.ADDRESS_TO)
        urban_routes_page.click_call_taxi()
        urban_routes_page.select_supportive_plan()

        urban_routes_page.enter_phone_number(data.PHONE_NUMBER)

        code = h.retrieve_phone_code(self.driver)

        urban_routes_page.enter_phone_code(code)

        urban_routes_page.enter_driver_comment(
            data.MESSAGE_FOR_DRIVER
        )

        urban_routes_page.click_order()

        assert urban_routes_page.is_car_search_modal_visible()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()