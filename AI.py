from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import html2text
import pyperclip
import pyautogui
import time
import textwrap
def convert_to_you_com_link(query):
    encoded_query = query.replace(' ', '%20').replace('+', '%2B').replace('/', '%2F')
    link = f"https://you.com/search?q={encoded_query}&fromSearchBar=true&tbm=youchat"
    return link

def run(playwright,query):
    browser = playwright.chromium.launch()
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    url=convert_to_you_com_link(query)
    page = context.new_page()
    page.goto(url)
    page.wait_for_selector('//div[@data-testid="reset-button"]')
    html_content = page.content()
    soup = BeautifulSoup(html_content, 'html.parser')
    parent_element = soup.find('div', {'data-testid': 'youchat-answer-turn-0'})
    h = html2text.HTML2Text()
    final_content = h.handle(parent_element.decode_contents())
    pyperclip.copy(final_content)
    pyautogui.typewrite("\n'''")
    time.sleep(0.1)
    pyautogui.hotkey('ctrl','v')
    time.sleep(0.3)
    browser.close()

def generate(query):

    with sync_playwright() as p:
        run(p,query)
