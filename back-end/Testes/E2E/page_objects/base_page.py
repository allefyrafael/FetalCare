"""
Classe base para Page Objects do sistema FetalCare.

Esta classe fornece funcionalidades comuns que serão herdadas
por todas as páginas do sistema.
"""

import logging
from typing import List, Optional, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

logger = logging.getLogger(__name__)


class BasePage:
    """Classe base para Page Objects com funcionalidades comuns."""
    
    def __init__(self, driver: webdriver.Chrome, timeout: int = 10):
        """
        Inicializar página base.
        
        Args:
            driver: Instância do WebDriver
            timeout: Timeout padrão para esperas
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        
    def get_url(self) -> str:
        """Obter URL atual da página."""
        return self.driver.current_url
    
    def get_title(self) -> str:
        """Obter título da página."""
        return self.driver.title
    
    def aguardar_elemento(
        self, 
        localizador: Tuple[str, str], 
        timeout: Optional[int] = None,
        condicao: str = 'presence'
    ) -> WebElement:
        """
        Aguardar elemento aparecer na página.
        
        Args:
            localizador: Tupla (By, valor) para localizar elemento
            timeout: Timeout personalizado (usa self.timeout se None)
            condicao: Tipo de condição ('presence', 'visible', 'clickable', 'invisible')
        
        Returns:
            WebElement encontrado
        
        Raises:
            TimeoutException: Se elemento não for encontrado
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        
        condicoes = {
            'presence': EC.presence_of_element_located,
            'visible': EC.visibility_of_element_located,
            'clickable': EC.element_to_be_clickable,
            'invisible': EC.invisibility_of_element_located
        }
        
        if condicao not in condicoes:
            raise ValueError(f"Condição inválida: {condicao}. Use: {list(condicoes.keys())}")
        
        try:
            elemento = wait.until(condicoes[condicao](localizador))
            logger.debug(f"Elemento encontrado: {localizador}")
            return elemento
        except TimeoutException:
            logger.error(f"Timeout aguardando elemento: {localizador}")
            raise
    
    def aguardar_elementos(
        self, 
        localizador: Tuple[str, str], 
        timeout: Optional[int] = None
    ) -> List[WebElement]:
        """
        Aguardar lista de elementos aparecer na página.
        
        Args:
            localizador: Tupla (By, valor) para localizar elementos
            timeout: Timeout personalizado
        
        Returns:
            Lista de WebElements encontrados
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        
        try:
            elementos = wait.until(EC.presence_of_all_elements_located(localizador))
            logger.debug(f"Elementos encontrados: {len(elementos)} para {localizador}")
            return elementos
        except TimeoutException:
            logger.error(f"Timeout aguardando elementos: {localizador}")
            return []
    
    def encontrar_elemento(self, localizador: Tuple[str, str]) -> Optional[WebElement]:
        """
        Encontrar elemento sem aguardar.
        
        Args:
            localizador: Tupla (By, valor) para localizar elemento
        
        Returns:
            WebElement encontrado ou None
        """
        try:
            elemento = self.driver.find_element(*localizador)
            logger.debug(f"Elemento encontrado: {localizador}")
            return elemento
        except NoSuchElementException:
            logger.debug(f"Elemento não encontrado: {localizador}")
            return None
    
    def encontrar_elementos(self, localizador: Tuple[str, str]) -> List[WebElement]:
        """
        Encontrar lista de elementos sem aguardar.
        
        Args:
            localizador: Tupla (By, valor) para localizar elementos
        
        Returns:
            Lista de WebElements encontrados
        """
        elementos = self.driver.find_elements(*localizador)
        logger.debug(f"Elementos encontrados: {len(elementos)} para {localizador}")
        return elementos
    
    def clicar(self, localizador: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        """
        Clicar em elemento aguardando que esteja clicável.
        
        Args:
            localizador: Tupla (By, valor) para localizar elemento
            timeout: Timeout personalizado
        
        Returns:
            True se clique foi realizado, False caso contrário
        """
        try:
            elemento = self.aguardar_elemento(localizador, timeout, 'clickable')
            elemento.click()
            logger.debug(f"Clique realizado em: {localizador}")
            return True
        except Exception as e:
            logger.error(f"Erro ao clicar em {localizador}: {e}")
            return False
    
    def clicar_js(self, localizador: Tuple[str, str]) -> bool:
        """
        Clicar em elemento usando JavaScript.
        
        Args:
            localizador: Tupla (By, valor) para localizar elemento
        
        Returns:
            True se clique foi realizado, False caso contrário
        """
        try:
            elemento = self.encontrar_elemento(localizador)
            if elemento:
                self.driver.execute_script("arguments[0].click();", elemento)
                logger.debug(f"Clique JS realizado em: {localizador}")
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao clicar com JS em {localizador}: {e}")
            return False
    
    def digitar(self, localizador: Tuple[str, str], texto: str, limpar: bool = True) -> bool:
        """
        Digitar texto em campo.
        
        Args:
            localizador: Tupla (By, valor) para localizar campo
            texto: Texto a ser digitado
            limpar: Se deve limpar campo antes de digitar
        
        Returns:
            True se texto foi digitado, False caso contrário
        """
        try:
            elemento = self.aguardar_elemento(localizador, condicao='visible')
            if limpar:
                elemento.clear()
            elemento.send_keys(texto)
            logger.debug(f"Texto digitado em {localizador}: {texto}")
            return True
        except Exception as e:
            logger.error(f"Erro ao digitar em {localizador}: {e}")
            return False
    
    def obter_texto(self, localizador: Tuple[str, str]) -> str:
        """
        Obter texto de elemento.
        
        Args:
            localizador: Tupla (By, valor) para localizar elemento
        
        Returns:
            Texto do elemento ou string vazia
        """
        try:
            elemento = self.aguardar_elemento(localizador, condicao='visible')
            texto = elemento.text
            logger.debug(f"Texto obtido de {localizador}: {texto}")
            return texto
        except Exception as e:
            logger.error(f"Erro ao obter texto de {localizador}: {e}")
            return ""
    
    def obter_atributo(self, localizador: Tuple[str, str], atributo: str) -> str:
        """
        Obter atributo de elemento.
        
        Args:
            localizador: Tupla (By, valor) para localizar elemento
            atributo: Nome do atributo
        
        Returns:
            Valor do atributo ou string vazia
        """
        try:
            elemento = self.aguardar_elemento(localizador)
            valor = elemento.get_attribute(atributo) or ""
            logger.debug(f"Atributo {atributo} de {localizador}: {valor}")
            return valor
        except Exception as e:
            logger.error(f"Erro ao obter atributo {atributo} de {localizador}: {e}")
            return ""
    
    def selecionar_dropdown(self, localizador: Tuple[str, str], valor: str) -> bool:
        """
        Selecionar opção em dropdown.
        
        Args:
            localizador: Tupla (By, valor) para localizar select
            valor: Valor a ser selecionado
        
        Returns:
            True se seleção foi realizada, False caso contrário
        """
        try:
            from selenium.webdriver.support.ui import Select
            elemento = self.aguardar_elemento(localizador)
            select = Select(elemento)
            select.select_by_value(valor)
            logger.debug(f"Selecionado {valor} em {localizador}")
            return True
        except Exception as e:
            logger.error(f"Erro ao selecionar {valor} em {localizador}: {e}")
            return False
    
    def elemento_visivel(self, localizador: Tuple[str, str]) -> bool:
        """
        Verificar se elemento está visível.
        
        Args:
            localizador: Tupla (By, valor) para localizar elemento
        
        Returns:
            True se elemento está visível, False caso contrário
        """
        try:
            elemento = self.encontrar_elemento(localizador)
            return elemento is not None and elemento.is_displayed()
        except Exception:
            return False
    
    def elemento_presente(self, localizador: Tuple[str, str]) -> bool:
        """
        Verificar se elemento está presente no DOM.
        
        Args:
            localizador: Tupla (By, valor) para localizar elemento
        
        Returns:
            True se elemento está presente, False caso contrário
        """
        return self.encontrar_elemento(localizador) is not None
    
    def aguardar_pagina_carregar(self, timeout: int = 30) -> bool:
        """
        Aguardar página carregar completamente.
        
        Args:
            timeout: Timeout em segundos
        
        Returns:
            True se página carregou, False caso contrário
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            logger.debug("Página carregada completamente")
            return True
        except TimeoutException:
            logger.error("Timeout aguardando página carregar")
            return False
    
    def aguardar_ajax(self, timeout: int = 15) -> bool:
        """
        Aguardar requisições AJAX completarem (se jQuery estiver disponível).
        
        Args:
            timeout: Timeout em segundos
        
        Returns:
            True se AJAX completou, False caso contrário
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(lambda d: d.execute_script("return jQuery.active == 0"))
            logger.debug("Requisições AJAX concluídas")
            return True
        except Exception:
            # jQuery pode não estar disponível
            logger.debug("jQuery não disponível ou erro aguardando AJAX")
            return True
    
    def rolar_para_elemento(self, localizador: Tuple[str, str]) -> bool:
        """
        Rolar página até elemento ficar visível.
        
        Args:
            localizador: Tupla (By, valor) para localizar elemento
        
        Returns:
            True se elemento foi encontrado e rolagem foi feita, False caso contrário
        """
        try:
            elemento = self.aguardar_elemento(localizador)
            self.driver.execute_script("arguments[0].scrollIntoView();", elemento)
            logger.debug(f"Rolagem realizada para: {localizador}")
            return True
        except Exception as e:
            logger.error(f"Erro ao rolar para {localizador}: {e}")
            return False
    
    def hover(self, localizador: Tuple[str, str]) -> bool:
        """
        Fazer hover sobre elemento.
        
        Args:
            localizador: Tupla (By, valor) para localizar elemento
        
        Returns:
            True se hover foi realizado, False caso contrário
        """
        try:
            elemento = self.aguardar_elemento(localizador, condicao='visible')
            ActionChains(self.driver).move_to_element(elemento).perform()
            logger.debug(f"Hover realizado em: {localizador}")
            return True
        except Exception as e:
            logger.error(f"Erro ao fazer hover em {localizador}: {e}")
            return False
    
    def obter_screenshot(self, nome_arquivo: str = None) -> str:
        """
        Capturar screenshot da página.
        
        Args:
            nome_arquivo: Nome personalizado do arquivo (opcional)
        
        Returns:
            Caminho do arquivo salvo
        """
        try:
            if not nome_arquivo:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                nome_arquivo = f"screenshot_{timestamp}.png"
            
            caminho = f"evidencias/screenshots/{nome_arquivo}"
            self.driver.save_screenshot(caminho)
            logger.info(f"Screenshot salvo: {caminho}")
            return caminho
        except Exception as e:
            logger.error(f"Erro ao capturar screenshot: {e}")
            return ""
    
    def aguardar_url_conter(self, texto: str, timeout: Optional[int] = None) -> bool:
        """
        Aguardar URL conter texto específico.
        
        Args:
            texto: Texto que deve estar presente na URL
            timeout: Timeout personalizado
        
        Returns:
            True se URL contém o texto, False caso contrário
        """
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.url_contains(texto))
            logger.debug(f"URL contém '{texto}': {self.get_url()}")
            return True
        except TimeoutException:
            logger.error(f"Timeout aguardando URL conter '{texto}'. URL atual: {self.get_url()}")
            return False
    
    def executar_javascript(self, script: str, *args) -> any:
        """
        Executar JavaScript na página.
        
        Args:
            script: Código JavaScript a ser executado
            *args: Argumentos para o script
        
        Returns:
            Resultado da execução do script
        """
        try:
            resultado = self.driver.execute_script(script, *args)
            logger.debug(f"JavaScript executado: {script[:50]}...")
            return resultado
        except Exception as e:
            logger.error(f"Erro ao executar JavaScript: {e}")
            return None
    
    def aguardar_loading_desaparecer(self, timeout: int = 30) -> bool:
        """
        Aguardar indicador de loading desaparecer.
        
        Args:
            timeout: Timeout em segundos
        
        Returns:
            True se loading desapareceu, False caso contrário
        """
        loading_localizador = (By.ID, "loadingOverlay")
        try:
            # Aguardar loading aparecer (opcional)
            try:
                self.aguardar_elemento(loading_localizador, timeout=2, condicao='visible')
            except TimeoutException:
                pass  # Loading pode não aparecer
            
            # Aguardar loading desaparecer
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.invisibility_of_element_located(loading_localizador))
            logger.debug("Loading desapareceu")
            return True
        except TimeoutException:
            logger.warning("Timeout aguardando loading desaparecer")
            return False
    
    def obter_status_conexao(self) -> str:
        """
        Obter status da conexão exibido na página.
        
        Returns:
            Status da conexão ('online', 'offline', etc.)
        """
        try:
            status_elemento = self.aguardar_elemento((By.ID, "connectionStatus"))
            classes = status_elemento.get_attribute("class")
            
            if "online" in classes:
                return "online"
            elif "offline" in classes:
                return "offline"
            else:
                return "unknown"
        except Exception:
            return "unknown"
    
    def aguardar_status_online(self, timeout: int = 10) -> bool:
        """
        Aguardar status da conexão ficar online.
        
        Args:
            timeout: Timeout em segundos
        
        Returns:
            True se status ficou online, False caso contrário
        """
        for _ in range(timeout):
            if self.obter_status_conexao() == "online":
                logger.debug("Status da conexão: online")
                return True
            time.sleep(1)
        
        logger.warning("Timeout aguardando status online")
        return False 