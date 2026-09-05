"""Web UI step definitions using Selenium."""
import time
from behave import when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

BASE_URL = "http://127.0.0.1:5000"


def get_driver(context):
    if not hasattr(context, "driver"):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        context.driver = webdriver.Chrome(options=options)
    return context.driver


def element_id(name):
    return name.lower().replace(" ", "_")


@when('I visit the "Home Page"')
def step_impl(context):
    get_driver(context).get(BASE_URL)


@when('I set the "{name}" to "{value}"')
def step_impl(context, name, value):
    el = get_driver(context).find_element(By.ID, element_id(name))
    el.clear()
    el.send_keys(value)


@when('I change "{name}" to "{value}"')
def step_impl(context, name, value):
    el = get_driver(context).find_element(By.ID, element_id(name))
    el.clear()
    el.send_keys(value)


@when('I select "{value}" in the "{name}" dropdown')
def step_impl(context, value, name):
    Select(get_driver(context).find_element(By.ID, element_id(name))).select_by_visible_text(value)


@when('I press the "{button}" button')
def step_impl(context, button):
    get_driver(context).find_element(By.ID, f"{button.lower()}-btn").click()
    time.sleep(1)


@when('I copy the "{name}" field')
def step_impl(context, name):
    context.clipboard = get_driver(context).find_element(By.ID, element_id(name)).get_attribute("value")


@when('I paste the "{name}" field')
def step_impl(context, name):
    el = get_driver(context).find_element(By.ID, element_id(name))
    el.clear()
    el.send_keys(context.clipboard)


@then('I should see the message "{message}"')
def step_impl(context, message):
    body = get_driver(context).find_element(By.TAG_NAME, "body").text
    assert message in body, f"Message '{message}' not found"


@then('I should see "{value}" in the "{name}" field')
def step_impl(context, value, name):
    found = get_driver(context).find_element(By.ID, element_id(name)).get_attribute("value")
    assert value in found, f"'{value}' not in field {name}"


@then('I should see "{value}" in the results')
def step_impl(context, value):
    body = get_driver(context).find_element(By.TAG_NAME, "body").text
    assert value in body, f"'{value}' not in results"


@then('I should not see "{value}" in the results')
def step_impl(context, value):
    body = get_driver(context).find_element(By.TAG_NAME, "body").text
    assert value not in body, f"'{value}' unexpectedly in results"
