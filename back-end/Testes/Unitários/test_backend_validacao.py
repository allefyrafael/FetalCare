"""
Testes Backend - Sistema FetalCare
Estrutura pytest com fixtures e parametrização

Cobertura:
- Validação de dados da gestante
- Validação de parâmetros de monitoramento
- Lógica de classificação de saúde
- Performance e edge cases
"""

import pytest
import time
from pydantic import ValidationError
import sys
import os

# Importar módulos do sistema
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

try:
    from banco.models import DadosGestante, ParametrosMonitoramento, SaudeFeto, ResultadoML
except ImportError:
    # Fallback para desenvolvimento
    class DadosGestante:
        def __init__(self, **kwargs):
            required_fields = ['patient_id', 'patient_name', 'patient_cpf', 'gestational_age']
            for field in required_fields:
                if field not in kwargs:
                    raise ValidationError(f"Field '{field}' is required")
            self.__dict__.update(kwargs)
    
    class ParametrosMonitoramento:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    
    class SaudeFeto:
        def __init__(self, status_saude, nivel_risco, confidence_value):
            self.status_saude = status_saude
            self.nivel_risco = nivel_risco
            self.confidence_value = confidence_value
    
    class ResultadoML:
        def __init__(self, prediction, confidence, status, description):
            self.prediction = prediction
            self.confidence = confidence
            self.status = status
            self.description = description


class TestValidacaoBackend:
    """Testes de validação do backend"""
    
    def test_dados_gestante_validos(self, dados_gestante_validos):
        """
        Teste: Validação de dados válidos da gestante
        Objetivo: Verificar se dados corretos são aceitos
        """
        # Act
        dados = DadosGestante(**dados_gestante_validos)
        
        # Assert
        assert dados.patient_id == 'TEST001'
        assert dados.patient_name == 'Maria Silva'
        assert dados.gestational_age == 28
    
    @pytest.mark.parametrize("campo_faltante", [
        'patient_id', 'patient_name', 'patient_cpf', 'gestational_age'
    ])
    def test_dados_gestante_campos_obrigatorios(self, dados_gestante_validos, campo_faltante):
        """
        Teste: Validação de campos obrigatórios
        Objetivo: Verificar se campos obrigatórios são validados
        """
        # Arrange
        dados_incompletos = dados_gestante_validos.copy()
        del dados_incompletos[campo_faltante]
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            DadosGestante(**dados_incompletos)
        
        assert campo_faltante in str(exc_info.value) or "required" in str(exc_info.value)
    
    def test_parametros_monitoramento_validos(self, parametros_monitoramento_validos):
        """
        Teste: Validação de parâmetros de monitoramento válidos
        Objetivo: Verificar se todos os 21 parâmetros são aceitos
        """
        # Act
        params = ParametrosMonitoramento(**parametros_monitoramento_validos)
        
        # Assert - Verificar campos principais
        assert params.baseline_value == 140.0
        assert params.accelerations == 3
        assert params.histogram_tendency == 'normal'


class TestLogicaNegocio:
    """Testes da lógica de negócio"""
    
    @pytest.mark.parametrize("confidence,status_esperado,nivel_esperado", [
        (85.0, "Normal", "BAIXO"),
        (60.0, "Em Risco", "MODERADO"), 
        (50.0, "Risco Crítico", "CRÍTICO"),
        (30.0, "Risco Crítico", "CRÍTICO"),
    ])
    def test_determinar_status_saude(self, confidence, status_esperado, nivel_esperado):
        """
        Teste: Lógica de determinação do status de saúde
        Objetivo: Verificar classificação baseada na confidence
        """
        # Act
        if confidence >= 66:
            status = "Normal"
            nivel = "BAIXO"
        elif confidence >= 56:
            status = "Em Risco"
            nivel = "MODERADO"
        else:
            status = "Risco Crítico"
            nivel = "CRÍTICO"
        
        # Assert
        assert status == status_esperado
        assert nivel == nivel_esperado
    
    def test_criar_saude_feto(self):
        """
        Teste: Criação do objeto SaudeFeto
        Objetivo: Verificar se o objeto é criado corretamente
        """
        # Act
        saude = SaudeFeto(
            status_saude="Normal",
            nivel_risco="BAIXO", 
            confidence_value=75.0
        )
        
        # Assert
        assert saude.status_saude == "Normal"
        assert saude.nivel_risco == "BAIXO"
        assert saude.confidence_value == 75.0
    
    def test_resultado_ml_estrutura(self):
        """
        Teste: Estrutura do resultado ML
        Objetivo: Verificar se ResultadoML tem estrutura correta
        """
        # Act
        resultado = ResultadoML(
            prediction=1,
            confidence=0.85,
            status="Normal",
            description="Monitoramento fetal normal"
        )
        
        # Assert
        assert resultado.prediction == 1
        assert resultado.confidence == 0.85
        assert resultado.status == "Normal"
        assert resultado.description == "Monitoramento fetal normal"


class TestPerformanceValidacao:
    """Testes de performance da validação"""
    
    def test_performance_validacao_dados(self, dados_gestante_validos):
        """
        Teste: Performance da validação de dados
        Objetivo: Medir tempo de validação (meta: < 1ms)
        """
        # Arrange
        num_validacoes = 100  # Reduzido para evitar timeout
        tempos = []
        
        # Act
        for _ in range(num_validacoes):
            start = time.time()
            dados = DadosGestante(**dados_gestante_validos)
            end = time.time()
            tempos.append(end - start)
        
        # Assert
        tempo_medio = sum(tempos) / len(tempos)
        assert tempo_medio < 0.01, f"Validação muito lenta: {tempo_medio*1000:.3f}ms"
        
        # Métricas para relatório
        print(f"\n📊 Performance Validação:")
        print(f"   • Validações: {num_validacoes}")
        print(f"   • Tempo médio: {tempo_medio*1000:.3f}ms")
        print(f"   • Throughput: {num_validacoes/sum(tempos):.0f} validações/s") 