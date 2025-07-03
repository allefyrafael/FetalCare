"""
Configuração pytest para Sistema FetalCare
Fixtures compartilhadas e configurações globais
"""

import pytest
import sys
import os
import warnings
import joblib
import numpy as np
from datetime import datetime

# Adicionar path do projeto
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

@pytest.fixture(scope="session")
def suppress_warnings():
    """Suprimir warnings do sklearn durante os testes"""
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        warnings.filterwarnings("ignore", category=FutureWarning)
        yield

@pytest.fixture(scope="session")
def ml_model():
    """Carregar modelo ML uma vez por sessão"""
    model_path = os.path.join('../../IA', 'model.sav')
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        model = joblib.load(model_path)
    return model

@pytest.fixture
def dados_gestante_validos():
    """Dados válidos de gestante para testes"""
    return {
        'patient_id': 'TEST001',
        'patient_name': 'Maria Silva',
        'patient_cpf': '12345678901',
        'gestational_age': 28,
        'patient_age': 25
    }

@pytest.fixture
def parametros_monitoramento_validos():
    """Parâmetros válidos de monitoramento fetal"""
    return {
        'baseline_value': 140.0,
        'accelerations': 3,
        'fetal_movement': 2,
        'uterine_contractions': 1,
        'light_decelerations': 0,
        'severe_decelerations': 0,
        'prolongued_decelerations': 0,
        'abnormal_short_term_variability': 20,
        'mean_value_of_short_term_variability': 1.5,
        'percentage_of_time_with_abnormal_long_term_variability': 10,
        'mean_value_of_long_term_variability': 8.5,
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
def features_ml_normais():
    """Features ML para caso normal"""
    return [
        140.0, 3, 2, 1, 0, 0, 0, 20, 1.5, 10,
        8.5, 150, 110, 160, 3, 0, 140, 142, 141, 25, 0
    ]

@pytest.fixture
def features_ml_criticas():
    """Features ML para caso crítico"""
    return [
        80.0, 0, 0, 5, 3, 2, 1, 50, 0.5, 30,
        15.0, 50, 60, 200, 1, 5, 90, 85, 88, 80, -1
    ]

@pytest.fixture(autouse=True)
def test_timing(request):
    """Medir tempo de execução de cada teste"""
    start_time = datetime.now()
    yield
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"\n⏱️  Teste {request.node.name}: {duration:.4f}s") 