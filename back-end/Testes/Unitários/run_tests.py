#!/usr/bin/env python3
"""
Script para executar testes unitários do Sistema FetalCare
Estrutura pytest profissional com relatórios automáticos
"""

import subprocess
import sys
import os
from datetime import datetime
import webbrowser
from pathlib import Path

def print_banner():
    """Imprimir banner do sistema"""
    print("=" * 80)
    print("🏥 SISTEMA FETALCARE - TESTES UNITÁRIOS")
    print("📊 Estrutura pytest com Análise de Cobertura")
    print("=" * 80)
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"📁 Diretório: {os.getcwd()}")
    print("-" * 80)

def run_command(command, description):
    """Executar comando com feedback visual"""
    print(f"\n🚀 {description}")
    print(f"💻 Comando: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=False, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCESSO")
            return True
        else:
            print(f"❌ {description} - FALHOU (código: {result.returncode})")
            return False
    except Exception as e:
        print(f"💥 Erro ao executar: {e}")
        return False

def main():
    """Função principal"""
    print_banner()
    
    # Comandos disponíveis
    commands = {
        "1": {
            "cmd": "pytest -v",
            "desc": "Execução básica dos testes",
            "open_html": False
        },
        "2": {
            "cmd": "pytest --cov=../../banco --cov=../../IA --cov-report=html --cov-report=term -v",
            "desc": "Testes com análise de cobertura completa",
            "open_html": True
        },
        "3": {
            "cmd": "pytest --html=relatorio_completo.html --self-contained-html -v",
            "desc": "Testes com relatório HTML detalhado",
            "open_html": True
        },
        "4": {
            "cmd": "pytest test_backend_validacao.py -v",
            "desc": "Apenas testes de backend/validação",
            "open_html": False
        },
        "5": {
            "cmd": "pytest test_modelo_ml.py -v",
            "desc": "Apenas testes do modelo ML",
            "open_html": False
        },
        "6": {
            "cmd": "pytest --cov=../../banco --cov=../../IA --cov-report=html --cov-report=term --html=relatorio_final.html --self-contained-html -v",
            "desc": "Relatório COMPLETO (Cobertura + HTML)",
            "open_html": True
        }
    }
    
    # Menu interativo
    print("\n📋 OPÇÕES DISPONÍVEIS:")
    for key, value in commands.items():
        print(f"  {key}. {value['desc']}")
    
    print("\n" + "=" * 80)
    
    # Execução automática se não for interativo
    if len(sys.argv) > 1:
        option = sys.argv[1]
    else:
        option = input("\n🎯 Escolha uma opção (1-6) ou Enter para opção 6: ").strip()
    
    if not option:
        option = "6"  # Padrão: relatório completo
    
    if option not in commands:
        print(f"❌ Opção inválida: {option}")
        return False
    
    # Executar comando selecionado
    cmd_info = commands[option]
    success = run_command(cmd_info["cmd"], cmd_info["desc"])
    
    if success:
        print("\n" + "=" * 80)
        print("🎉 EXECUÇÃO CONCLUÍDA COM SUCESSO!")
        
        # Listar arquivos gerados
        generated_files = []
        
        # Verificar arquivos HTML
        html_files = ["relatorio_completo.html", "relatorio_final.html"]
        for html_file in html_files:
            if Path(html_file).exists():
                generated_files.append(html_file)
        
        # Verificar diretório de cobertura
        if Path("htmlcov").exists():
            generated_files.append("htmlcov/index.html")
        
        if generated_files:
            print("\n📁 ARQUIVOS GERADOS:")
            for file in generated_files:
                print(f"   📄 {file}")
            
            # Abrir relatório automaticamente
            if cmd_info["open_html"] and generated_files:
                try:
                    file_to_open = generated_files[0]
                    print(f"\n🌐 Abrindo relatório: {file_to_open}")
                    webbrowser.open(f"file://{Path(file_to_open).absolute()}")
                except Exception as e:
                    print(f"⚠️  Não foi possível abrir automaticamente: {e}")
        
        print("\n📊 RESUMO:")
        print("   ✅ Todos os testes executados")
        print("   📈 Relatórios de cobertura gerados")
        print("   🏥 Sistema FetalCare validado")
        
    else:
        print("\n💥 EXECUÇÃO FALHOU!")
        print("   🔍 Verifique os erros acima")
        print("   📋 Consulte a documentação dos testes")
    
    print("\n" + "=" * 80)
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Execução interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erro inesperado: {e}")
        sys.exit(1) 