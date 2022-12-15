import goto
page = <Page url='http://0.0.0.0:5000/urls/3'>


def test_site_is_invalid(page):
    page.goto('/')
    page.locator('input[name="url"]').type('http://wrong.com')
    page.locator('input[type="submit"]').click()
    assert page.locator('text=Страница успешно добавлена').is_visible()
    page.locator('text=Запустить проверку').click()
    assert page.locator('text=Произошла ошибка при проверке').is_visible()

test_site_is_invalid(page)