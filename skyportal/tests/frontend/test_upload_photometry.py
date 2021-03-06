import pytest
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver import ActionChains


@pytest.mark.flaky(reruns=2)
def test_upload_photometry(
    driver, sedm, super_admin_user, public_source, super_admin_token, public_group
):
    inst_id = sedm.id
    driver.get(f"/become_user/{super_admin_user.id}")
    driver.get(f"/upload_photometry/{public_source.id}")
    csv_text_input = driver.wait_for_xpath('//textarea[@name="csvData"]')
    csv_text_input.send_keys(
        "mjd,flux,fluxerr,zp,magsys,filter\n"
        "58001,55,1,25,ab,sdssg\n"
        "58002,53,1,25,ab,sdssg"
    )

    inst_select = driver.wait_for_xpath('//*[@id="mui-component-select-instrumentID"]')
    driver.scroll_to_element(inst_select)
    ActionChains(driver).move_to_element(inst_select).click().pause(2).perform()

    sedm_element = driver.wait_for_xpath(f'//li[@data-value="{inst_id}"]')

    driver.scroll_to_element(sedm_element)

    # wait for the little animation - 2 seconds is plenty
    ActionChains(driver).pause(2).perform()

    # wait for the second little animation - 2 seconds is plenty
    driver.scroll_to_element_and_click(sedm_element)
    ActionChains(driver).pause(2).perform()

    driver.wait_for_xpath_to_be_clickable('//body').click()
    try:
        driver.wait_for_xpath_to_be_clickable('//div[@id="selectGroups"]').click()
    except ElementClickInterceptedException:
        # time.sleep(3)
        try:
            driver.wait_for_xpath_to_be_clickable('//div[@id="selectGroups"]').click()
        except ElementClickInterceptedException:
            raise
    driver.wait_for_xpath_to_be_clickable(f'//li[text()="{public_group.name}"]').click()
    driver.execute_script(
        "arguments[0].click();",
        driver.wait_for_xpath('//*[text()="Preview in Tabular Form"]'),
    )
    driver.wait_for_xpath('//div[text()="58001"]')
    driver.execute_script(
        "arguments[0].click();",
        driver.wait_for_xpath('//*[text()="Upload Photometry"]'),
    )
    driver.wait_for_xpath('//*[contains(.,"Upload successful. Your upload ID is")]')


@pytest.mark.flaky(reruns=2)
def test_upload_photometry_multiple_groups(
    driver,
    sedm,
    super_admin_user_two_groups,
    public_group,
    public_group2,
    public_source_two_groups,
    super_admin_token,
):
    user = super_admin_user_two_groups
    public_source = public_source_two_groups
    inst_id = sedm.id
    driver.get(f"/become_user/{user.id}")
    driver.get(f"/upload_photometry/{public_source.id}")
    csv_text_input = driver.wait_for_xpath('//textarea[@name="csvData"]')
    csv_text_input.send_keys(
        "mjd,flux,fluxerr,zp,magsys,filter\n"
        "58001,55,1,25,ab,sdssg\n"
        "58002,53,1,25,ab,sdssg"
    )
    inst_select = driver.wait_for_xpath('//*[@id="mui-component-select-instrumentID"]')
    driver.scroll_to_element(inst_select)
    ActionChains(driver).move_to_element(inst_select).click().pause(2).perform()

    sedm_element = driver.wait_for_xpath(f'//li[@data-value="{inst_id}"]')

    driver.scroll_to_element(sedm_element)

    # wait for the little animation - 2 seconds is plenty
    ActionChains(driver).pause(2).perform()
    driver.scroll_to_element_and_click(sedm_element)

    # wait for the second little animation - 2 seconds is plenty
    ActionChains(driver).pause(2).perform()
    driver.wait_for_xpath_to_be_clickable('//body').click()

    try:
        driver.wait_for_xpath_to_be_clickable('//div[@id="selectGroups"]').click()
    except ElementClickInterceptedException:
        # time.sleep(3)
        try:
            driver.wait_for_xpath_to_be_clickable('//div[@id="selectGroups"]').click()
        except ElementClickInterceptedException:
            raise
    driver.wait_for_xpath_to_be_clickable(f'//li[text()="{public_group.name}"]').click()
    driver.wait_for_xpath_to_be_clickable(
        f'//li[text()="{public_group2.name}"]'
    ).click()
    driver.execute_script(
        "arguments[0].click();",
        driver.wait_for_xpath('//*[text()="Preview in Tabular Form"]'),
    )
    driver.wait_for_xpath('//div[text()="58001"]')
    driver.execute_script(
        "arguments[0].click();",
        driver.wait_for_xpath('//*[text()="Upload Photometry"]'),
    )
    driver.wait_for_xpath('//*[contains(.,"Upload successful. Your upload ID is")]')


@pytest.mark.flaky(reruns=2)
def test_upload_photometry_with_altdata(
    driver, sedm, super_admin_user, public_source, super_admin_token, public_group
):
    inst_id = sedm.id
    driver.get(f"/become_user/{super_admin_user.id}")
    driver.get(f"/upload_photometry/{public_source.id}")
    csv_text_input = driver.wait_for_xpath('//textarea[@name="csvData"]')
    csv_text_input.send_keys(
        "mjd,flux,fluxerr,zp,magsys,filter,altdata.meta1,altdata.meta2\n"
        "58001,55,1,25,ab,sdssg,44.4,\"abc,abc\"\n"
        "58002,53,1,25,ab,sdssg,44.2,\"edf,edf\""
    )
    inst_select = driver.wait_for_xpath('//*[@id="mui-component-select-instrumentID"]')
    driver.scroll_to_element(inst_select)
    ActionChains(driver).move_to_element(inst_select).click().pause(2).perform()

    sedm_element = driver.wait_for_xpath(f'//li[@data-value="{inst_id}"]')

    driver.scroll_to_element(sedm_element)

    # wait for the little animation - 2 seconds is plenty
    ActionChains(driver).pause(2).perform()
    driver.scroll_to_element_and_click(sedm_element)

    # wait for the second little animation - 2 seconds is plenty
    ActionChains(driver).pause(2).perform()

    driver.wait_for_xpath_to_be_clickable('//body').click()

    try:
        driver.wait_for_xpath_to_be_clickable('//div[@id="selectGroups"]').click()
    except ElementClickInterceptedException:
        # time.sleep(3)
        try:
            driver.wait_for_xpath_to_be_clickable('//div[@id="selectGroups"]').click()
        except ElementClickInterceptedException:
            raise
    driver.wait_for_xpath_to_be_clickable(f'//li[text()="{public_group.name}"]').click()
    driver.execute_script(
        "arguments[0].click();",
        driver.wait_for_xpath('//*[text()="Preview in Tabular Form"]'),
    )
    driver.wait_for_xpath('//div[text()="58001"]')
    driver.execute_script(
        "arguments[0].click();",
        driver.wait_for_xpath('//*[text()="Upload Photometry"]'),
    )
    driver.wait_for_xpath('//*[contains(.,"Upload successful. Your upload ID is")]')


@pytest.mark.flaky(reruns=2)
def test_upload_photometry_form_validation(
    driver, sedm, super_admin_user, public_source, super_admin_token, public_group
):
    inst_id = sedm.id
    driver.get(f"/become_user/{super_admin_user.id}")
    driver.get(f"/upload_photometry/{public_source.id}")
    csv_text_input = driver.wait_for_xpath('//textarea[@name="csvData"]')
    csv_text_input.send_keys(
        "mjd,flux,fluxerr,zp,magsys,OTHER\n"
        "58001,55,1,25,ab,sdssg\n"
        "58002,53,1,25,ab,sdssg"
    )
    driver.wait_for_xpath('//*[text()="Preview in Tabular Form"]').click()
    driver.wait_for_xpath(
        '//div[contains(.,"Invalid input: Missing required column: filter")]'
    )
    csv_text_input.clear()
    csv_text_input.send_keys(
        "mjd,flux,fluxerr,zp,magsys,filter\n"
        "58001,55,1,25,ab,sdssg\n"
        "58002,53,1,25,ab"
    )
    driver.wait_for_xpath(
        '//div[contains(.,"Invalid input: All data rows must have the same number of columns as header row")]'
    )
    csv_text_input.clear()
    csv_text_input.send_keys("mjd,flux,fluxerr,zp,magsys,filter")
    driver.wait_for_xpath(
        '//div[contains(.,"Invalid input: There must be a header row and one or more data rows")]'
    )
    csv_text_input.clear()
    csv_text_input.send_keys(
        "mjd,flux,fluxerr,zp,magsys,filter\n"
        "58001,55,1,25,ab,sdssg\n"
        "58002,53,1,25,ab,sdssg"
    )
    driver.wait_for_xpath('//div[contains(.,"Select an instrument")]')

    inst_select = driver.wait_for_xpath('//*[@id="mui-component-select-instrumentID"]')
    driver.scroll_to_element(inst_select)
    ActionChains(driver).move_to_element(inst_select).click().pause(2).perform()

    sedm_element = driver.wait_for_xpath(f'//li[@data-value="{inst_id}"]')

    driver.scroll_to_element(sedm_element)

    # wait for the little animation - 2 seconds is plenty
    ActionChains(driver).pause(2).perform()

    driver.scroll_to_element_and_click(sedm_element)

    # wait for the second little animation - 2 seconds is plenty
    ActionChains(driver).pause(2).perform()

    driver.wait_for_xpath_to_be_clickable('//body').click()

    driver.wait_for_xpath('//div[contains(.,"Select at least one group")]')
    driver.wait_for_xpath_to_be_clickable('//body').click()
    try:
        driver.wait_for_xpath_to_be_clickable('//div[@id="selectGroups"]').click()
    except ElementClickInterceptedException:
        # time.sleep(3)
        try:
            driver.wait_for_xpath_to_be_clickable('//div[@id="selectGroups"]').click()
        except ElementClickInterceptedException:
            raise
    driver.wait_for_xpath_to_be_clickable(f'//li[text()="{public_group.name}"]').click()
    driver.execute_script(
        "arguments[0].click();",
        driver.wait_for_xpath('//*[text()="Preview in Tabular Form"]'),
    )
    driver.wait_for_xpath('//div[text()="58001"]')
