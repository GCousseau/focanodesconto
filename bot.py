import json
import os
import time
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from datetime import datetime

class Produtos:
    def __init__(self):
        with open('links.txt', 'r', encoding='utf-8') as file:
            self.links = file.readlines()
            
        self.servico = Service(ChromeDriverManager().install())
        opcoes = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=self.servico, options=opcoes)
    
        
    def scraping_links(self):
        mercado = 'Amazon'
        tempo = ''
        imagem = ''
        nome = ''
        preco_inteiro = ''
        preco_decimal = ''
        preco = ''
        parcelas = ''
        link = ''
        avaliacao = ''
        porcentagem = '-'
        imagem_caminho = ''
        
        for url in self.links:
            self.driver.get(url)
            
            tempo = datetime.now().date()

            time.sleep(10)
            
            try:
                nome = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[6]/div[3]/div[4]/div[1]/div/h1/span').text
            except NoSuchElementException:
                print('nome não encontrado')
            
            if nome:
                parte = re.sub(r'[^a-zA-Z0-9]', '', nome)
                imagem = 'imagens/promos/' + parte + '.png'
                
            try:
                # screenshot = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[6]/div[3]/div[3]/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/ul/li[1]/span/span/div/img').screenshot(f'{imagem}')
                screenshot = self.driver.find_element(By.ID, 'landingImage')
                imagem_caminho = screenshot.get_attribute('src')
            except NoSuchElementException:
                print('imagem não encontrado')
                
            try:
                avaliacao = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[6]/div[3]/div[4]/div[4]/div/span[1]/span/span[1]/a/span').text
            except NoSuchElementException:
                print('avaliacao não encontrada')
            
            if avaliacao:
                avaliacao = 'Avaliação: ' + avaliacao + ' de 5,0'
                
            try:
                parcelas = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[6]/div[3]/div[4]/div[13]/span[1]').text
            except NoSuchElementException:
                print('parcelas não encontradas')
                
            try:
                preco_inteiro = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[6]/div[3]/div[4]/div[12]/div/div/div[3]/div[1]/span[3]/span[2]/span[2]').text
            except NoSuchElementException:
                print('preço inteiro não encontrado')    

            try:
                preco_inteiro = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[6]/div[3]/div[4]/div[12]/div/div/div[1]/div/div[3]/div[1]/span[3]/span[2]/span[2]').text
            except NoSuchElementException:
                print('preço inteiro não encontrado')   
                
            try:
                preco_decimal = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[6]/div[3]/div[4]/div[12]/div/div/div[3]/div[1]/span[3]/span[2]/span[3]').text
            except NoSuchElementException:
                print('preço decimal não encontrado') 

            try:
                preco_decimal = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[6]/div[3]/div[4]/div[12]/div/div/div[1]/div/div[3]/div[1]/span[3]/span[2]/span[3]').text
            except NoSuchElementException:
                print('preço decimal não encontrado')        
                
            try:
                porcentagem = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[6]/div[3]/div[4]/div[12]/div/div/div[3]/div[1]/span[2]').text
            except NoSuchElementException:
                print('porcentagem não encontrada')

            try:
                porcentagem = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[6]/div[3]/div[4]/div[12]/div/div/div[1]/div/div[3]/div[1]/span[2]').text
            except NoSuchElementException:
                print('porcentagem não encontrada')
            
            if porcentagem:
                porcentagem = porcentagem + ' de desconto'

            if preco_decimal and preco_inteiro:
                preco = f'R$ {preco_inteiro},{preco_decimal}'
            
            tempo = tempo.strftime('%d/%m/%Y')
            # print(imagem_caminho)
            # print(f'{nome}\n{avaliacao}\n{parcelas}\nR$ {preco_inteiro},{preco_decimal}\n{porcentagem[1:]}\n{tempo}')

            self.create_json(mercado, tempo, imagem_caminho, nome, preco, parcelas, url, avaliacao, porcentagem[1:])
            
    
    def create_json(self, mercado, tempo, imagem, nome, preco, parcelas, link, avaliacao, porcentagem):
        produto = {
            'mercado'    : mercado,
            'tempo'      : tempo,
            'imagem'     : imagem,
            'nome'       : nome,
            'preco'      : preco,
            'parcelas'   : parcelas,
            'link'       : link,
            'avaliacao'  : avaliacao,
            'porcentagem': porcentagem,
        }

        nome_arquivo = 'promocoes.json'

        if os.path.exists(nome_arquivo):
            with open(nome_arquivo, 'r', encoding='utf-8') as file:
                promocoes = json.load(file)
        else:
            promocoes = []

        promocoes.insert(0, produto)

        with open(nome_arquivo, 'w', encoding='utf-8') as file:
            json.dump(promocoes, file, ensure_ascii=False, indent=4)
            
            
produtos = Produtos()

produtos.scraping_links()