#!/usr/bin/env python3
"""
Script automático para configurar e testar o banco de dados do FetalCare
"""

import subprocess
import time
import requests
import json
from datetime import datetime

def run_command(command, shell=True, check=True):
    """Executa um comando e retorna o resultado"""
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True, check=check)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def check_docker():
    """Verifica se o Docker está disponível"""
    success, stdout, stderr = run_command("docker --version", check=False)
    return success

def setup_mongodb():
    """Configura o MongoDB via Docker"""
    print("🐳 Configurando MongoDB via Docker...")
    
    # Verificar se já existe
    success, stdout, stderr = run_command("docker ps -a | grep fetalcare-mongo", check=False)
    if success and "fetalcare-mongo" in stdout:
        print("📦 Container MongoDB já existe")
        
        # Verificar se está rodando
        success, stdout, stderr = run_command("docker ps | grep fetalcare-mongo", check=False)
        if success and "fetalcare-mongo" in stdout:
            print("✅ MongoDB já está rodando")
            return True
        else:
            print("🔄 Iniciando container MongoDB existente...")
            success, stdout, stderr = run_command("docker start fetalcare-mongo", check=False)
            if success:
                print("✅ MongoDB iniciado com sucesso")
                time.sleep(5)
                return True
            else:
                print("❌ Erro ao iniciar MongoDB")
                return False
    else:
        # Criar novo container
        print("🆕 Criando novo container MongoDB...")
        success, stdout, stderr = run_command(
            "docker run -d --name fetalcare-mongo -p 27017:27017 mongo:latest",
            check=False
        )
        if success:
            print("✅ MongoDB criado e iniciado com sucesso")
            time.sleep(8)  # Aguarda inicialização
            return True
        else:
            print(f"❌ Erro ao criar MongoDB: {stderr}")
            return False

def test_mongodb():
    """Testa a conexão com MongoDB"""
    print("🧪 Testando conexão com MongoDB...")
    
    try:
        from pymongo import MongoClient
        client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        
        # Verificar versão
        version = client.server_info()['version']
        print(f"✅ MongoDB conectado - Versão: {version}")
        
        # Verificar banco e collection
        db = client['fetalcare_db']
        collection = db['registros_exames']
        count = collection.count_documents({})
        print(f"📊 Registros existentes: {count}")
        
        client.close()
        return True
    except Exception as e:
        print(f"❌ Erro ao conectar MongoDB: {e}")
        return False

def start_api_with_database():
    """Inicia a API com banco de dados"""
    print("🚀 Iniciando API com banco de dados...")
    
    try:
        # Verificar se já está rodando
        try:
            response = requests.get("http://localhost:5001/", timeout=2)
            if response.status_code == 200:
                print("✅ API com banco já está rodando")
                return True
        except:
            pass
        
        # Iniciar API
        import subprocess
        import os
        
        # Mudar para diretório back-end
        os.chdir("back-end")
        
        # Iniciar em background
        process = subprocess.Popen(
            ["python", "app_with_database.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Aguardar inicialização
        print("⏳ Aguardando API inicializar...")
        time.sleep(8)
        
        # Verificar se está rodando
        try:
            response = requests.get("http://localhost:5001/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API Status: {data.get('status')}")
                print(f"📊 Modelo: {data.get('model_loaded')}")
                print(f"🗄️  Database: {data.get('database_status')}")
                
                # Voltar ao diretório original
                os.chdir("..")
                return True
            else:
                print(f"❌ API não respondeu corretamente: {response.status_code}")
                os.chdir("..")
                return False
        except Exception as e:
            print(f"❌ Erro ao verificar API: {e}")
            os.chdir("..")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao iniciar API: {e}")
        return False

def test_database_saving():
    """Testa se os dados estão sendo salvos no banco"""
    print("🧪 Testando salvamento no banco de dados...")
    
    # Dados de teste
    test_data = {
        "patient_name": "Teste Automático Setup",
        "patient_id": "SETUP_AUTO_001",
        "patient_cpf": "11111111111",
        "gestational_age": 30,
        "patient_age": 25,
        "baseline_value": 135.0,
        "accelerations": 2,
        "fetal_movement": 1,
        "uterine_contractions": 0,
        "light_decelerations": 0,
        "severe_decelerations": 0,
        "prolongued_decelerations": 0,
        "abnormal_short_term_variability": 0,
        "mean_value_of_short_term_variability": 40.0,
        "percentage_of_time_with_abnormal_long_term_variability": 5,
        "mean_value_of_long_term_variability": 80.0,
        "histogram_width": 110,
        "histogram_min": 45,
        "histogram_max": 165,
        "histogram_number_of_peaks": 1,
        "histogram_number_of_zeroes": 0,
        "histogram_mode": 135,
        "histogram_mean": 130,
        "histogram_median": 133,
        "histogram_variance": 140,
        "histogram_tendency": "normal"
    }
    
    try:
        # Contar registros antes
        from pymongo import MongoClient
        client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=3000)
        db = client['fetalcare_db']
        collection = db['registros_exames']
        count_before = collection.count_documents({})
        
        # Fazer predição
        response = requests.post("http://localhost:5001/predict", json=test_data, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Predição realizada!")
            print(f"📊 Status: {result.get('status')}")
            print(f"📊 Confidence: {result.get('confidence')}%")
            print(f"💾 Salvo no banco: {result.get('saved_to_database')}")
            
            # Verificar se foi salvo
            time.sleep(2)
            count_after = collection.count_documents({})
            
            if count_after > count_before:
                print("✅ DADOS SALVOS COM SUCESSO NO BANCO!")
                
                # Mostrar último registro
                latest = collection.find_one(sort=[("data_exame", -1)])
                if latest:
                    print(f"🆔 ID: {latest.get('_id')}")
                    print(f"👤 Paciente: {latest.get('dados_gestante', {}).get('patient_name')}")
                    print(f"🏥 Status: {latest.get('saude_feto', {}).get('status_saude')}")
                
                client.close()
                return True
            else:
                print("❌ Dados não foram salvos no banco")
                client.close()
                return False
        else:
            print(f"❌ Erro na predição: {response.status_code}")
            client.close()
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def show_final_instructions():
    """Mostra instruções finais"""
    print("\n" + "="*60)
    print("🎉 CONFIGURAÇÃO COMPLETA!")
    print("="*60)
    print()
    print("✅ MongoDB instalado e rodando")
    print("✅ API com banco funcionando (porta 5001)")
    print("✅ Dados sendo salvos automaticamente")
    print()
    print("🌐 COMO USAR:")
    print("1. Frontend: http://localhost:8080")
    print("2. Configure API URL para: http://localhost:5001")
    print("3. Faça predições normalmente")
    print()
    print("🔍 VERIFICAR DADOS SALVOS:")
    print("• Via API: http://localhost:5001/records")
    print("• Via MongoDB: docker exec -it fetalcare-mongo mongosh")
    print("• Via teste: python test_api_with_db.py")
    print()
    print("📊 ENDPOINTS DISPONÍVEIS:")
    print("• GET  /records - Buscar registros")
    print("• GET  /records/stats - Estatísticas")
    print("• POST /predict - Fazer predição (salva automaticamente)")
    print()
    print("🆘 TROUBLESHOOTING:")
    print("• Verificar MongoDB: docker ps | grep mongo")
    print("• Verificar API: netstat -an | findstr :5001")
    print("• Logs: docker logs fetalcare-mongo")
    print()
    print("🏁 SETUP CONCLUÍDO COM SUCESSO!")

def main():
    """Função principal"""
    print("🔧 SETUP AUTOMÁTICO - BANCO DE DADOS FETALCARE")
    print("="*60)
    print("Este script configura automaticamente o MongoDB e a API")
    print()
    
    # Verificar Docker
    if not check_docker():
        print("❌ Docker não está disponível")
        print("💡 Instale o Docker primeiro: https://docker.com")
        return False
    
    print("✅ Docker disponível")
    
    # Configurar MongoDB
    if not setup_mongodb():
        print("❌ Falha ao configurar MongoDB")
        return False
    
    # Testar MongoDB
    if not test_mongodb():
        print("❌ Falha ao conectar MongoDB")
        return False
    
    # Iniciar API com banco
    if not start_api_with_database():
        print("❌ Falha ao iniciar API com banco")
        return False
    
    # Testar salvamento
    if not test_database_saving():
        print("❌ Falha no teste de salvamento")
        return False
    
    # Mostrar instruções finais
    show_final_instructions()
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ SETUP FALHOU")
        print("💡 Execute: python test_database_simple.py para diagnóstico")
    else:
        print("\n✅ SETUP CONCLUÍDO COM SUCESSO!") 