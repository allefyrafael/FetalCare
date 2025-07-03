"""
Page Object para a página principal do sistema FetalCare.

Esta classe encapsula todos os elementos e ações da página index.html,
incluindo formulários de gestante e monitoramento fetal.
"""

import logging
from typing import Dict, Any, Optional
from selenium.webdriver.common.by import By
from .base_page import BasePage

logger = logging.getLogger(__name__)


class HomePage(BasePage):
    """Page Object para página principal do FetalCare."""
    
    # ========== LOCALIZADORES ==========
    
    # Header
    LOGO_TITULO = (By.CSS_SELECTOR, ".logo h1")
    BTN_VER_REGISTROS = (By.ID, "viewRecordsBtn")
    STATUS_CONEXAO = (By.ID, "connectionStatus")
    
    # Formulário da Gestante
    FORM_GESTANTE = (By.ID, "patientForm")
    INPUT_NOME_GESTANTE = (By.ID, "patientName")
    INPUT_ID_GESTANTE = (By.ID, "patientId")
    INPUT_CPF_GESTANTE = (By.ID, "patientCpf")
    INPUT_IDADE_GESTACIONAL = (By.ID, "gestationalAge")
    INPUT_IDADE_GESTANTE = (By.ID, "patientAge")
    BTN_SALVAR_GESTANTE = (By.CSS_SELECTOR, "#patientForm button[type='submit']")
    
    # Formulário de Monitoramento
    FORM_MONITORAMENTO = (By.ID, "monitoringForm")
    BTN_CARREGAR_PADROES = (By.ID, "loadDefaults")
    BTN_REALIZAR_ANALISE = (By.CSS_SELECTOR, "#monitoringForm button[type='submit']")
    
    # Campos de Frequência Cardíaca Fetal
    INPUT_BASELINE_VALUE = (By.ID, "baselineValue")
    INPUT_ACCELERATIONS = (By.ID, "accelerations")
    INPUT_FETAL_MOVEMENT = (By.ID, "fetalMovement")
    
    # Campos de Contrações e Decelerações
    INPUT_UTERINE_CONTRACTIONS = (By.ID, "uterineContractions")
    INPUT_LIGHT_DECELERATIONS = (By.ID, "lightDecelerations")
    INPUT_SEVERE_DECELERATIONS = (By.ID, "severeDecelerations")
    INPUT_PROLONGUED_DECELERATIONS = (By.ID, "prolonguedDecelerations")
    
    # Campos de Variabilidade
    INPUT_ABNORMAL_SHORT_TERM_VARIABILITY = (By.ID, "abnormalShortTermVariability")
    INPUT_MEAN_VALUE_SHORT_TERM_VARIABILITY = (By.ID, "meanValueOfShortTermVariability")
    INPUT_PERCENTAGE_ABNORMAL_LONG_TERM_VARIABILITY = (By.ID, "percentageOfTimeWithAbnormalLongTermVariability")
    INPUT_MEAN_VALUE_LONG_TERM_VARIABILITY = (By.ID, "meanValueOfLongTermVariability")
    
    # Campos do Histograma
    INPUT_HISTOGRAM_WIDTH = (By.ID, "histogramWidth")
    INPUT_HISTOGRAM_MIN = (By.ID, "histogramMin")
    INPUT_HISTOGRAM_MAX = (By.ID, "histogramMax")
    INPUT_HISTOGRAM_NUMBER_OF_PEAKS = (By.ID, "histogramNumberOfPeaks")
    INPUT_HISTOGRAM_NUMBER_OF_ZEROES = (By.ID, "histogramNumberOfZeroes")
    INPUT_HISTOGRAM_MODE = (By.ID, "histogramMode")
    INPUT_HISTOGRAM_MEAN = (By.ID, "histogramMean")
    INPUT_HISTOGRAM_MEDIAN = (By.ID, "histogramMedian")
    INPUT_HISTOGRAM_VARIANCE = (By.ID, "histogramVariance")
    SELECT_HISTOGRAM_TENDENCY = (By.ID, "histogramTendency")
    
    # Seção de Resultados
    SECAO_RESULTADOS = (By.ID, "resultsSection")
    ICONE_STATUS = (By.ID, "statusIcon")
    TEXTO_STATUS = (By.ID, "statusText")
    DESCRICAO_STATUS = (By.ID, "statusDescription")
    BARRA_STATUS = (By.ID, "statusBarFill")
    LABEL_STATUS = (By.ID, "statusLabel")
    DETALHES_RESULTADO = (By.ID, "resultDetails")
    BTN_SALVAR_RESULTADOS = (By.ID, "saveResults")
    
    # Detalhes do Resultado
    DETAIL_BASELINE = (By.ID, "detailBaseline")
    DETAIL_ACCELERATIONS = (By.ID, "detailAccelerations")
    DETAIL_MOVEMENT = (By.ID, "detailMovement")
    DETAIL_TIMESTAMP = (By.ID, "detailTimestamp")
    RECOMMENDATIONS_LIST = (By.ID, "recommendationsList")
    
    # Loading
    LOADING_OVERLAY = (By.ID, "loadingOverlay")
    NOTIFICATIONS = (By.ID, "notifications")
    
    def __init__(self, driver, timeout=10):
        """Inicializar página principal."""
        super().__init__(driver, timeout)
        logger.info("Inicializando HomePage")
    
    # ========== MÉTODOS DE NAVEGAÇÃO ==========
    
    def aguardar_pagina_carregada(self) -> bool:
        """
        Aguardar página principal carregar completamente.
        
        Returns:
            True se página carregou, False caso contrário
        """
        try:
            # Aguardar elementos principais aparecerem
            self.aguardar_elemento(self.LOGO_TITULO, timeout=15)
            self.aguardar_elemento(self.FORM_GESTANTE, timeout=10)
            self.aguardar_elemento(self.FORM_MONITORAMENTO, timeout=10)
            
            # Aguardar scripts carregarem
            self.aguardar_pagina_carregar()
            
            logger.info("Página principal carregada com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao carregar página principal: {e}")
            return False
    
    def clicar_ver_registros(self) -> bool:
        """
        Clicar no botão 'Ver Registros'.
        
        Returns:
            True se clique foi realizado, False caso contrário
        """
        sucesso = self.clicar(self.BTN_VER_REGISTROS)
        if sucesso:
            logger.info("Clicado em 'Ver Registros'")
        return sucesso
    
    def obter_status_conexao(self) -> str:
        """
        Obter status atual da conexão.
        
        Returns:
            Status da conexão
        """
        try:
            elemento = self.aguardar_elemento(self.STATUS_CONEXAO)
            classes = elemento.get_attribute("class")
            texto = elemento.text
            
            if "online" in classes:
                status = "online"
            elif "offline" in classes:
                status = "offline"
            else:
                status = "checking"
            
            logger.debug(f"Status da conexão: {status} - {texto}")
            return status
        except Exception as e:
            logger.error(f"Erro ao obter status da conexão: {e}")
            return "unknown"
    
    # ========== MÉTODOS DO FORMULÁRIO DE GESTANTE ==========
    
    def preencher_dados_gestante(self, dados: Dict[str, Any]) -> bool:
        """
        Preencher formulário de dados da gestante.
        
        Args:
            dados: Dicionário com os dados da gestante
                - nome: Nome da gestante
                - id: ID da gestante  
                - cpf: CPF da gestante (opcional)
                - idade_gestacional: Idade gestacional em semanas
                - idade: Idade da gestante (opcional)
        
        Returns:
            True se preenchimento foi realizado, False caso contrário
        """
        try:
            logger.info("Preenchendo dados da gestante")
            
            # Aguardar formulário estar visível
            self.aguardar_elemento(self.FORM_GESTANTE, condicao='visible')
            
            # Preencher campos obrigatórios
            if 'nome' in dados:
                self.digitar(self.INPUT_NOME_GESTANTE, dados['nome'])
                
            if 'id' in dados:
                self.digitar(self.INPUT_ID_GESTANTE, dados['id'])
                
            if 'idade_gestacional' in dados:
                self.digitar(self.INPUT_IDADE_GESTACIONAL, str(dados['idade_gestacional']))
            
            # Preencher campos opcionais
            if 'cpf' in dados and dados['cpf']:
                self.digitar(self.INPUT_CPF_GESTANTE, dados['cpf'])
                
            if 'idade' in dados and dados['idade']:
                self.digitar(self.INPUT_IDADE_GESTANTE, str(dados['idade']))
            
            logger.info("Dados da gestante preenchidos com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao preencher dados da gestante: {e}")
            return False
    
    def salvar_dados_gestante(self) -> bool:
        """
        Salvar dados da gestante clicando no botão submit.
        
        Returns:
            True se salvamento foi realizado, False caso contrário
        """
        try:
            sucesso = self.clicar(self.BTN_SALVAR_GESTANTE)
            if sucesso:
                logger.info("Dados da gestante salvos")
                # Aguardar possível mensagem de sucesso ou carregamento
                self.aguardar_ajax()
            return sucesso
        except Exception as e:
            logger.error(f"Erro ao salvar dados da gestante: {e}")
            return False
    
    def obter_dados_gestante(self) -> Dict[str, str]:
        """
        Obter dados atualmente preenchidos no formulário da gestante.
        
        Returns:
            Dicionário com os dados preenchidos
        """
        try:
            dados = {
                'nome': self.obter_atributo(self.INPUT_NOME_GESTANTE, 'value'),
                'id': self.obter_atributo(self.INPUT_ID_GESTANTE, 'value'),
                'cpf': self.obter_atributo(self.INPUT_CPF_GESTANTE, 'value'),
                'idade_gestacional': self.obter_atributo(self.INPUT_IDADE_GESTACIONAL, 'value'),
                'idade': self.obter_atributo(self.INPUT_IDADE_GESTANTE, 'value')
            }
            logger.debug(f"Dados da gestante obtidos: {dados}")
            return dados
        except Exception as e:
            logger.error(f"Erro ao obter dados da gestante: {e}")
            return {}
    
    # ========== MÉTODOS DO FORMULÁRIO DE MONITORAMENTO ==========
    
    def carregar_padroes_monitoramento(self) -> bool:
        """
        Carregar valores padrão no formulário de monitoramento.
        
        Returns:
            True se padrões foram carregados, False caso contrário
        """
        try:
            sucesso = self.clicar(self.BTN_CARREGAR_PADROES)
            if sucesso:
                logger.info("Padrões de monitoramento carregados")
                # Aguardar campos serem preenchidos
                self.aguardar_ajax()
            return sucesso
        except Exception as e:
            logger.error(f"Erro ao carregar padrões: {e}")
            return False
    
    def preencher_parametros_monitoramento(self, parametros: Dict[str, Any]) -> bool:
        """
        Preencher formulário de parâmetros de monitoramento.
        
        Args:
            parametros: Dicionário com parâmetros de monitoramento
        
        Returns:
            True se preenchimento foi realizado, False caso contrário
        """
        try:
            logger.info("Preenchendo parâmetros de monitoramento")
            
            # Aguardar formulário estar visível
            self.aguardar_elemento(self.FORM_MONITORAMENTO, condicao='visible')
            
            # Mapeamento de campos
            campos = {
                'baseline_value': self.INPUT_BASELINE_VALUE,
                'accelerations': self.INPUT_ACCELERATIONS,
                'fetal_movement': self.INPUT_FETAL_MOVEMENT,
                'uterine_contractions': self.INPUT_UTERINE_CONTRACTIONS,
                'light_decelerations': self.INPUT_LIGHT_DECELERATIONS,
                'severe_decelerations': self.INPUT_SEVERE_DECELERATIONS,
                'prolongued_decelerations': self.INPUT_PROLONGUED_DECELERATIONS,
                'abnormal_short_term_variability': self.INPUT_ABNORMAL_SHORT_TERM_VARIABILITY,
                'mean_value_of_short_term_variability': self.INPUT_MEAN_VALUE_SHORT_TERM_VARIABILITY,
                'percentage_of_time_with_abnormal_long_term_variability': self.INPUT_PERCENTAGE_ABNORMAL_LONG_TERM_VARIABILITY,
                'mean_value_of_long_term_variability': self.INPUT_MEAN_VALUE_LONG_TERM_VARIABILITY,
                'histogram_width': self.INPUT_HISTOGRAM_WIDTH,
                'histogram_min': self.INPUT_HISTOGRAM_MIN,
                'histogram_max': self.INPUT_HISTOGRAM_MAX,
                'histogram_number_of_peaks': self.INPUT_HISTOGRAM_NUMBER_OF_PEAKS,
                'histogram_number_of_zeroes': self.INPUT_HISTOGRAM_NUMBER_OF_ZEROES,
                'histogram_mode': self.INPUT_HISTOGRAM_MODE,
                'histogram_mean': self.INPUT_HISTOGRAM_MEAN,
                'histogram_median': self.INPUT_HISTOGRAM_MEDIAN,
                'histogram_variance': self.INPUT_HISTOGRAM_VARIANCE
            }
            
            # Preencher campos
            for chave, localizador in campos.items():
                if chave in parametros and parametros[chave] is not None:
                    valor = str(parametros[chave])
                    self.digitar(localizador, valor)
                    logger.debug(f"Preenchido {chave}: {valor}")
            
            # Selecionar tendência do histograma
            if 'histogram_tendency' in parametros and parametros['histogram_tendency']:
                self.selecionar_dropdown(self.SELECT_HISTOGRAM_TENDENCY, parametros['histogram_tendency'])
                logger.debug(f"Selecionada tendência: {parametros['histogram_tendency']}")
            
            logger.info("Parâmetros de monitoramento preenchidos com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao preencher parâmetros de monitoramento: {e}")
            return False
    
    def realizar_analise_fetal(self) -> bool:
        """
        Realizar análise fetal clicando no botão de análise.
        
        Returns:
            True se análise foi iniciada, False caso contrário
        """
        try:
            # Clicar no botão de análise
            sucesso = self.clicar(self.BTN_REALIZAR_ANALISE)
            if sucesso:
                logger.info("Análise fetal iniciada")
                
                # Aguardar loading aparecer e desaparecer
                self.aguardar_loading_desaparecer(timeout=60)
                
                return True
            return False
            
        except Exception as e:
            logger.error(f"Erro ao realizar análise fetal: {e}")
            return False
    
    # ========== MÉTODOS DOS RESULTADOS ==========
    
    def aguardar_resultados_aparecerem(self, timeout: int = 60) -> bool:
        """
        Aguardar seção de resultados aparecer após análise.
        
        Args:
            timeout: Timeout em segundos
        
        Returns:
            True se resultados apareceram, False caso contrário
        """
        try:
            # Aguardar seção de resultados ficar visível
            self.aguardar_elemento(self.SECAO_RESULTADOS, timeout=timeout, condicao='visible')
            
            # Aguardar detalhes aparecerem
            self.aguardar_elemento(self.DETALHES_RESULTADO, timeout=10, condicao='visible')
            
            logger.info("Resultados da análise aparecerem")
            return True
            
        except Exception as e:
            logger.error(f"Timeout aguardando resultados: {e}")
            return False
    
    def obter_resultado_analise(self) -> Dict[str, Any]:
        """
        Obter resultados da análise fetal.
        
        Returns:
            Dicionário com os resultados da análise
        """
        try:
            # Aguardar resultados estarem visíveis
            if not self.elemento_visivel(self.SECAO_RESULTADOS):
                return {}
            
            resultado = {
                'status_texto': self.obter_texto(self.TEXTO_STATUS),
                'status_descricao': self.obter_texto(self.DESCRICAO_STATUS),
                'status_label': self.obter_texto(self.LABEL_STATUS),
                'baseline': self.obter_texto(self.DETAIL_BASELINE),
                'accelerations': self.obter_texto(self.DETAIL_ACCELERATIONS),
                'movement': self.obter_texto(self.DETAIL_MOVEMENT),
                'timestamp': self.obter_texto(self.DETAIL_TIMESTAMP)
            }
            
            # Obter recomendações
            try:
                lista_recomendacoes = self.encontrar_elementos((By.CSS_SELECTOR, "#recommendationsList li"))
                resultado['recomendacoes'] = [item.text for item in lista_recomendacoes]
            except Exception:
                resultado['recomendacoes'] = []
            
            # Obter classe do ícone de status para determinar tipo
            try:
                icone = self.encontrar_elemento(self.ICONE_STATUS)
                if icone:
                    parent = icone.find_element(By.XPATH, "..")
                    classes = parent.get_attribute("class") or ""
                    if "normal" in classes:
                        resultado['classificacao'] = "normal"
                    elif "risk" in classes or "suspect" in classes:
                        resultado['classificacao'] = "risco"
                    elif "critical" in classes or "pathologic" in classes:
                        resultado['classificacao'] = "critico"
                    else:
                        resultado['classificacao'] = "unknown"
            except Exception:
                resultado['classificacao'] = "unknown"
            
            logger.info(f"Resultado obtido: {resultado['status_texto']} - {resultado['classificacao']}")
            return resultado
            
        except Exception as e:
            logger.error(f"Erro ao obter resultado da análise: {e}")
            return {}
    
    def salvar_resultados(self) -> bool:
        """
        Salvar resultados da análise.
        
        Returns:
            True se resultados foram salvos, False caso contrário
        """
        try:
            if not self.elemento_visivel(self.BTN_SALVAR_RESULTADOS):
                logger.warning("Botão de salvar resultados não está visível")
                return False
                
            sucesso = self.clicar(self.BTN_SALVAR_RESULTADOS)
            if sucesso:
                logger.info("Resultados salvos")
                # Aguardar possível confirmação
                self.aguardar_ajax()
            return sucesso
            
        except Exception as e:
            logger.error(f"Erro ao salvar resultados: {e}")
            return False
    
    def obter_tempo_analise(self) -> float:
        """
        Medir tempo de execução da análise ML.
        
        Returns:
            Tempo em segundos ou 0 se erro
        """
        try:
            import time
            
            # Marcar início
            inicio = time.time()
            
            # Aguardar loading aparecer
            try:
                self.aguardar_elemento(self.LOADING_OVERLAY, timeout=5, condicao='visible')
            except Exception:
                pass  # Loading pode não aparecer
            
            # Aguardar loading desaparecer
            self.aguardar_loading_desaparecer(timeout=60)
            
            # Calcular tempo
            tempo_total = time.time() - inicio
            logger.info(f"Tempo de análise: {tempo_total:.2f}s")
            return tempo_total
            
        except Exception as e:
            logger.error(f"Erro ao medir tempo de análise: {e}")
            return 0.0
    
    # ========== MÉTODOS DE VALIDAÇÃO ==========
    
    def validar_campos_obrigatorios_gestante(self) -> Dict[str, bool]:
        """
        Validar se campos obrigatórios do formulário de gestante estão preenchidos.
        
        Returns:
            Dicionário com status de validação de cada campo
        """
        try:
            validacao = {}
            
            # Verificar campos obrigatórios
            campos_obrigatorios = {
                'nome': self.INPUT_NOME_GESTANTE,
                'id': self.INPUT_ID_GESTANTE,
                'idade_gestacional': self.INPUT_IDADE_GESTACIONAL
            }
            
            for nome, localizador in campos_obrigatorios.items():
                valor = self.obter_atributo(localizador, 'value')
                validacao[nome] = bool(valor and valor.strip())
            
            logger.debug(f"Validação campos gestante: {validacao}")
            return validacao
            
        except Exception as e:
            logger.error(f"Erro ao validar campos obrigatórios: {e}")
            return {}
    
    def validar_campos_obrigatorios_monitoramento(self) -> Dict[str, bool]:
        """
        Validar se campos obrigatórios do monitoramento estão preenchidos.
        
        Returns:
            Dicionário com status de validação de cada campo
        """
        try:
            validacao = {}
            
            # Verificar campos obrigatórios principais
            campos_obrigatorios = {
                'baseline_value': self.INPUT_BASELINE_VALUE,
                'accelerations': self.INPUT_ACCELERATIONS,
                'fetal_movement': self.INPUT_FETAL_MOVEMENT,
                'mean_value_of_short_term_variability': self.INPUT_MEAN_VALUE_SHORT_TERM_VARIABILITY,
                'mean_value_of_long_term_variability': self.INPUT_MEAN_VALUE_LONG_TERM_VARIABILITY
            }
            
            for nome, localizador in campos_obrigatorios.items():
                valor = self.obter_atributo(localizador, 'value')
                validacao[nome] = bool(valor and valor.strip())
            
            logger.debug(f"Validação campos monitoramento: {validacao}")
            return validacao
            
        except Exception as e:
            logger.error(f"Erro ao validar campos obrigatórios monitoramento: {e}")
            return {}
    
    def obter_mensagens_erro(self) -> list:
        """
        Obter mensagens de erro de validação exibidas na página.
        
        Returns:
            Lista de mensagens de erro
        """
        try:
            # Procurar por diferentes tipos de mensagens de erro
            seletores_erro = [
                ".error-message",
                ".alert-danger",
                ".validation-error",
                "[role='alert']"
            ]
            
            mensagens = []
            for seletor in seletores_erro:
                elementos = self.encontrar_elementos((By.CSS_SELECTOR, seletor))
                for elemento in elementos:
                    if elemento.is_displayed():
                        texto = elemento.text.strip()
                        if texto:
                            mensagens.append(texto)
            
            logger.debug(f"Mensagens de erro encontradas: {mensagens}")
            return mensagens
            
        except Exception as e:
            logger.error(f"Erro ao obter mensagens de erro: {e}")
            return [] 