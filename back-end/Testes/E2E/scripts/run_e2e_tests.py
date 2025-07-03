#!/usr/bin/env python3
"""
Script executor principal dos testes E2E do FetalCare.

Este script fornece uma interface interativa para executar diferentes
tipos de testes E2E com configurações personalizadas.
"""

import os
import sys
import subprocess
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Adicionar diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

try:
    import colorama
    from colorama import Fore, Back, Style
    colorama.init()
except ImportError:
    # Se colorama não estiver disponível, usar strings vazias
    class MockColor:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = ""
        RESET = ""
    
    Fore = MockColor()
    Back = MockColor()
    Style = MockColor()
    Style.RESET_ALL = ""


class TestExecutor:
    """Executor de testes E2E com interface interativa."""
    
    def __init__(self):
        """Inicializar executor."""
        self.projeto_root = Path(__file__).parent.parent
        self.resultados_dir = self.projeto_root / "relatorios"
        self.evidencias_dir = self.projeto_root / "evidencias"
        
        # Criar diretórios se não existirem
        self.resultados_dir.mkdir(exist_ok=True)
        self.evidencias_dir.mkdir(exist_ok=True)
        (self.evidencias_dir / "screenshots").mkdir(exist_ok=True)
        (self.evidencias_dir / "logs").mkdir(exist_ok=True)
    
    def print_header(self):
        """Imprimir cabeçalho do script."""
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🧪 EXECUTOR DE TESTES E2E - SISTEMA FETALCARE 🧪{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Sistema de monitoramento fetal com análise por Machine Learning{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Testes automatizados End-to-End com Selenium WebDriver{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    def verificar_prerequisitos(self) -> bool:
        """Verificar se pré-requisitos estão atendidos."""
        print(f"{Fore.YELLOW}🔍 Verificando pré-requisitos...{Style.RESET_ALL}")
        
        verificacoes = []
        
        # Verificar Python
        try:
            python_version = sys.version
            verificacoes.append(("Python", True, f"Versão: {python_version.split()[0]}"))
        except Exception as e:
            verificacoes.append(("Python", False, str(e)))
        
        # Verificar pytest
        try:
            result = subprocess.run(["pytest", "--version"], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                verificacoes.append(("pytest", True, result.stdout.strip()))
            else:
                verificacoes.append(("pytest", False, "Comando falhou"))
        except Exception as e:
            verificacoes.append(("pytest", False, str(e)))
        
        # Verificar Selenium
        try:
            import selenium
            verificacoes.append(("Selenium", True, f"Versão: {selenium.__version__}"))
        except ImportError:
            verificacoes.append(("Selenium", False, "Módulo não encontrado"))
        
        # Verificar ChromeDriver (tentativa)
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            
            driver_path = ChromeDriverManager().install()
            verificacoes.append(("ChromeDriver", True, f"Disponível em: {driver_path}"))
        except Exception as e:
            verificacoes.append(("ChromeDriver", False, str(e)))
        
        # Verificar serviços (opcional)
        import requests
        
        # Frontend
        try:
            response = requests.get("http://localhost:8080", timeout=5)
            if response.status_code == 200:
                verificacoes.append(("Frontend (8080)", True, "Respondendo"))
            else:
                verificacoes.append(("Frontend (8080)", False, f"Status: {response.status_code}"))
        except Exception:
            verificacoes.append(("Frontend (8080)", False, "Não acessível"))
        
        # API
        try:
            response = requests.get("http://localhost:5001/health", timeout=5)
            if response.status_code == 200:
                verificacoes.append(("API (5001)", True, "Respondendo"))
            else:
                verificacoes.append(("API (5001)", False, f"Status: {response.status_code}"))
        except Exception:
            verificacoes.append(("API (5001)", False, "Não acessível"))
        
        # Mostrar resultados
        print("\n📋 Status dos Pré-requisitos:")
        todos_ok = True
        for nome, ok, detalhes in verificacoes:
            status_icon = "✅" if ok else "❌"
            cor = Fore.GREEN if ok else Fore.RED
            print(f"  {status_icon} {cor}{nome:<20}{Style.RESET_ALL} - {detalhes}")
            if not ok and nome in ["Python", "pytest", "Selenium", "ChromeDriver"]:
                todos_ok = False
        
        if not todos_ok:
            print(f"\n{Fore.RED}⚠️  Alguns pré-requisitos essenciais estão faltando.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 Execute: pip install -r requirements.txt{Style.RESET_ALL}")
            return False
        
        print(f"\n{Fore.GREEN}✅ Pré-requisitos essenciais atendidos!{Style.RESET_ALL}")
        
        # Avisar sobre serviços se não estiverem rodando
        servicos_ok = any("Frontend" in v[0] and v[1] for v in verificacoes) and \
                     any("API" in v[0] and v[1] for v in verificacoes)
        
        if not servicos_ok:
            print(f"\n{Fore.YELLOW}⚠️  Serviços FetalCare não estão rodando.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   Alguns testes podem falhar. Inicie o sistema antes de continuar.{Style.RESET_ALL}")
        
        return True
    
    def mostrar_menu_principal(self) -> str:
        """Mostrar menu principal e obter escolha do usuário."""
        opcoes = {
            "1": ("🎯 Executar Fluxo Completo", "Teste do fluxo principal end-to-end"),
            "2": ("📝 Executar Testes de Formulário", "Validações de campos e preenchimento"),
            "3": ("🤖 Executar Testes de Análise ML", "Testes específicos da análise de ML"),
            "4": ("🔍 Executar Testes de Validação", "Testes de validação e tratamento de erros"),
            "5": ("📱 Executar Testes de Responsividade", "Testes em diferentes resoluções"),
            "6": ("🚀 Executar TODOS os Testes", "Suite completa de testes E2E"),
            "7": ("📊 Gerar Relatório", "Gerar relatório dos últimos testes"),
            "8": ("🔧 Configurações", "Ajustar configurações de execução"),
            "9": ("❓ Ajuda", "Informações sobre uso dos testes"),
            "0": ("🚪 Sair", "Encerrar programa")
        }
        
        print(f"\n{Fore.BLUE}📋 MENU PRINCIPAL{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{'─' * 50}{Style.RESET_ALL}")
        
        for key, (titulo, descricao) in opcoes.items():
            print(f"  {Fore.WHITE}{key}{Style.RESET_ALL} - {Fore.CYAN}{titulo}{Style.RESET_ALL}")
            print(f"      {Fore.WHITE}{descricao}{Style.RESET_ALL}")
        
        print(f"{Fore.BLUE}{'─' * 50}{Style.RESET_ALL}")
        
        while True:
            escolha = input(f"\n{Fore.YELLOW}👉 Escolha uma opção (0-9): {Style.RESET_ALL}").strip()
            if escolha in opcoes:
                return escolha
            print(f"{Fore.RED}❌ Opção inválida. Tente novamente.{Style.RESET_ALL}")
    
    def executar_pytest(
        self, 
        argumentos: List[str], 
        titulo: str,
        descricao: str = ""
    ) -> bool:
        """
        Executar pytest com argumentos específicos.
        
        Args:
            argumentos: Lista de argumentos para pytest
            titulo: Título da execução
            descricao: Descrição adicional
        
        Returns:
            True se execução foi bem-sucedida, False caso contrário
        """
        print(f"\n{Fore.GREEN}🚀 {titulo}{Style.RESET_ALL}")
        if descricao:
            print(f"{Fore.WHITE}{descricao}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{'─' * 60}{Style.RESET_ALL}")
        
        # Preparar comando
        cmd = ["pytest"] + argumentos
        
        print(f"{Fore.YELLOW}📝 Comando: {' '.join(cmd)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}⏰ Iniciando em 3 segundos...{Style.RESET_ALL}")
        time.sleep(3)
        
        # Mudar para diretório do projeto
        os.chdir(self.projeto_root)
        
        # Executar
        start_time = time.time()
        try:
            result = subprocess.run(cmd, cwd=self.projeto_root, timeout=1800)  # 30 min timeout
            execution_time = time.time() - start_time
            
            if result.returncode == 0:
                print(f"\n{Fore.GREEN}✅ Execução concluída com sucesso!{Style.RESET_ALL}")
                print(f"{Fore.GREEN}⏱️  Tempo total: {execution_time:.1f} segundos{Style.RESET_ALL}")
                return True
            else:
                print(f"\n{Fore.RED}❌ Execução falhou com código: {result.returncode}{Style.RESET_ALL}")
                print(f"{Fore.RED}⏱️  Tempo até falha: {execution_time:.1f} segundos{Style.RESET_ALL}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"\n{Fore.RED}⏰ Timeout! Execução excedeu 30 minutos.{Style.RESET_ALL}")
            return False
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⏹️  Execução interrompida pelo usuário.{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"\n{Fore.RED}💥 Erro durante execução: {e}{Style.RESET_ALL}")
            return False
    
    def obter_configuracoes_execucao(self) -> Dict[str, any]:
        """Obter configurações personalizadas do usuário."""
        print(f"\n{Fore.BLUE}⚙️  CONFIGURAÇÕES DE EXECUÇÃO{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{'─' * 40}{Style.RESET_ALL}")
        
        config = {}
        
        # Modo headless
        resposta = input(f"{Fore.YELLOW}🖥️  Executar em modo headless (sem interface gráfica)? [s/N]: {Style.RESET_ALL}").strip().lower()
        config['headless'] = resposta in ['s', 'sim', 'y', 'yes']
        
        # Captura de screenshots
        resposta = input(f"{Fore.YELLOW}📸 Capturar screenshots sempre (não só em falhas)? [s/N]: {Style.RESET_ALL}").strip().lower()
        config['screenshots'] = resposta in ['s', 'sim', 'y', 'yes']
        
        # Execução paralela
        resposta = input(f"{Fore.YELLOW}⚡ Executar testes em paralelo? [S/n]: {Style.RESET_ALL}").strip().lower()
        config['paralelo'] = resposta not in ['n', 'nao', 'no']
        
        # Número de workers se paralelo
        if config['paralelo']:
            while True:
                try:
                    workers = input(f"{Fore.YELLOW}👥 Número de workers (auto/1-8) [auto]: {Style.RESET_ALL}").strip()
                    if not workers or workers.lower() == 'auto':
                        config['workers'] = 'auto'
                        break
                    else:
                        num = int(workers)
                        if 1 <= num <= 8:
                            config['workers'] = str(num)
                            break
                        else:
                            print(f"{Fore.RED}❌ Use um número entre 1 e 8{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}❌ Digite um número válido{Style.RESET_ALL}")
        
        # Timeout personalizado
        while True:
            try:
                timeout = input(f"{Fore.YELLOW}⏱️  Timeout para testes em segundos [300]: {Style.RESET_ALL}").strip()
                if not timeout:
                    config['timeout'] = 300
                    break
                else:
                    num = int(timeout)
                    if 30 <= num <= 1800:
                        config['timeout'] = num
                        break
                    else:
                        print(f"{Fore.RED}❌ Use um valor entre 30 e 1800 segundos{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}❌ Digite um número válido{Style.RESET_ALL}")
        
        return config
    
    def construir_argumentos_pytest(self, tipo: str, config: Dict[str, any] = None) -> List[str]:
        """
        Construir argumentos para pytest baseado no tipo de teste e configurações.
        
        Args:
            tipo: Tipo de teste a executar
            config: Configurações personalizadas
        
        Returns:
            Lista de argumentos para pytest
        """
        config = config or {}
        
        # Argumentos base
        args = [
            "-v",  # verbose
            "--tb=short",  # traceback curto
            "--strict-markers",  # marcadores estritos
            "--alluredir=relatorios/allure-results",  # relatório Allure
            "--html=relatorios/html/report.html",  # relatório HTML
            "--self-contained-html"  # HTML auto-contido
        ]
        
        # Configurações condicionais
        if config.get('headless'):
            args.append("--headless")
        
        if config.get('screenshots'):
            args.append("--capture-screenshots")
        
        if config.get('paralelo') and config.get('workers'):
            args.extend(["-n", config['workers']])
        
        if config.get('timeout'):
            args.extend(["--timeout", str(config['timeout'])])
        
        # Argumentos específicos por tipo
        if tipo == "fluxo_completo":
            args.extend([
                "cenarios/test_fluxo_completo.py",
                "-m", "critical or smoke"
            ])
        elif tipo == "formularios":
            args.extend([
                "cenarios/test_formulario_gestante.py",
                "cenarios/test_monitoramento.py",
                "-m", "form"
            ])
        elif tipo == "analise_ml":
            args.extend([
                "cenarios/test_analise_ml.py",
                "-m", "ml"
            ])
        elif tipo == "validacoes":
            args.extend([
                "cenarios/test_validacoes.py",
                "-m", "validation"
            ])
        elif tipo == "responsividade":
            args.extend([
                "cenarios/test_responsividade.py",
                "-m", "mobile or tablet or desktop"
            ])
        elif tipo == "todos":
            args.extend([
                "cenarios/",
                "--maxfail=10"  # Parar após 10 falhas
            ])
        
        return args
    
    def gerar_relatorio_allure(self) -> bool:
        """Gerar e abrir relatório Allure."""
        print(f"\n{Fore.BLUE}📊 Gerando relatório Allure...{Style.RESET_ALL}")
        
        allure_results = self.resultados_dir / "allure-results"
        allure_report = self.resultados_dir / "allure-report"
        
        if not allure_results.exists() or not any(allure_results.iterdir()):
            print(f"{Fore.RED}❌ Nenhum resultado de teste encontrado.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 Execute alguns testes primeiro.{Style.RESET_ALL}")
            return False
        
        try:
            # Gerar relatório
            subprocess.run([
                "allure", "generate", str(allure_results), 
                "-o", str(allure_report), "--clean"
            ], check=True, timeout=60)
            
            print(f"{Fore.GREEN}✅ Relatório gerado com sucesso!{Style.RESET_ALL}")
            
            # Perguntar se quer abrir
            resposta = input(f"{Fore.YELLOW}🌐 Abrir relatório no navegador? [S/n]: {Style.RESET_ALL}").strip().lower()
            if resposta not in ['n', 'nao', 'no']:
                subprocess.run(["allure", "open", str(allure_report)], check=True)
                print(f"{Fore.GREEN}🌐 Relatório aberto no navegador!{Style.RESET_ALL}")
            
            return True
            
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}❌ Erro ao gerar relatório Allure.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 Verifique se o Allure está instalado: npm install -g allure-commandline{Style.RESET_ALL}")
            return False
        except FileNotFoundError:
            print(f"{Fore.RED}❌ Allure não encontrado.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 Instale o Allure: npm install -g allure-commandline{Style.RESET_ALL}")
            return False
    
    def mostrar_ajuda(self):
        """Mostrar informações de ajuda."""
        help_text = f"""
{Fore.CYAN}📚 AJUDA - TESTES E2E FETALCARE{Style.RESET_ALL}
{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}

{Fore.YELLOW}🎯 TIPOS DE TESTE:{Style.RESET_ALL}

{Fore.GREEN}• Fluxo Completo{Style.RESET_ALL}
  Testa o ciclo completo: gestante → monitoramento → análise → resultados
  Tempo estimado: 2-5 minutos por teste

{Fore.GREEN}• Testes de Formulário{Style.RESET_ALL}
  Validações de campos, preenchimento e salvamento
  Tempo estimado: 1-3 minutos

{Fore.GREEN}• Testes de Análise ML{Style.RESET_ALL}
  Foco na funcionalidade de Machine Learning
  Tempo estimado: 3-8 minutos

{Fore.GREEN}• Testes de Validação{Style.RESET_ALL}
  Tratamento de erros e dados inválidos
  Tempo estimado: 2-4 minutos

{Fore.GREEN}• Testes de Responsividade{Style.RESET_ALL}
  Layout em diferentes resoluções (mobile, tablet, desktop)
  Tempo estimado: 5-10 minutos

{Fore.YELLOW}🔧 PRÉ-REQUISITOS:{Style.RESET_ALL}
• Python 3.8+
• Google Chrome (versão atual)
• Sistema FetalCare rodando:
  - Frontend: http://localhost:8080
  - Backend: http://localhost:5001

{Fore.YELLOW}📋 INSTALAÇÃO:{Style.RESET_ALL}
1. pip install -r requirements.txt
2. python scripts/setup_chromedriver.py (opcional)

{Fore.YELLOW}📊 RELATÓRIOS:{Style.RESET_ALL}
• HTML: relatorios/html/report.html
• Allure: relatorios/allure-report/
• Screenshots: evidencias/screenshots/
• Logs: evidencias/logs/

{Fore.YELLOW}⚡ EXECUÇÃO RÁPIDA:{Style.RESET_ALL}
• pytest cenarios/test_fluxo_completo.py -v
• pytest -m smoke --headless
• pytest -n auto (paralelo)

{Fore.YELLOW}🐛 SOLUÇÃO DE PROBLEMAS:{Style.RESET_ALL}
• ChromeDriver: python scripts/setup_chromedriver.py
• Timeout: Use --timeout=60 para mais tempo
• Headless: Use --headless se não precisar ver o navegador
• Logs: Verifique evidencias/logs/pytest.log
"""
        print(help_text)
        input(f"\n{Fore.YELLOW}📖 Pressione Enter para continuar...{Style.RESET_ALL}")
    
    def run(self):
        """Executar interface principal."""
        # Verificar se estamos no diretório correto
        if not (Path.cwd() / "requirements.txt").exists():
            print(f"{Fore.RED}❌ Execute este script do diretório E2E{Style.RESET_ALL}")
            return
        
        self.print_header()
        
        # Verificar pré-requisitos
        if not self.verificar_prerequisitos():
            resposta = input(f"\n{Fore.YELLOW}❓ Continuar mesmo assim? [s/N]: {Style.RESET_ALL}").strip().lower()
            if resposta not in ['s', 'sim', 'y', 'yes']:
                print(f"{Fore.YELLOW}👋 Até mais!{Style.RESET_ALL}")
                return
        
        # Loop principal
        while True:
            try:
                escolha = self.mostrar_menu_principal()
                
                if escolha == "0":
                    print(f"\n{Fore.GREEN}👋 Obrigado por usar os testes E2E do FetalCare!{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}🎯 Sistema de monitoramento fetal - Qualidade garantida{Style.RESET_ALL}")
                    break
                
                elif escolha == "1":
                    config = self.obter_configuracoes_execucao()
                    args = self.construir_argumentos_pytest("fluxo_completo", config)
                    self.executar_pytest(
                        args,
                        "Executando Testes de Fluxo Completo",
                        "Testando o fluxo principal end-to-end do sistema"
                    )
                
                elif escolha == "2":
                    config = self.obter_configuracoes_execucao()
                    args = self.construir_argumentos_pytest("formularios", config)
                    self.executar_pytest(
                        args,
                        "Executando Testes de Formulário",
                        "Testando validações e preenchimento de formulários"
                    )
                
                elif escolha == "3":
                    config = self.obter_configuracoes_execucao()
                    args = self.construir_argumentos_pytest("analise_ml", config)
                    self.executar_pytest(
                        args,
                        "Executando Testes de Análise ML",
                        "Testando funcionalidade de Machine Learning"
                    )
                
                elif escolha == "4":
                    config = self.obter_configuracoes_execucao()
                    args = self.construir_argumentos_pytest("validacoes", config)
                    self.executar_pytest(
                        args,
                        "Executando Testes de Validação",
                        "Testando tratamento de erros e validações"
                    )
                
                elif escolha == "5":
                    config = self.obter_configuracoes_execucao()
                    args = self.construir_argumentos_pytest("responsividade", config)
                    self.executar_pytest(
                        args,
                        "Executando Testes de Responsividade",
                        "Testando layout em diferentes resoluções"
                    )
                
                elif escolha == "6":
                    print(f"\n{Fore.YELLOW}⚠️  ATENÇÃO: Suite completa pode demorar 15-30 minutos{Style.RESET_ALL}")
                    resposta = input(f"{Fore.YELLOW}❓ Continuar? [s/N]: {Style.RESET_ALL}").strip().lower()
                    if resposta in ['s', 'sim', 'y', 'yes']:
                        config = self.obter_configuracoes_execucao()
                        args = self.construir_argumentos_pytest("todos", config)
                        self.executar_pytest(
                            args,
                            "Executando TODOS os Testes E2E",
                            "Suite completa de testes End-to-End"
                        )
                
                elif escolha == "7":
                    self.gerar_relatorio_allure()
                
                elif escolha == "8":
                    config = self.obter_configuracoes_execucao()
                    print(f"\n{Fore.GREEN}✅ Configurações salvas para próxima execução:{Style.RESET_ALL}")
                    for key, value in config.items():
                        print(f"  {Fore.CYAN}{key}{Style.RESET_ALL}: {value}")
                
                elif escolha == "9":
                    self.mostrar_ajuda()
                
                # Perguntar se quer continuar após execução
                if escolha in ["1", "2", "3", "4", "5", "6"]:
                    input(f"\n{Fore.YELLOW}📖 Pressione Enter para voltar ao menu...{Style.RESET_ALL}")
                
            except KeyboardInterrupt:
                print(f"\n\n{Fore.YELLOW}⏹️  Interrompido pelo usuário.{Style.RESET_ALL}")
                resposta = input(f"{Fore.YELLOW}❓ Sair do programa? [S/n]: {Style.RESET_ALL}").strip().lower()
                if resposta not in ['n', 'nao', 'no']:
                    break
            except Exception as e:
                print(f"\n{Fore.RED}💥 Erro inesperado: {e}{Style.RESET_ALL}")
                input(f"{Fore.YELLOW}📖 Pressione Enter para continuar...{Style.RESET_ALL}")


if __name__ == "__main__":
    executor = TestExecutor()
    executor.run() 