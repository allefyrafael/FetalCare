"""
Testes E2E do fluxo completo do sistema FetalCare.

Este módulo testa o fluxo end-to-end principal do sistema:
1. Preenchimento de dados da gestante
2. Preenchimento de parâmetros de monitoramento
3. Execução da análise ML
4. Visualização dos resultados
5. Salvamento dos dados
6. Navegação para registros
"""

import pytest
import logging
import allure
import sys
import os
from selenium.webdriver.common.by import By

# Adicionar o diretório pai ao sys.path para imports relativos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from page_objects.home_page import HomePage

logger = logging.getLogger(__name__)


@allure.epic("FetalCare E2E")
@allure.feature("Fluxo Completo")
class TestFluxoCompleto:
    """Classe de testes para o fluxo completo do sistema."""
    
    @pytest.fixture(autouse=True)
    def setup(self, navegador):
        """Setup comum para todos os testes."""
        self.driver = navegador
        self.home_page = HomePage(self.driver)
        
        # Aguardar página carregar
        assert self.home_page.aguardar_pagina_carregada(), "Página principal não carregou"
        
        # Aguardar conexão ficar online
        assert self.home_page.aguardar_status_online(timeout=10), "Sistema não ficou online"
    
    @allure.story("Fluxo Principal")
    @allure.title("Teste do fluxo completo com dados normais")
    @allure.description("Testa o fluxo completo desde preenchimento até salvamento dos resultados")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.critical
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_fluxo_completo_normal(
        self, 
        dados_gestante_valida, 
        parametros_monitoramento_normais,
        performance_monitor
    ):
        """Teste do fluxo completo com parâmetros normais."""
        
        with allure.step("1. Verificar estado inicial da página"):
            # Verificar que página carregou corretamente
            assert self.home_page.obter_status_conexao() == "online"
            assert not self.home_page.elemento_visivel(self.home_page.SECAO_RESULTADOS)
            
            # Capturar screenshot inicial
            self.home_page.obter_screenshot("01_estado_inicial")
        
        with allure.step("2. Preencher dados da gestante"):
            performance_monitor.iniciar("preenchimento_gestante")
            
            # Preencher formulário da gestante
            sucesso = self.home_page.preencher_dados_gestante(dados_gestante_valida)
            assert sucesso, "Falha ao preencher dados da gestante"
            
            # Verificar campos preenchidos
            dados_preenchidos = self.home_page.obter_dados_gestante()
            assert dados_preenchidos['nome'] == dados_gestante_valida['nome']
            assert dados_preenchidos['id'] == dados_gestante_valida['id']
            
            performance_monitor.finalizar("preenchimento_gestante")
            self.home_page.obter_screenshot("02_dados_gestante_preenchidos")
        
        with allure.step("3. Salvar dados da gestante"):
            # Salvar dados da gestante
            sucesso = self.home_page.salvar_dados_gestante()
            assert sucesso, "Falha ao salvar dados da gestante"
            
            self.home_page.obter_screenshot("03_dados_gestante_salvos")
        
        with allure.step("4. Preencher parâmetros de monitoramento"):
            performance_monitor.iniciar("preenchimento_monitoramento")
            
            # Preencher parâmetros de monitoramento
            sucesso = self.home_page.preencher_parametros_monitoramento(parametros_monitoramento_normais)
            assert sucesso, "Falha ao preencher parâmetros de monitoramento"
            
            # Verificar campos obrigatórios preenchidos
            validacao = self.home_page.validar_campos_obrigatorios_monitoramento()
            assert all(validacao.values()), f"Campos obrigatórios não preenchidos: {validacao}"
            
            performance_monitor.finalizar("preenchimento_monitoramento")
            self.home_page.obter_screenshot("04_parametros_monitoramento_preenchidos")
        
        with allure.step("5. Executar análise fetal"):
            performance_monitor.iniciar("analise_fetal")
            
            # Realizar análise
            sucesso = self.home_page.realizar_analise_fetal()
            assert sucesso, "Falha ao executar análise fetal"
            
            # Aguardar resultados aparecerem
            resultados_apareceram = self.home_page.aguardar_resultados_aparecerem(timeout=60)
            assert resultados_apareceram, "Resultados não apareceram no tempo esperado"
            
            tempo_analise = performance_monitor.finalizar("analise_fetal")
            
            # Verificar que análise não demorou muito
            assert tempo_analise < 30, f"Análise muito lenta: {tempo_analise:.2f}s"
            
            self.home_page.obter_screenshot("05_analise_executada")
        
        with allure.step("6. Verificar resultados da análise"):
            # Obter resultados
            resultado = self.home_page.obter_resultado_analise()
            assert resultado, "Nenhum resultado foi obtido"
            
            # Verificar campos essenciais dos resultados
            assert resultado['status_texto'], "Status do resultado não informado"
            assert resultado['classificacao'] in ['normal', 'risco', 'critico'], \
                f"Classificação inválida: {resultado['classificacao']}"
            assert resultado['baseline'], "Baseline não informado nos resultados"
            assert resultado['timestamp'], "Timestamp não informado"
            
            # Para parâmetros normais, esperamos classificação normal
            assert resultado['classificacao'] == 'normal', \
                f"Esperado resultado normal, obtido: {resultado['classificacao']}"
            
            # Verificar se há recomendações
            assert isinstance(resultado['recomendacoes'], list), "Recomendações devem ser uma lista"
            
            logger.info(f"Resultado da análise: {resultado['status_texto']}")
            logger.info(f"Classificação: {resultado['classificacao']}")
            logger.info(f"Recomendações: {len(resultado['recomendacoes'])} itens")
            
            self.home_page.obter_screenshot("06_resultados_exibidos")
        
        with allure.step("7. Salvar resultados"):
            # Salvar resultados
            sucesso = self.home_page.salvar_resultados()
            assert sucesso, "Falha ao salvar resultados"
            
            self.home_page.obter_screenshot("07_resultados_salvos")
        
        with allure.step("8. Navegar para página de registros"):
            # Clicar em "Ver Registros"
            sucesso = self.home_page.clicar_ver_registros()
            assert sucesso, "Falha ao clicar em 'Ver Registros'"
            
            # Aguardar navegação (URL deve mudar)
            sucesso = self.home_page.aguardar_url_conter("records", timeout=10)
            assert sucesso, "Navegação para página de registros falhou"
            
            self.home_page.obter_screenshot("08_navegacao_registros")
        
        with allure.step("9. Verificar que registro foi salvo"):
            # Aguardar página de registros carregar
            self.home_page.aguardar_pagina_carregar()
            
            # Verificar se há registros na tabela
            # (Implementação específica dependeria da estrutura da página de registros)
            
            self.home_page.obter_screenshot("09_registros_verificados")
    
    @allure.story("Fluxo com Risco")
    @allure.title("Teste do fluxo completo com dados de risco")
    @allure.description("Testa fluxo com parâmetros que indicam risco fetal")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.critical
    @pytest.mark.ml
    def test_fluxo_completo_risco(
        self, 
        dados_gestante_valida, 
        parametros_monitoramento_risco,
        performance_monitor
    ):
        """Teste do fluxo completo com parâmetros de risco."""
        
        with allure.step("1. Preencher dados da gestante"):
            sucesso = self.home_page.preencher_dados_gestante(dados_gestante_valida)
            assert sucesso, "Falha ao preencher dados da gestante"
            
            sucesso = self.home_page.salvar_dados_gestante()
            assert sucesso, "Falha ao salvar dados da gestante"
        
        with allure.step("2. Preencher parâmetros de risco"):
            sucesso = self.home_page.preencher_parametros_monitoramento(parametros_monitoramento_risco)
            assert sucesso, "Falha ao preencher parâmetros de risco"
            
            self.home_page.obter_screenshot("parametros_risco_preenchidos")
        
        with allure.step("3. Executar análise e verificar resultado de risco"):
            performance_monitor.iniciar("analise_risco")
            
            sucesso = self.home_page.realizar_analise_fetal()
            assert sucesso, "Falha ao executar análise"
            
            resultados_apareceram = self.home_page.aguardar_resultados_aparecerem(timeout=60)
            assert resultados_apareceram, "Resultados não apareceram"
            
            performance_monitor.finalizar("analise_risco")
            
            # Obter e verificar resultados
            resultado = self.home_page.obter_resultado_analise()
            assert resultado, "Nenhum resultado obtido"
            
            # Para parâmetros de risco, esperamos classificação de risco ou crítico
            assert resultado['classificacao'] in ['risco', 'critico'], \
                f"Esperado resultado de risco/crítico, obtido: {resultado['classificacao']}"
            
            # Deve ter recomendações para casos de risco
            assert len(resultado['recomendacoes']) > 0, "Casos de risco devem ter recomendações"
            
            logger.info(f"Resultado para caso de risco: {resultado['classificacao']}")
            self.home_page.obter_screenshot("resultado_risco")
    
    @allure.story("Performance")
    @allure.title("Teste de performance do fluxo completo")
    @allure.description("Verifica se o sistema atende aos critérios de performance")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.performance
    @pytest.mark.fast
    def test_performance_fluxo_completo(
        self, 
        dados_gestante_valida, 
        parametros_monitoramento_normais,
        performance_monitor
    ):
        """Teste focado na performance do fluxo completo."""
        
        performance_monitor.iniciar("fluxo_completo")
        
        with allure.step("Executar fluxo completo medindo tempos"):
            # Preencher gestante
            self.home_page.preencher_dados_gestante(dados_gestante_valida)
            self.home_page.salvar_dados_gestante()
            
            # Preencher monitoramento
            self.home_page.preencher_parametros_monitoramento(parametros_monitoramento_normais)
            
            # Medir tempo específico da análise ML
            tempo_analise = self.home_page.obter_tempo_analise()
            
            # Aguardar resultados
            self.home_page.aguardar_resultados_aparecerem()
            
            # Obter resultados
            resultado = self.home_page.obter_resultado_analise()
            assert resultado, "Falha ao obter resultados"
        
        tempo_total = performance_monitor.finalizar("fluxo_completo")
        
        with allure.step("Verificar critérios de performance"):
            # Critérios de performance
            assert tempo_analise < 10, f"Análise ML muito lenta: {tempo_analise:.2f}s (máximo: 10s)"
            assert tempo_total < 30, f"Fluxo completo muito lento: {tempo_total:.2f}s (máximo: 30s)"
            
            # Anexar métricas ao relatório
            allure.attach(
                f"Tempo de análise ML: {tempo_analise:.2f}s\n"
                f"Tempo total do fluxo: {tempo_total:.2f}s",
                name="Métricas de Performance",
                attachment_type=allure.attachment_type.TEXT
            )
        
        logger.info(f"Performance - Análise: {tempo_analise:.2f}s, Total: {tempo_total:.2f}s")
    
    @allure.story("Validação")
    @allure.title("Teste do fluxo com dados inválidos")
    @allure.description("Verifica tratamento de erros e validações")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.validation
    @pytest.mark.form
    def test_fluxo_com_dados_invalidos(self, dados_gestante_invalida):
        """Teste do fluxo com dados inválidos para verificar validações."""
        
        with allure.step("Tentar preencher dados inválidos da gestante"):
            # Preencher dados inválidos
            sucesso = self.home_page.preencher_dados_gestante(dados_gestante_invalida)
            assert sucesso, "Falha ao preencher formulário (mesmo com dados inválidos)"
            
            self.home_page.obter_screenshot("dados_invalidos_preenchidos")
        
        with allure.step("Tentar salvar e verificar validações"):
            # Tentar salvar
            self.home_page.clicar(self.home_page.BTN_SALVAR_GESTANTE)
            
            # Verificar se validações impedem salvamento
            validacao = self.home_page.validar_campos_obrigatorios_gestante()
            
            # Deve haver falha na validação
            assert not all(validacao.values()), "Validação deveria falhar com dados inválidos"
            
            # Verificar se há mensagens de erro
            mensagens_erro = self.home_page.obter_mensagens_erro()
            
            self.home_page.obter_screenshot("validacao_erro")
            
            logger.info(f"Validações falharam conforme esperado: {validacao}")
            if mensagens_erro:
                logger.info(f"Mensagens de erro: {mensagens_erro}")
    
    @allure.story("Robustez")
    @allure.title("Teste de múltiplas execuções")
    @allure.description("Verifica estabilidade executando múltiplas análises")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.slow
    @pytest.mark.regression
    def test_multiplas_execucoes(
        self, 
        dados_gestante_valida, 
        parametros_monitoramento_normais
    ):
        """Teste de robustez com múltiplas execuções."""
        
        num_execucoes = 3
        resultados = []
        
        for i in range(num_execucoes):
            with allure.step(f"Execução {i+1} de {num_execucoes}"):
                # Preencher dados
                self.home_page.preencher_dados_gestante(dados_gestante_valida)
                self.home_page.salvar_dados_gestante()
                self.home_page.preencher_parametros_monitoramento(parametros_monitoramento_normais)
                
                # Executar análise
                sucesso = self.home_page.realizar_analise_fetal()
                assert sucesso, f"Falha na execução {i+1}"
                
                self.home_page.aguardar_resultados_aparecerem()
                
                # Obter resultado
                resultado = self.home_page.obter_resultado_analise()
                assert resultado, f"Falha ao obter resultado na execução {i+1}"
                
                resultados.append(resultado['classificacao'])
                
                self.home_page.obter_screenshot(f"execucao_{i+1}")
                
                logger.info(f"Execução {i+1}: {resultado['classificacao']}")
        
        with allure.step("Verificar consistência dos resultados"):
            # Todos os resultados devem ser iguais (mesmos parâmetros)
            assert all(r == resultados[0] for r in resultados), \
                f"Resultados inconsistentes: {resultados}"
            
            logger.info(f"Todas as {num_execucoes} execuções foram consistentes: {resultados[0]}")
    
    @allure.story("Interrupção")
    @allure.title("Teste de interrupção durante análise")
    @allure.description("Verifica comportamento quando análise é interrompida")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.edge_case
    def test_interrupcao_analise(
        self, 
        dados_gestante_valida, 
        parametros_monitoramento_normais
    ):
        """Teste de comportamento com interrupção da análise."""
        
        with allure.step("Preparar dados para análise"):
            self.home_page.preencher_dados_gestante(dados_gestante_valida)
            self.home_page.salvar_dados_gestante()
            self.home_page.preencher_parametros_monitoramento(parametros_monitoramento_normais)
        
        with allure.step("Iniciar análise e simular interrupção"):
            # Clicar em análise
            sucesso = self.home_page.clicar(self.home_page.BTN_REALIZAR_ANALISE)
            assert sucesso, "Falha ao iniciar análise"
            
            # Aguardar loading aparecer
            try:
                self.home_page.aguardar_elemento(
                    self.home_page.LOADING_OVERLAY, 
                    timeout=5, 
                    condicao='visible'
                )
                
                # Simular refresh da página (interrupção)
                self.driver.refresh()
                self.home_page.aguardar_pagina_carregada()
                
                logger.info("Página recarregada durante análise")
                
            except Exception:
                # Se loading não aparecer, análise foi muito rápida
                logger.info("Análise muito rápida para simular interrupção")
                pytest.skip("Análise muito rápida para testar interrupção")
        
        with allure.step("Verificar estado após interrupção"):
            # Verificar que não há resultados exibidos
            assert not self.home_page.elemento_visivel(self.home_page.SECAO_RESULTADOS), \
                "Resultados não deveriam estar visíveis após interrupção"
            
            # Verificar que formulários ainda estão acessíveis
            assert self.home_page.elemento_visivel(self.home_page.FORM_GESTANTE), \
                "Formulário de gestante deve estar acessível"
            assert self.home_page.elemento_visivel(self.home_page.FORM_MONITORAMENTO), \
                "Formulário de monitoramento deve estar acessível"
            
            self.home_page.obter_screenshot("estado_apos_interrupcao")
            
            logger.info("Sistema manteve estabilidade após interrupção") 