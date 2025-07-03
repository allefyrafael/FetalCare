"""
Configurações e fixtures compartilhadas para testes E2E do FetalCare.

Este módulo contém:
- Configuração do WebDriver
- Fixtures de dados de teste
- Hooks do pytest
- Utilitários compartilhados
"""

import os
import json
import pytest
import logging
from datetime import datetime
from typing import Dict, Any, Generator
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configurações globais
BASE_URL = os.getenv('FETALCARE_BASE_URL', 'http://localhost:8080')
API_URL = os.getenv('FETALCARE_API_URL', 'http://localhost:5001')
HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
SCREENSHOT_ON_FAILURE = os.getenv('SCREENSHOT_ON_FAILURE', 'true').lower() == 'true'
DEFAULT_TIMEOUT = int(os.getenv('DEFAULT_TIMEOUT', '10'))

# Criar diretórios necessários
os.makedirs('evidencias/screenshots', exist_ok=True)
os.makedirs('evidencias/logs', exist_ok=True)
os.makedirs('relatorios/html', exist_ok=True)
os.makedirs('relatorios/allure-results', exist_ok=True)


def pytest_addoption(parser):
    """Adicionar opções customizadas ao pytest."""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Executar testes em modo headless"
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Navegador para execução (chrome, firefox, edge)"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default=BASE_URL,
        help="URL base da aplicação"
    )
    parser.addoption(
        "--capture-screenshots",
        action="store_true",
        default=False,
        help="Capturar screenshots sempre"
    )
    parser.addoption(
        "--timeout",
        action="store",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="Timeout padrão em segundos"
    )


@pytest.fixture(scope="session")
def config(request) -> Dict[str, Any]:
    """Configurações globais dos testes."""
    return {
        'base_url': request.config.getoption("--base-url"),
        'api_url': API_URL,
        'headless': request.config.getoption("--headless") or HEADLESS,
        'browser': request.config.getoption("--browser"),
        'capture_screenshots': request.config.getoption("--capture-screenshots"),
        'timeout': request.config.getoption("--timeout"),
        'screenshot_on_failure': SCREENSHOT_ON_FAILURE
    }


@pytest.fixture(scope="session")
def verify_services(config):
    """Verificar se os serviços estão rodando antes dos testes."""
    logger.info("Verificando serviços do FetalCare...")
    
    # Verificar frontend
    try:
        response = requests.get(config['base_url'], timeout=10)
        assert response.status_code == 200, f"Frontend não está rodando em {config['base_url']}"
        logger.info(f"✅ Frontend rodando em {config['base_url']}")
    except Exception as e:
        pytest.fail(f"❌ Frontend não acessível: {e}")
    
    # Verificar API
    try:
        response = requests.get(f"{config['api_url']}/health", timeout=10)
        assert response.status_code == 200, f"API não está rodando em {config['api_url']}"
        logger.info(f"✅ API rodando em {config['api_url']}")
    except Exception as e:
        pytest.fail(f"❌ API não acessível: {e}")
    
    return True


@pytest.fixture
def driver(config, verify_services) -> Generator[webdriver.Chrome, None, None]:
    """Configurar e fornecer instância do WebDriver."""
    logger.info(f"Configurando WebDriver ({config['browser']})...")
    
    # Configurar opções do Chrome
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--start-maximized')
    
    if config['headless']:
        chrome_options.add_argument('--headless')
        logger.info("Modo headless ativado")
    
    # Desabilitar logs verbosos
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Configurar service
    service = Service(ChromeDriverManager().install())
    
    # Criar driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(config['timeout'])
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)
    
    logger.info("✅ WebDriver configurado com sucesso")
    
    yield driver
    
    # Cleanup
    logger.info("Fechando WebDriver...")
    driver.quit()


@pytest.fixture
def wait(driver, config):
    """Fornecer WebDriverWait configurado."""
    return WebDriverWait(driver, config['timeout'])


@pytest.fixture
def navegador(driver, config):
    """Navegar para página inicial do FetalCare."""
    logger.info(f"Navegando para {config['base_url']}")
    driver.get(config['base_url'])
    
    # Aguardar carregamento da página
    wait = WebDriverWait(driver, 10)
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    
    logger.info("Página inicial carregada")
    return driver


@pytest.fixture
def dados_gestante_valida():
    """Dados válidos de gestante para testes."""
    return {
        'nome': 'Maria Silva Santos',
        'id': 'P001',
        'cpf': '123.456.789-00',
        'idade_gestacional': 28,
        'idade': 30
    }


@pytest.fixture
def dados_gestante_invalida():
    """Dados inválidos de gestante para testes de validação."""
    return {
        'nome': '',  # Nome vazio
        'id': '',    # ID vazio
        'cpf': '123.456.789-99',  # CPF inválido
        'idade_gestacional': 50,  # Idade gestacional fora do limite
        'idade': 5               # Idade muito baixa
    }


@pytest.fixture
def parametros_monitoramento_normais():
    """Parâmetros de monitoramento normais."""
    return {
        'baseline_value': 140,
        'accelerations': 3,
        'fetal_movement': 5,
        'uterine_contractions': 2,
        'light_decelerations': 1,
        'severe_decelerations': 0,
        'prolongued_decelerations': 0,
        'abnormal_short_term_variability': 5,
        'mean_value_of_short_term_variability': 2.5,
        'percentage_of_time_with_abnormal_long_term_variability': 10,
        'mean_value_of_long_term_variability': 15.0,
        'histogram_width': 150,
        'histogram_min': 110,
        'histogram_max': 160,
        'histogram_number_of_peaks': 3,
        'histogram_number_of_zeroes': 0,
        'histogram_mode': 140,
        'histogram_mean': 142,
        'histogram_median': 141,
        'histogram_variance': 25,
        'histogram_tendency': 'normal'
    }


@pytest.fixture
def parametros_monitoramento_risco():
    """Parâmetros de monitoramento indicando risco."""
    return {
        'baseline_value': 180,  # Taquicardia
        'accelerations': 0,     # Sem acelerações
        'fetal_movement': 1,    # Pouco movimento
        'uterine_contractions': 8,
        'light_decelerations': 5,
        'severe_decelerations': 3,  # Decelerações severas
        'prolongued_decelerations': 2,
        'abnormal_short_term_variability': 80,  # Alta variabilidade anormal
        'mean_value_of_short_term_variability': 0.5,  # Baixa variabilidade
        'percentage_of_time_with_abnormal_long_term_variability': 90,
        'mean_value_of_long_term_variability': 5.0,
        'histogram_width': 80,
        'histogram_min': 170,
        'histogram_max': 190,
        'histogram_number_of_peaks': 1,
        'histogram_number_of_zeroes': 20,
        'histogram_mode': 180,
        'histogram_mean': 181,
        'histogram_median': 180,
        'histogram_variance': 100,
        'histogram_tendency': 'increasing'
    }


@pytest.fixture
def carregar_dados_json():
    """Carregador de dados JSON para testes."""
    def _carregar(arquivo: str) -> Dict[str, Any]:
        caminho = os.path.join('dados', arquivo)
        if os.path.exists(caminho):
            with open(caminho, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    return _carregar


def capturar_screenshot(driver, nome_teste: str, etapa: str = "") -> str:
    """Capturar screenshot com nome descritivo."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sufixo = f"_{etapa}" if etapa else ""
    nome_arquivo = f"{nome_teste}{sufixo}_{timestamp}.png"
    caminho = os.path.join('evidencias', 'screenshots', nome_arquivo)
    
    try:
        driver.save_screenshot(caminho)
        logger.info(f"Screenshot salvo: {caminho}")
        return caminho
    except Exception as e:
        logger.error(f"Erro ao salvar screenshot: {e}")
        return ""


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook para capturar informações de execução dos testes."""
    outcome = yield
    rep = outcome.get_result()
    
    # Adicionar resultado ao item para uso em outras fixtures
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(autouse=True)
def capturar_evidencias(request, driver, config):
    """Capturar evidências automaticamente em caso de falha."""
    yield
    
    # Verificar se o teste falhou
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        if config['screenshot_on_failure']:
            nome_teste = request.node.name
            capturar_screenshot(driver, nome_teste, "falha")
            
        # Salvar HTML da página
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            html_path = os.path.join('evidencias', 'screenshots', f"{request.node.name}_falha_{timestamp}.html")
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            logger.info(f"HTML da página salvo: {html_path}")
        except Exception as e:
            logger.error(f"Erro ao salvar HTML: {e}")


@pytest.fixture
def aguardar_elemento():
    """Utilitário para aguardar elementos de forma customizada."""
    def _aguardar(driver, localizador, timeout=10, condicao='presence'):
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        
        wait = WebDriverWait(driver, timeout)
        
        condicoes = {
            'presence': EC.presence_of_element_located,
            'visible': EC.visibility_of_element_located,
            'clickable': EC.element_to_be_clickable,
            'invisible': EC.invisibility_of_element_located
        }
        
        if condicao not in condicoes:
            raise ValueError(f"Condição inválida: {condicao}")
            
        return wait.until(condicoes[condicao](localizador))
    
    return _aguardar


@pytest.fixture
def limpar_dados_teste():
    """Limpar dados de teste após execução (se necessário)."""
    yield
    # Aqui poderia haver lógica para limpar dados de teste
    # Por exemplo, remover registros criados durante o teste
    logger.info("Limpeza de dados de teste concluída")


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Configurar ambiente de teste no início da sessão."""
    logger.info("=== INICIANDO SESSÃO DE TESTES E2E ===")
    logger.info(f"Base URL: {BASE_URL}")
    logger.info(f"API URL: {API_URL}")
    logger.info(f"Headless: {HEADLESS}")
    
    yield
    
    logger.info("=== FINALIZANDO SESSÃO DE TESTES E2E ===")


@pytest.fixture
def performance_monitor():
    """Monitor de performance para medir tempos de execução."""
    tempos = {}
    
    def iniciar(nome: str):
        tempos[nome] = time.time()
    
    def finalizar(nome: str) -> float:
        if nome in tempos:
            duracao = time.time() - tempos[nome]
            logger.info(f"Tempo de execução '{nome}': {duracao:.2f}s")
            return duracao
        return 0.0
    
    class Monitor:
        def __init__(self):
            self.iniciar = iniciar
            self.finalizar = finalizar
    
    return Monitor()


# Configurações de timeout para diferentes tipos de operação
TIMEOUTS = {
    'page_load': 30,
    'element_wait': 10,
    'ajax_wait': 15,
    'analysis_wait': 60,
    'form_submit': 20,
    'navigation': 5
}


@pytest.fixture
def timeouts():
    """Fornecer configurações de timeout."""
    return TIMEOUTS 