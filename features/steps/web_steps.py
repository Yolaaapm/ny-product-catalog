from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text_string)

@when('I select "{text}" from the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    for option in element.find_elements(By.TAG_NAME, 'option'):
        if option.text == text:
            option.click()
            break

@when('I click the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + "-btn"
    context.driver.find_element(By.ID, button_id).click()

@then('I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element((By.ID, "flash_message"), message)
    )
    assert found

@then('I should see "{text}" in the results')
def step_impl(context, text):
    element = context.driver.find_element(By.ID, "search_results")
    assert text in element.text

@then('I should not see "{text}" in the results')
def step_impl(context, text):
    element = context.driver.find_element(By.ID, "search_results")
    assert text not in element.text

@then('I should see "{text}" in the "{element_name}" field')
def step_impl(context, text, element_name):
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    assert text in element.get_attribute("value")
