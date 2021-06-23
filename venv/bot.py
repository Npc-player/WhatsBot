from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import _thread
import threading
import pickle
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


def start(numeros, msg, anexo):
    x = _thread.start_new_thread(navegador, (numeros, msg, anexo,))

def navegador(numeros, msg, anexo):
    # apagando arquivos de log
    la = open('Lista_sucesso.txt', mode='w', encoding='UTF16')
    la.write(datetime.now().strftime('%d-%m-%Y' + ' ## ' +  '%H:%M:%S'))
    la.close()
    le = open('lista_com_erros.txt', mode='w', encoding='UTF16')
    le.write(datetime.now().strftime('%d-%m-%Y' + ' ## ' +  '%H:%M:%S'))
    le.close()
    anexo = anexo.replace('/','\\\\')
    try:
        os.mkdir('selenium_profile')
        os.mkdir('TEMP')
    except:
        pass
####### CONFIGURAÇÕES DO NAVEGADOR
    chromeoptions = Options()
    downloadfolder = (os.getcwd() + '\\TEMP\\')
    preferencia = {'download.default_directory': downloadfolder, "directory_upgrade": True,
                   "safebrowsing.enabled": True}  # , "new_chrome_options.headless": True}  # configurando navegador para pasta Download em TEMP
    chromeoptions.add_experimental_option('prefs', preferencia)
    chromeoptions.add_argument('--user-data-dir=' + os.getcwd() + '\\selenium_profile') # PASTA COM COOKIES
########### FIM CONFIGURAÇÕES DO NAVEGADOR

    driver = webdriver.Chrome(options=chromeoptions, executable_path=os.getcwd() + '\\chromedriver.exe')
    driver.get('https://web.whatsapp.com')
    try:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div/div[1]/div[1]/div[3]/div/div[2]")))
    except Exception as erro:
        print('Erro = ', erro)
        log_de_erros = open(os.getcwd() + '\\' + 'lista_com_erros.txt', mode='r', encoding='UTF16')
        conteudo = log_de_erros.readlines()
        conteudo.append('###############################\n' , erro , ' Erro de abertura do Whatsapp Web - Tente novamente\n')
        log_de_erros = open(os.getcwd() + '\\' + 'lista_com_erros.txt', mode='w', encoding='UTF16')
        log_de_erros.writelines(conteudo)
        log_de_erros.close()
        sleep(1)

    for i in numeros:
        driver.get('https://web.whatsapp.com/send?phone=%2B55' + str(i) + '&text&app_absent=0')
        try:
            status = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[1]'))).text
            print('status = ', status)
            sleep(2)
            if status == 'Digite uma mensagem':
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[2]/div/div[2]"))).send_keys(msg)
                sleep(3)
                #### criação do log de acertos
                log_de_acertos = open(os.getcwd() + '\\' + 'Lista_sucesso.txt', mode='r', encoding='UTF16')
                conteudo = log_de_acertos.readlines()
                conteudo.append('\n#######################################################\n' + i + ' Mensagem OK=  ' + msg + '\n')
                log_de_acertos = open(os.getcwd() + '\\' + 'Lista_sucesso.txt', mode='w', encoding='UTF16')
                log_de_acertos.writelines(conteudo)
                log_de_acertos.close()
                sleep(1)

#########   ANEXO
            if anexo != 'SEM ANEXO':
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[1]/div[2]/div/div"))).click()
                sleep(2)
                elemento = driver.find_element_by_css_selector("input[type='file']")
                elemento.send_keys(anexo)
                sleep(1)
                elemento2 = driver.find_element_by_css_selector("span[data-icon='send']")
                elemento2.click()
                sleep(2)
                log_de_acertos = open(os.getcwd() + '\\' + 'Lista_sucesso.txt', mode='r', encoding='UTF16')
                conteudo = log_de_acertos.readlines()
                conteudo.append(i + ' Anexo ok\n################################\n')
                log_de_acertos = open(os.getcwd() + '\\' + 'Lista_sucesso.txt', mode='w', encoding='UTF16')
                log_de_acertos.writelines(conteudo)
                log_de_acertos.close()
                sleep(1)
            else:
                log_de_acertos = open(os.getcwd() + '\\' + 'Lista_sucesso.txt', mode='r', encoding='UTF16')
                conteudo = log_de_acertos.readlines()
                conteudo.append(i + ' SEM ANEXO - ok\n#######################################################\n')
                log_de_acertos = open(os.getcwd() + '\\' + 'Lista_sucesso.txt', mode='w', encoding='UTF16')
                log_de_acertos.writelines(conteudo)
                log_de_acertos.close()
                sleep(1)
        except Exception as select:
            print(f'*** Número errado/Erro de conexão *** : {select}')
            # encontrar o texto número inexistente
            erro = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div[1]'))).text
            if erro == ('O número de telefone compartilhado através de url é inválido.'):
                log_de_erros = open(os.getcwd() + '\\' + 'lista_com_erros.txt', mode='r', encoding='UTF16')
                conteudo = log_de_erros.readlines()
                conteudo.append('\nNúmeros errados= ' + i + '\n#######################################################\n')
                log_de_erros = open(os.getcwd() + '\\' + 'lista_com_erros.txt', mode='w', encoding='UTF16')
                log_de_erros.writelines(conteudo)
                log_de_erros.close()
                sleep(1)
    os.system("taskkill /f /im chromedriver.exe /T")
