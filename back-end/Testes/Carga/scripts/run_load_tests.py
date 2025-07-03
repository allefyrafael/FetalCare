#!/usr/bin/env python3
"""
🚀 Sistema FetalCare - Executor de Testes de Carga
Executor automático para testes de performance com Apache JMeter

Autor: Sistema de Testes de Performance
Data: 03/07/2025
Versão: 1.0.0
"""

import subprocess
import argparse
import datetime
import os
import sys
import time
import json
import xml.etree.ElementTree as ET
from pathlib import Path
import requests
from typing import Dict, List, Optional, Tuple

# Configurações
JMETER_PATH = "jmeter"  # Assumindo que está no PATH
BASE_DIR = Path(__file__).parent.parent
CENARIOS_DIR = BASE_DIR / "cenarios"
RESULTADOS_DIR = BASE_DIR / "resultados"
RELATORIOS_DIR = RESULTADOS_DIR / "relatorios_html"
LOGS_DIR = RESULTADOS_DIR / "logs"

# Criar diretórios necessários
for dir_path in [RESULTADOS_DIR, RELATORIOS_DIR, LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

class Colors:
    """Cores para output colorido"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_colored(message: str, color: str = Colors.ENDC) -> None:
    """Imprime mensagem colorida"""
    print(f"{color}{message}{Colors.ENDC}")

def print_banner():
    """Imprime banner do sistema"""
    banner = f"""
{Colors.HEADER}{'='*70}
🚀 SISTEMA FETALCARE - TESTES DE CARGA
{'='*70}{Colors.ENDC}

{Colors.OKCYAN}📊 Executor Automático de Testes de Performance
🎯 Apache JMeter Integration
🏥 Monitoramento Fetal Inteligente{Colors.ENDC}

{Colors.WARNING}⚠️  Certifique-se de que o Sistema FetalCare está rodando!
🔗 API: http://localhost:5001{Colors.ENDC}
"""
    print(banner)

def verificar_sistema_ativo() -> bool:
    """Verifica se o sistema FetalCare está ativo"""
    try:
        response = requests.get("http://localhost:5001/health", timeout=5)
        if response.status_code == 200:
            print_colored("✅ Sistema FetalCare está ativo", Colors.OKGREEN)
            return True
        else:
            print_colored(f"❌ Sistema retornou status {response.status_code}", Colors.FAIL)
            return False
    except requests.exceptions.RequestException as e:
        print_colored(f"❌ Erro ao conectar com o sistema: {e}", Colors.FAIL)
        return False

def verificar_jmeter() -> bool:
    """Verifica se JMeter está instalado"""
    try:
        result = subprocess.run([JMETER_PATH, "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print_colored(f"✅ JMeter encontrado: {version}", Colors.OKGREEN)
            return True
        else:
            print_colored("❌ JMeter não encontrado ou erro na execução", Colors.FAIL)
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print_colored(f"❌ Erro ao verificar JMeter: {e}", Colors.FAIL)
        return False

def executar_teste_jmeter(cenario: str, gerar_relatorio: bool = True, 
                         parametros_extras: Dict[str, str] = None) -> Tuple[bool, str]:
    """
    Executa teste JMeter e retorna resultado
    
    Args:
        cenario: Nome do cenário (ex: 'load_test')
        gerar_relatorio: Se deve gerar relatório HTML
        parametros_extras: Parâmetros adicionais para JMeter
    
    Returns:
        Tuple[bool, str]: (sucesso, caminho_relatorio)
    """
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Arquivos de resultado
    cenario_file = CENARIOS_DIR / f"{cenario}.jmx"
    resultado_file = RESULTADOS_DIR / f"{cenario}_{timestamp}.jtl"
    relatorio_dir = RELATORIOS_DIR / f"{cenario}_{timestamp}"
    log_file = LOGS_DIR / f"{cenario}_{timestamp}.log"
    
    # Verificar se arquivo de cenário existe
    if not cenario_file.exists():
        print_colored(f"❌ Arquivo de cenário não encontrado: {cenario_file}", Colors.FAIL)
        return False, ""
    
    # Comando JMeter
    cmd = [
        JMETER_PATH,
        "-n",  # Modo não-GUI
        "-t", str(cenario_file),
        "-l", str(resultado_file),
        "-j", str(log_file)
    ]
    
    # Adicionar relatório HTML se solicitado
    if gerar_relatorio:
        cmd.extend(["-e", "-o", str(relatorio_dir)])
    
    # Adicionar parâmetros extras
    if parametros_extras:
        for key, value in parametros_extras.items():
            cmd.extend(["-J", f"{key}={value}"])
    
    # Executar teste
    print_colored(f"🚀 Iniciando teste: {cenario}", Colors.OKBLUE)
    print_colored(f"📁 Resultado será salvo em: {resultado_file}", Colors.OKCYAN)
    
    start_time = time.time()
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)  # 1 hora timeout
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print_colored(f"✅ Teste concluído com sucesso!", Colors.OKGREEN)
            print_colored(f"⏱️  Duração: {duration:.2f} segundos", Colors.OKCYAN)
            
            if gerar_relatorio and relatorio_dir.exists():
                relatorio_html = relatorio_dir / "index.html"
                if relatorio_html.exists():
                    print_colored(f"📊 Relatório HTML: {relatorio_html}", Colors.OKGREEN)
                    return True, str(relatorio_html)
            
            return True, str(resultado_file)
        else:
            print_colored(f"❌ Erro na execução do teste", Colors.FAIL)
            print_colored(f"Stderr: {result.stderr}", Colors.FAIL)
            return False, ""
            
    except subprocess.TimeoutExpired:
        print_colored("❌ Timeout na execução do teste (1 hora)", Colors.FAIL)
        return False, ""
    except Exception as e:
        print_colored(f"❌ Erro inesperado: {e}", Colors.FAIL)
        return False, ""

def analisar_resultados(arquivo_jtl: str) -> Dict:
    """
    Analisa resultados do JMeter e extrai métricas
    
    Args:
        arquivo_jtl: Caminho para arquivo .jtl
    
    Returns:
        Dict com métricas analisadas
    """
    if not os.path.exists(arquivo_jtl):
        return {}
    
    try:
        # Parse do XML
        tree = ET.parse(arquivo_jtl)
        root = tree.getroot()
        
        # Coletar dados
        tempos_resposta = []
        sucessos = 0
        falhas = 0
        total_bytes = 0
        
        for sample in root.findall('.//httpSample') + root.findall('.//sample'):
            # Tempo de resposta
            elapsed = int(sample.get('t', 0))
            tempos_resposta.append(elapsed)
            
            # Sucesso/Falha
            success = sample.get('s', 'false').lower() == 'true'
            if success:
                sucessos += 1
            else:
                falhas += 1
            
            # Bytes
            bytes_sent = int(sample.get('by', 0))
            total_bytes += bytes_sent
        
        total_requests = sucessos + falhas
        
        if total_requests == 0:
            return {"erro": "Nenhuma requisição encontrada"}
        
        # Calcular métricas
        tempo_medio = sum(tempos_resposta) / len(tempos_resposta) if tempos_resposta else 0
        tempo_min = min(tempos_resposta) if tempos_resposta else 0
        tempo_max = max(tempos_resposta) if tempos_resposta else 0
        
        # Percentis
        tempos_ordenados = sorted(tempos_resposta)
        percentil_95 = tempos_ordenados[int(len(tempos_ordenados) * 0.95)] if tempos_ordenados else 0
        percentil_99 = tempos_ordenados[int(len(tempos_ordenados) * 0.99)] if tempos_ordenados else 0
        
        # Taxa de erro
        taxa_erro = (falhas / total_requests) * 100
        
        # Disponibilidade
        disponibilidade = (sucessos / total_requests) * 100
        
        return {
            "total_requests": total_requests,
            "sucessos": sucessos,
            "falhas": falhas,
            "taxa_erro": taxa_erro,
            "disponibilidade": disponibilidade,
            "tempo_medio": tempo_medio,
            "tempo_min": tempo_min,
            "tempo_max": tempo_max,
            "percentil_95": percentil_95,
            "percentil_99": percentil_99,
            "total_bytes": total_bytes
        }
        
    except Exception as e:
        return {"erro": f"Erro ao analisar resultados: {e}"}

def gerar_relatorio_resumo(cenario: str, metricas: Dict) -> str:
    """
    Gera relatório resumo das métricas
    
    Args:
        cenario: Nome do cenário
        metricas: Métricas analisadas
    
    Returns:
        String com relatório formatado
    """
    if "erro" in metricas:
        return f"❌ Erro na análise: {metricas['erro']}"
    
    # Determinar status baseado nas métricas
    status_tempo = "✅" if metricas["tempo_medio"] < 500 else "⚠️" if metricas["tempo_medio"] < 1000 else "❌"
    status_erro = "✅" if metricas["taxa_erro"] < 1 else "⚠️" if metricas["taxa_erro"] < 5 else "❌"
    status_disponibilidade = "✅" if metricas["disponibilidade"] > 99.5 else "⚠️" if metricas["disponibilidade"] > 99 else "❌"
    
    relatorio = f"""
{Colors.HEADER}📊 RELATÓRIO DE PERFORMANCE - {cenario.upper()}{Colors.ENDC}
{Colors.OKCYAN}{'='*60}{Colors.ENDC}

{Colors.BOLD}📈 MÉTRICAS PRINCIPAIS{Colors.ENDC}
┌─────────────────────────────────────────────────────┐
│ {Colors.OKBLUE}Total de Requisições:{Colors.ENDC} {metricas['total_requests']:,}
│ {Colors.OKGREEN}Sucessos:{Colors.ENDC} {metricas['sucessos']:,}
│ {Colors.FAIL}Falhas:{Colors.ENDC} {metricas['falhas']:,}
│ {status_erro} {Colors.BOLD}Taxa de Erro:{Colors.ENDC} {metricas['taxa_erro']:.2f}%
│ {status_disponibilidade} {Colors.BOLD}Disponibilidade:{Colors.ENDC} {metricas['disponibilidade']:.2f}%
└─────────────────────────────────────────────────────┘

{Colors.BOLD}⏱️  TEMPO DE RESPOSTA{Colors.ENDC}
┌─────────────────────────────────────────────────────┐
│ {status_tempo} {Colors.BOLD}Tempo Médio:{Colors.ENDC} {metricas['tempo_medio']:.0f}ms
│ {Colors.OKCYAN}Tempo Mínimo:{Colors.ENDC} {metricas['tempo_min']:.0f}ms
│ {Colors.WARNING}Tempo Máximo:{Colors.ENDC} {metricas['tempo_max']:.0f}ms
│ {Colors.OKBLUE}95º Percentil:{Colors.ENDC} {metricas['percentil_95']:.0f}ms
│ {Colors.OKBLUE}99º Percentil:{Colors.ENDC} {metricas['percentil_99']:.0f}ms
└─────────────────────────────────────────────────────┘

{Colors.BOLD}🎯 CRITÉRIOS DE APROVAÇÃO{Colors.ENDC}
┌─────────────────────────────────────────────────────┐
│ Tempo Médio < 500ms:     {status_tempo}
│ Taxa de Erro < 1%:       {status_erro}
│ Disponibilidade > 99.5%: {status_disponibilidade}
└─────────────────────────────────────────────────────┘

{Colors.BOLD}📊 THROUGHPUT{Colors.ENDC}
┌─────────────────────────────────────────────────────┐
│ {Colors.OKCYAN}Total de Bytes:{Colors.ENDC} {metricas['total_bytes']:,}
│ {Colors.OKCYAN}Média por Requisição:{Colors.ENDC} {metricas['total_bytes']/metricas['total_requests']:.0f} bytes
└─────────────────────────────────────────────────────┘
"""
    
    return relatorio

def menu_interativo():
    """Menu interativo para seleção de testes"""
    cenarios_disponiveis = {
        "1": ("load_test", "Teste de Carga Normal (50 usuários, 10 min)"),
        "2": ("stress_test", "Teste de Stress (500 usuários, 20 min)"),
        "3": ("spike_test", "Teste de Picos (Picos súbitos de carga)"),
        "4": ("endurance_test", "Teste de Resistência (2 horas)"),
        "5": ("all", "Executar Todos os Testes"),
        "6": ("custom", "Teste Customizado")
    }
    
    print_colored("\n🎯 MENU DE TESTES DE CARGA", Colors.HEADER)
    print_colored("=" * 40, Colors.OKCYAN)
    
    for key, (cenario, descricao) in cenarios_disponiveis.items():
        print_colored(f"{key}. {descricao}", Colors.OKBLUE)
    
    print_colored("0. Sair", Colors.WARNING)
    print_colored("=" * 40, Colors.OKCYAN)
    
    while True:
        escolha = input(f"\n{Colors.BOLD}Digite sua escolha (0-6): {Colors.ENDC}").strip()
        
        if escolha == "0":
            print_colored("👋 Saindo...", Colors.WARNING)
            sys.exit(0)
        
        if escolha in cenarios_disponiveis:
            cenario, descricao = cenarios_disponiveis[escolha]
            print_colored(f"\n✅ Selecionado: {descricao}", Colors.OKGREEN)
            return cenario
        
        print_colored("❌ Opção inválida! Tente novamente.", Colors.FAIL)

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="🚀 Executor de Testes de Carga - Sistema FetalCare",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python run_load_tests.py --scenario load_test --report
  python run_load_tests.py --scenario stress_test --no-report
  python run_load_tests.py --scenario all --report
  python run_load_tests.py --interactive
        """
    )
    
    parser.add_argument('--scenario', 
                       choices=['load_test', 'stress_test', 'spike_test', 'endurance_test', 'all'],
                       help='Cenário de teste a executar')
    
    parser.add_argument('--report', action='store_true', default=True,
                       help='Gerar relatório HTML (padrão: True)')
    
    parser.add_argument('--no-report', action='store_true',
                       help='Não gerar relatório HTML')
    
    parser.add_argument('--interactive', action='store_true',
                       help='Modo interativo')
    
    parser.add_argument('--analyze-only', type=str,
                       help='Apenas analisar arquivo .jtl existente')
    
    parser.add_argument('--host', default='localhost',
                       help='Host do sistema (padrão: localhost)')
    
    parser.add_argument('--port', default='5001',
                       help='Porta do sistema (padrão: 5001)')
    
    args = parser.parse_args()
    
    # Imprimir banner
    print_banner()
    
    # Modo análise apenas
    if args.analyze_only:
        print_colored(f"📊 Analisando arquivo: {args.analyze_only}", Colors.OKBLUE)
        metricas = analisar_resultados(args.analyze_only)
        relatorio = gerar_relatorio_resumo("análise", metricas)
        print(relatorio)
        return
    
    # Verificações iniciais
    if not verificar_jmeter():
        print_colored("❌ JMeter não encontrado. Instale o Apache JMeter.", Colors.FAIL)
        sys.exit(1)
    
    if not verificar_sistema_ativo():
        print_colored("❌ Sistema FetalCare não está ativo. Inicie o sistema antes de executar os testes.", Colors.FAIL)
        sys.exit(1)
    
    # Determinar cenário
    if args.interactive:
        cenario = menu_interativo()
    elif args.scenario:
        cenario = args.scenario
    else:
        print_colored("❌ Especifique --scenario ou use --interactive", Colors.FAIL)
        sys.exit(1)
    
    # Configurar relatório
    gerar_relatorio = args.report and not args.no_report
    
    # Parâmetros extras
    parametros_extras = {
        'HOST': args.host,
        'PORT': args.port
    }
    
    # Executar testes
    if cenario == "all":
        cenarios = ["load_test", "stress_test", "spike_test"]
        print_colored(f"🚀 Executando {len(cenarios)} cenários de teste", Colors.HEADER)
        
        resultados = []
        for c in cenarios:
            print_colored(f"\n{'='*60}", Colors.OKCYAN)
            sucesso, caminho = executar_teste_jmeter(c, gerar_relatorio, parametros_extras)
            resultados.append((c, sucesso, caminho))
            
            if sucesso and caminho.endswith('.jtl'):
                metricas = analisar_resultados(caminho)
                relatorio = gerar_relatorio_resumo(c, metricas)
                print(relatorio)
        
        # Resumo final
        print_colored(f"\n{'='*60}", Colors.HEADER)
        print_colored("📊 RESUMO FINAL", Colors.BOLD)
        print_colored(f"{'='*60}", Colors.HEADER)
        
        for cenario_nome, sucesso, caminho in resultados:
            status = "✅" if sucesso else "❌"
            print_colored(f"{status} {cenario_nome}: {'SUCESSO' if sucesso else 'FALHA'}", 
                         Colors.OKGREEN if sucesso else Colors.FAIL)
    
    else:
        # Executar cenário único
        sucesso, caminho = executar_teste_jmeter(cenario, gerar_relatorio, parametros_extras)
        
        if sucesso:
            if caminho.endswith('.jtl'):
                metricas = analisar_resultados(caminho)
                relatorio = gerar_relatorio_resumo(cenario, metricas)
                print(relatorio)
            
            print_colored(f"\n🎉 Teste {cenario} concluído com sucesso!", Colors.OKGREEN)
            if gerar_relatorio:
                print_colored(f"📊 Relatório disponível em: {caminho}", Colors.OKCYAN)
        else:
            print_colored(f"\n❌ Teste {cenario} falhou!", Colors.FAIL)
            sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\n⚠️  Teste interrompido pelo usuário", Colors.WARNING)
        sys.exit(1)
    except Exception as e:
        print_colored(f"\n❌ Erro inesperado: {e}", Colors.FAIL)
        sys.exit(1) 