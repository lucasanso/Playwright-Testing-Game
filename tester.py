from time import sleep
from playwright.sync_api import sync_playwright
import words
import pandas as pd

# A intenção com esse tester aqui é jogar um monte de palavra no jogo contexto.

class TesterContext:
    def __init__(self, words):
        print("Iniciando testador de palavras")
        self.words = words

    def execute(self):
        with sync_playwright() as p:
            browser = p.firefox.launch(
                headless=False
            )
            page = browser.new_page()
            page.goto("https://contexto.me/pt/")
            page.wait_for_selector(".word")
            page.click(".word")
            
            for w in self.words:
                if page.query_selector(".message"):
                    page.fill(".word", "")

                    # Alternativa abaixo:
                    # page.keyboard.press("Control+A")
                    # page.keyboard.press("Delete")

                page.type(".word", w, delay=100)
                page.keyboard.press("Enter")  

                sleep(1)

        browser.close()

if __name__ == "__main__":
    try:
        with open('palavras.csv', 'r') as w:
            df = pd.read_csv(w)
            column_words = df["palavra"]

            # all_words = words.PALAVRAS["ESPORTES"] + words.PALAVRAS["CINEMA"] + words.PALAVRAS["NOTÍCIA"] + words.PALAVRAS["OBJETOS"] 
            bot = TesterContext(column_words)
            
            bot.execute()
    except:
        print("Não foi possível abrir o arquivo palavras.csv")
            