#!/usr/bin/env python3
"""
🎯 Sistema FetalCare - Gerador de Dados de Teste
Gerador de dados sintéticos para testes de carga JMeter

Autor: Sistema de Testes de Performance
Data: 03/07/2025
Versão: 1.0.0
"""

import csv
import random
import json
import os
from pathlib import Path
from faker import Faker
from typing import List, Dict, Any
import numpy as np

# Configurações
BASE_DIR = Path(__file__).parent.parent
DADOS_DIR = BASE_DIR / "dados"
DADOS_DIR.mkdir(parents=True, exist_ok=True)

# Inicializar Faker
fake = Faker('pt_BR')

class FetalCareDataGenerator:
    """Gerador de dados para testes do Sistema FetalCare"""
    
    def __init__(self):
        self.fake = Faker('pt_BR')
        
        # Ranges realistas para parâmetros ML
        self.ml_ranges = {
            'baseline_value': (110, 160),  # BPM
            'accelerations': (0, 10),
            'fetal_movement': (0, 10),
            'uterine_contractions': (0, 10),
            'light_decelerations': (0, 5),
            'severe_decelerations': (0, 3),
            'prolonged_decelerations': (0, 2),
            'abnormal_short_term_variability': (0, 100),
            'mean_value_of_short_term_variability': (0.0, 5.0),
            'percentage_of_time_with_abnormal_long_term_variability': (0, 100),
            'mean_value_of_long_term_variability': (0.0, 20.0),
            'histogram_width': (10, 100),
            'histogram_min': (80, 130),
            'histogram_max': (140, 180),
            'histogram_number_of_peaks': (1, 10),
            'histogram_number_of_zeroes': (0, 20),
            'histogram_mode': (100, 160),
            'histogram_mean': (100, 160),
            'histogram_median': (100, 160),
            'histogram_variance': (0, 100),
            'histogram_tendency': (-1, 1)
        }
    
    def gerar_cpf_valido(self) -> str:
        """Gera CPF válido"""
        return self.fake.cpf()
    
    def gerar_gestante(self) -> Dict[str, Any]:
        """Gera dados de uma gestante"""
        return {
            'patient_id': f'TEST{random.randint(1000, 9999)}',
            'patient_name': self.fake.name(),
            'patient_cpf': self.gerar_cpf_valido(),
            'gestational_age': random.randint(20, 40),
            'medical_history': f'Histórico médico {random.randint(1, 100)}',
            'current_medications': f'Medicação {random.randint(1, 10)}',
            'allergies': f'Alergia {random.randint(1, 5)}' if random.random() < 0.3 else 'Nenhuma',
            'emergency_contact': self.fake.phone_number()
        }
    
    def gerar_parametros_ml_normal(self) -> Dict[str, Any]:
        """Gera parâmetros ML para caso normal"""
        return {
            'baseline_value': random.randint(130, 150),
            'accelerations': random.randint(2, 5),
            'fetal_movement': random.randint(1, 4),
            'uterine_contractions': random.randint(0, 2),
            'light_decelerations': random.randint(0, 1),
            'severe_decelerations': 0,
            'prolonged_decelerations': 0,
            'abnormal_short_term_variability': random.randint(10, 25),
            'mean_value_of_short_term_variability': round(random.uniform(0.3, 1.0), 2),
            'percentage_of_time_with_abnormal_long_term_variability': random.randint(5, 20),
            'mean_value_of_long_term_variability': round(random.uniform(6.0, 12.0), 2),
            'histogram_width': random.randint(50, 80),
            'histogram_min': random.randint(110, 125),
            'histogram_max': random.randint(150, 170),
            'histogram_number_of_peaks': random.randint(1, 3),
            'histogram_number_of_zeroes': random.randint(0, 2),
            'histogram_mode': random.randint(130, 150),
            'histogram_mean': random.randint(135, 145),
            'histogram_median': random.randint(135, 145),
            'histogram_variance': random.randint(10, 25),
            'histogram_tendency': random.choice([0, 1])
        }
    
    def gerar_parametros_ml_suspeito(self) -> Dict[str, Any]:
        """Gera parâmetros ML para caso suspeito"""
        return {
            'baseline_value': random.randint(110, 130),
            'accelerations': random.randint(0, 2),
            'fetal_movement': random.randint(0, 2),
            'uterine_contractions': random.randint(2, 4),
            'light_decelerations': random.randint(1, 3),
            'severe_decelerations': random.randint(0, 1),
            'prolonged_decelerations': random.randint(0, 1),
            'abnormal_short_term_variability': random.randint(25, 45),
            'mean_value_of_short_term_variability': round(random.uniform(1.0, 2.0), 2),
            'percentage_of_time_with_abnormal_long_term_variability': random.randint(20, 50),
            'mean_value_of_long_term_variability': round(random.uniform(3.0, 8.0), 2),
            'histogram_width': random.randint(30, 60),
            'histogram_min': random.randint(90, 115),
            'histogram_max': random.randint(130, 150),
            'histogram_number_of_peaks': random.randint(1, 2),
            'histogram_number_of_zeroes': random.randint(2, 8),
            'histogram_mode': random.randint(110, 130),
            'histogram_mean': random.randint(115, 125),
            'histogram_median': random.randint(115, 125),
            'histogram_variance': random.randint(25, 45),
            'histogram_tendency': random.choice([-1, 0])
        }
    
    def gerar_parametros_ml_critico(self) -> Dict[str, Any]:
        """Gera parâmetros ML para caso crítico"""
        return {
            'baseline_value': random.randint(90, 115),
            'accelerations': random.randint(0, 1),
            'fetal_movement': random.randint(0, 1),
            'uterine_contractions': random.randint(4, 8),
            'light_decelerations': random.randint(2, 5),
            'severe_decelerations': random.randint(1, 3),
            'prolonged_decelerations': random.randint(1, 2),
            'abnormal_short_term_variability': random.randint(45, 80),
            'mean_value_of_short_term_variability': round(random.uniform(2.0, 4.0), 2),
            'percentage_of_time_with_abnormal_long_term_variability': random.randint(50, 90),
            'mean_value_of_long_term_variability': round(random.uniform(1.0, 5.0), 2),
            'histogram_width': random.randint(15, 40),
            'histogram_min': random.randint(70, 100),
            'histogram_max': random.randint(110, 130),
            'histogram_number_of_peaks': random.randint(1, 2),
            'histogram_number_of_zeroes': random.randint(5, 15),
            'histogram_mode': random.randint(90, 110),
            'histogram_mean': random.randint(85, 105),
            'histogram_median': random.randint(85, 105),
            'histogram_variance': random.randint(40, 80),
            'histogram_tendency': -1
        }
    
    def gerar_parametros_ml_aleatorio(self) -> Dict[str, Any]:
        """Gera parâmetros ML aleatórios dentro dos ranges"""
        params = {}
        for param, (min_val, max_val) in self.ml_ranges.items():
            if isinstance(min_val, float):
                params[param] = round(random.uniform(min_val, max_val), 2)
            else:
                params[param] = random.randint(min_val, max_val)
        return params
    
    def gerar_csv_gestantes(self, quantidade: int = 1000, arquivo: str = 'gestantes.csv') -> str:
        """
        Gera arquivo CSV com dados de gestantes
        
        Args:
            quantidade: Número de gestantes a gerar
            arquivo: Nome do arquivo CSV
        
        Returns:
            Caminho do arquivo gerado
        """
        caminho = DADOS_DIR / arquivo
        
        with open(caminho, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Cabeçalho
            writer.writerow([
                'patient_id', 'patient_name', 'patient_cpf', 'gestational_age',
                'medical_history', 'current_medications', 'allergies', 'emergency_contact'
            ])
            
            # Dados
            for i in range(quantidade):
                gestante = self.gerar_gestante()
                writer.writerow([
                    gestante['patient_id'],
                    gestante['patient_name'],
                    gestante['patient_cpf'],
                    gestante['gestational_age'],
                    gestante['medical_history'],
                    gestante['current_medications'],
                    gestante['allergies'],
                    gestante['emergency_contact']
                ])
        
        print(f"✅ Gerado arquivo: {caminho} ({quantidade} gestantes)")
        return str(caminho)
    
    def gerar_csv_parametros_ml(self, quantidade: int = 5000, arquivo: str = 'parametros_ml.csv') -> str:
        """
        Gera arquivo CSV com parâmetros ML
        
        Args:
            quantidade: Número de conjuntos de parâmetros
            arquivo: Nome do arquivo CSV
        
        Returns:
            Caminho do arquivo gerado
        """
        caminho = DADOS_DIR / arquivo
        
        # Cabeçalho com todas as features ML
        features = list(self.ml_ranges.keys())
        
        with open(caminho, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Cabeçalho
            writer.writerow(features)
            
            # Gerar dados com distribuição realista
            for i in range(quantidade):
                # 60% normais, 25% suspeitos, 15% críticos
                rand = random.random()
                if rand < 0.6:
                    params = self.gerar_parametros_ml_normal()
                elif rand < 0.85:
                    params = self.gerar_parametros_ml_suspeito()
                else:
                    params = self.gerar_parametros_ml_critico()
                
                # Escrever linha
                writer.writerow([params[feature] for feature in features])
        
        print(f"✅ Gerado arquivo: {caminho} ({quantidade} conjuntos de parâmetros ML)")
        return str(caminho)
    
    def gerar_csv_usuarios(self, quantidade: int = 100, arquivo: str = 'usuarios.csv') -> str:
        """
        Gera arquivo CSV com dados de usuários do sistema
        
        Args:
            quantidade: Número de usuários
            arquivo: Nome do arquivo CSV
        
        Returns:
            Caminho do arquivo gerado
        """
        caminho = DADOS_DIR / arquivo
        
        with open(caminho, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Cabeçalho
            writer.writerow(['user_id', 'username', 'email', 'role', 'department'])
            
            # Dados
            roles = ['doctor', 'nurse', 'admin', 'technician']
            departments = ['obstetrics', 'neonatology', 'emergency', 'icu']
            
            for i in range(quantidade):
                writer.writerow([
                    f'USER{i:04d}',
                    self.fake.user_name(),
                    self.fake.email(),
                    random.choice(roles),
                    random.choice(departments)
                ])
        
        print(f"✅ Gerado arquivo: {caminho} ({quantidade} usuários)")
        return str(caminho)
    
    def gerar_json_cenarios_teste(self, arquivo: str = 'cenarios_teste.json') -> str:
        """
        Gera arquivo JSON com cenários de teste pré-definidos
        
        Args:
            arquivo: Nome do arquivo JSON
        
        Returns:
            Caminho do arquivo gerado
        """
        caminho = DADOS_DIR / arquivo
        
        cenarios = {
            'normal_cases': [self.gerar_parametros_ml_normal() for _ in range(10)],
            'suspicious_cases': [self.gerar_parametros_ml_suspeito() for _ in range(10)],
            'critical_cases': [self.gerar_parametros_ml_critico() for _ in range(10)],
            'edge_cases': [
                # Valores extremos
                {**self.gerar_parametros_ml_normal(), 'baseline_value': 180},
                {**self.gerar_parametros_ml_normal(), 'baseline_value': 80},
                {**self.gerar_parametros_ml_critico(), 'severe_decelerations': 5},
                {**self.gerar_parametros_ml_critico(), 'prolonged_decelerations': 3},
            ]
        }
        
        with open(caminho, 'w', encoding='utf-8') as file:
            json.dump(cenarios, file, indent=2, ensure_ascii=False)
        
        print(f"✅ Gerado arquivo: {caminho} (cenários de teste)")
        return str(caminho)
    
    def gerar_todos_os_arquivos(self):
        """Gera todos os arquivos de dados de teste"""
        print("🎯 Gerando dados de teste para Sistema FetalCare...")
        print("=" * 50)
        
        # Gerar arquivos
        self.gerar_csv_gestantes(1000)
        self.gerar_csv_parametros_ml(5000)
        self.gerar_csv_usuarios(100)
        self.gerar_json_cenarios_teste()
        
        print("=" * 50)
        print("✅ Todos os arquivos de dados de teste foram gerados!")
        print(f"📁 Localização: {DADOS_DIR}")
        
        # Listar arquivos gerados
        print("\n📋 Arquivos gerados:")
        for arquivo in DADOS_DIR.glob('*'):
            if arquivo.is_file():
                tamanho = arquivo.stat().st_size
                print(f"  📄 {arquivo.name} ({tamanho:,} bytes)")

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="🎯 Gerador de Dados de Teste - Sistema FetalCare")
    parser.add_argument('--gestantes', type=int, default=1000,
                       help='Número de gestantes a gerar (padrão: 1000)')
    parser.add_argument('--parametros-ml', type=int, default=5000,
                       help='Número de conjuntos de parâmetros ML (padrão: 5000)')
    parser.add_argument('--usuarios', type=int, default=100,
                       help='Número de usuários a gerar (padrão: 100)')
    parser.add_argument('--all', action='store_true',
                       help='Gerar todos os arquivos com quantidades padrão')
    
    args = parser.parse_args()
    
    generator = FetalCareDataGenerator()
    
    if args.all:
        generator.gerar_todos_os_arquivos()
    else:
        print("🎯 Gerando dados de teste personalizados...")
        print("=" * 50)
        
        if args.gestantes:
            generator.gerar_csv_gestantes(args.gestantes)
        
        if args.parametros_ml:
            generator.gerar_csv_parametros_ml(args.parametros_ml)
        
        if args.usuarios:
            generator.gerar_csv_usuarios(args.usuarios)
        
        generator.gerar_json_cenarios_teste()
        
        print("=" * 50)
        print("✅ Dados de teste gerados com sucesso!")

if __name__ == "__main__":
    main() 