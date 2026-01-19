import random, time


def human_sleep(a=0.8, b=2.2):
    time.sleep(random.uniform(a, b))




def human_type(page, selector, text):
    el = page.locator(selector)
    el.click()
    for ch in text:
        el.type(ch, delay=random.randint(30, 120))
    human_sleep()




def human_scroll(page):
    for _ in range(random.randint(2, 5)):
        page.mouse.wheel(0, random.randint(300, 900))
        human_sleep(0.4, 1.2)   