#!/usr/bin/env python3
"""
Script de teste para a API FetalCare
Testa todas as funcionalidades da API
"""

import asyncio
import httpx
import json
from datetime import datetime
from typing import Dict, Any

# Configurações
API_BASE_URL = "http://localhost:8000"
ML_API_URL = "http://localhost:5000"

class FetalCareAPITester:
    """Testador da API FetalCare"""
    
    def __init__(self):
        self.base_url = API_BASE_URL
        self.session = None
        self.registro_id = None
    
    async def __aenter__(self):
        self.session = httpx.AsyncClient(timeout=30.0)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.aclose()
    
    def print_resultado(self, titulo: str, resultado: Dict[str, Any], status_code: int = 200):
        """Imprime resultado formatado"""
        print(f"\n{'='*50}")
        print(f"🧪 {titulo}")
        print(f"{'='*50}")
        print(f"Status Code: {status_code}")
        print(f"Resultado: {json.dumps(resultado, indent=2, ensure_ascii=False)}")
    
    async def testar_health_check(self):
        """Testa health check da API"""
        try:
            response = await self.session.get(f"{self.base_url}/")
            self.print_resultado("Health Check", response.json(), response.status_code)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Erro no health check: {e}")
            return False
    
    async def testar_criacao_registro(self):
        """Testa criação de registro de exame"""
        try:
            dados_teste = {
                "dados_gestante": {
                    "patient_id": "G2024001",
                    "patient_name": "Maria Silva Santos",
                    "patient_cpf": "123.456.789-00",
                    "gestational_age": 28,
                    "patient_age": 25,
                    "patient_phone": "(11) 99999-9999",
                    "responsible_doctor": "Dr. João Oliveira"
                },
                "parametros_monitoramento": {
                    "baseline_value": 140.0,
                    "accelerations": 3,
                    "fetal_movement": 4,
                    "uterine_contractions": 0,
                    "light_decelerations": 0,
                    "severe_decelerations": 0,
                    "prolongued_decelerations": 0,
                    "abnormal_short_term_variability": 0,
                    "mean_value_of_short_term_variability": 5.5,
                    "percentage_of_time_with_abnormal_long_term_variability": 10,
                    "mean_value_of_long_term_variability": 25.0,
                    "histogram_width": 120,
                    "histogram_min": 90,
                    "histogram_max": 180,
                    "histogram_number_of_peaks": 3,
                    "histogram_number_of_zeroes": 0,
                    "histogram_mode": 140,
                    "histogram_mean": 140,
                    "histogram_median": 140,
                    "histogram_variance": 15,
                    "histogram_tendency": "normal"
                },
                "medico_responsavel": "Dr. João Oliveira",
                "observacoes": "Exame de rotina - paciente sem queixas"
            }
            
            response = await self.session.post(
                f"{self.base_url}/registros",
                json=dados_teste
            )
            
            resultado = response.json()
            self.print_resultado("Criação de Registro", resultado, response.status_code)
            
            if response.status_code == 200:
                self.registro_id = resultado.get("id")
                print(f"✅ Registro criado com ID: {self.registro_id}")
                print(f"📊 Status saúde: {resultado.get('saude_feto', {}).get('status_saude')}")
                return True
            return False
            
        except Exception as e:
            print(f"❌ Erro na criação de registro: {e}")
            return False
    
    async def testar_listagem_registros(self):
        """Testa listagem de registros"""
        try:
            # Teste 1: Listar todos
            response = await self.session.get(f"{self.base_url}/registros")
            resultado = response.json()
            self.print_resultado("Listagem - Todos os Registros", resultado, response.status_code)
            
            # Teste 2: Filtrar por CPF
            response = await self.session.get(f"{self.base_url}/registros?cpf=123.456.789-00")
            resultado = response.json()
            self.print_resultado("Listagem - Por CPF", resultado, response.status_code)
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ Erro na listagem: {e}")
            return False
    
    async def testar_obter_registro(self):
        """Testa obtenção de registro específico"""
        if not self.registro_id:
            print("⚠️  Registro ID não disponível para teste")
            return False
        
        try:
            response = await self.session.get(f"{self.base_url}/registros/{self.registro_id}")
            resultado = response.json()
            self.print_resultado("Obter Registro Específico", resultado, response.status_code)
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ Erro ao obter registro: {e}")
            return False
    
    async def testar_estatisticas(self):
        """Testa endpoint de estatísticas"""
        try:
            response = await self.session.get(f"{self.base_url}/estatisticas")
            resultado = response.json()
            self.print_resultado("Estatísticas", resultado, response.status_code)
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ Erro nas estatísticas: {e}")
            return False
    
    async def testar_ml_endpoints(self):
        """Testa endpoints relacionados ao ML"""
        try:
            # Info do modelo
            response = await self.session.get(f"{self.base_url}/ml/info")
            resultado = response.json()
            self.print_resultado("ML - Info do Modelo", resultado, response.status_code)
            
            # Cenários de teste
            response = await self.session.get(f"{self.base_url}/ml/cenarios")
            resultado = response.json()
            self.print_resultado("ML - Cenários de Teste", resultado, response.status_code)
            
            # Health check do ML
            response = await self.session.get(f"{self.base_url}/ml/health")
            resultado = response.json()
            self.print_resultado("ML - Health Check", resultado, response.status_code)
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ Erro nos endpoints ML: {e}")
            return False
    
    async def executar_todos_testes(self):
        """Executa todos os testes"""
        print("🚀 INICIANDO TESTES DA API FETALCARE")
        print(f"🔗 Base URL: {self.base_url}")
        print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        testes = [
            ("Health Check", self.testar_health_check),
            ("Criação de Registro", self.testar_criacao_registro),
            ("Listagem de Registros", self.testar_listagem_registros),
            ("Obter Registro Específico", self.testar_obter_registro),
            ("Estatísticas", self.testar_estatisticas),
            ("Endpoints ML", self.testar_ml_endpoints),
        ]
        
        resultados = []
        
        for nome, teste in testes:
            print(f"\n🧪 Executando: {nome}")
            try:
                sucesso = await teste()
                resultados.append((nome, sucesso))
                status = "✅ PASSOU" if sucesso else "❌ FALHOU"
                print(f"   {status}")
            except Exception as e:
                print(f"   ❌ ERRO: {e}")
                resultados.append((nome, False))
        
        # Resumo final
        print(f"\n{'='*60}")
        print("📊 RESUMO DOS TESTES")
        print(f"{'='*60}")
        
        total_testes = len(resultados)
        testes_passou = sum(1 for _, sucesso in resultados if sucesso)
        
        for nome, sucesso in resultados:
            status = "✅ PASSOU" if sucesso else "❌ FALHOU"
            print(f"   {nome}: {status}")
        
        print(f"\n🎯 RESULTADO FINAL: {testes_passou}/{total_testes} testes passaram")
        
        if testes_passou == total_testes:
            print("🎉 TODOS OS TESTES PASSARAM!")
        else:
            print("⚠️  ALGUNS TESTES FALHARAM")
        
        return testes_passou == total_testes

async def main():
    """Função principal"""
    async with FetalCareAPITester() as tester:
        await tester.executar_todos_testes()

if __name__ == "__main__":
    asyncio.run(main()) 