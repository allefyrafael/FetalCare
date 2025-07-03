from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any
from bson import ObjectId

class DadosGestante(BaseModel):
    """Dados básicos da gestante"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    patient_id: str = Field(..., description="ID da gestante")
    patient_name: str = Field(..., description="Nome completo")
    patient_cpf: str = Field(..., description="CPF")
    gestational_age: int = Field(..., description="Idade gestacional em semanas")
    last_menstrual_period: Optional[datetime] = Field(None, description="Data da última menstruação")
    expected_delivery: Optional[datetime] = Field(None, description="Data provável do parto")
    blood_type: Optional[str] = Field(None, description="Tipo sanguíneo")
    pregnancy_number: Optional[int] = Field(None, description="Número da gravidez")
    risk_factors: Optional[str] = Field(None, description="Fatores de risco")
    patient_age: Optional[int] = Field(None, description="Idade da gestante")
    patient_phone: Optional[str] = Field(None, description="Telefone")
    patient_address: Optional[str] = Field(None, description="Endereço")
    emergency_contact: Optional[str] = Field(None, description="Contato de emergência")
    health_insurance: Optional[str] = Field(None, description="Convênio")
    responsible_doctor: Optional[str] = Field(None, description="Médico responsável")

class ParametrosMonitoramento(BaseModel):
    """Parâmetros de monitoramento fetal para o modelo ML"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    baseline_value: float = Field(..., description="Valor basal da FCF (bpm)")
    accelerations: int = Field(..., description="Número de acelerações")
    fetal_movement: int = Field(..., description="Movimento fetal")
    uterine_contractions: int = Field(..., description="Contrações uterinas")
    light_decelerations: int = Field(0, description="Decelerações leves")
    severe_decelerations: int = Field(0, description="Decelerações severas")
    prolongued_decelerations: int = Field(0, description="Decelerações prolongadas")
    abnormal_short_term_variability: int = Field(0, description="Variabilidade anormal de curto prazo")
    mean_value_of_short_term_variability: float = Field(..., description="Valor médio da variabilidade de curto prazo")
    percentage_of_time_with_abnormal_long_term_variability: int = Field(0, description="% tempo com variabilidade anormal de longo prazo")
    mean_value_of_long_term_variability: float = Field(..., description="Valor médio da variabilidade de longo prazo")
    histogram_width: int = Field(0, description="Largura do histograma")
    histogram_min: int = Field(0, description="Valor mínimo do histograma")
    histogram_max: int = Field(0, description="Valor máximo do histograma")
    histogram_number_of_peaks: int = Field(0, description="Número de picos do histograma")
    histogram_number_of_zeroes: int = Field(0, description="Número de zeros do histograma")
    histogram_mode: int = Field(0, description="Moda do histograma")
    histogram_mean: int = Field(0, description="Média do histograma")
    histogram_median: int = Field(0, description="Mediana do histograma")
    histogram_variance: int = Field(0, description="Variância do histograma")
    histogram_tendency: Optional[str] = Field(None, description="Tendência do histograma")

class ResultadoML(BaseModel):
    """Resultado do modelo de Machine Learning"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    prediction: int = Field(..., description="Predição do modelo (1, 2, 3)")
    confidence: float = Field(..., description="Confiança da predição (%)")
    status: str = Field(..., description="Status retornado pelo modelo")
    description: str = Field(..., description="Descrição do resultado")
    recommendations: list = Field(default_factory=list, description="Recomendações médicas")

class SaudeFeto(BaseModel):
    """Status da saúde do feto baseado na confidence"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    status_saude: str = Field(..., description="Status da saúde (Normal, Em Risco, Risco Crítico)")
    confidence_value: float = Field(..., description="Valor da confiança")
    nivel_risco: str = Field(..., description="Nível de risco determinado")

class RegistroExame(BaseModel):
    """Registro completo do exame fetal"""
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
    
    id: Optional[str] = Field(default=None, alias="_id")
    
    # Dados da gestante
    dados_gestante: DadosGestante
    
    # Parâmetros do monitoramento
    parametros_monitoramento: ParametrosMonitoramento
    
    # Resultado do ML
    resultado_ml: ResultadoML
    
    # Saúde do feto (calculado baseado na confidence)
    saude_feto: SaudeFeto
    
    # Metadados
    data_exame: datetime = Field(default_factory=datetime.utcnow, description="Data e hora do exame")
    medico_responsavel: Optional[str] = Field(None, description="Médico que realizou o exame")
    observacoes: Optional[str] = Field(None, description="Observações adicionais")

class RegistroExameCreate(BaseModel):
    """Schema para criar um novo registro de exame"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    dados_gestante: DadosGestante
    parametros_monitoramento: ParametrosMonitoramento
    medico_responsavel: Optional[str] = None
    observacoes: Optional[str] = None

def determinar_status_saude(confidence: float) -> tuple[str, str]:
    """
    Determina o status de saúde baseado na confidence do modelo ML
    
    Args:
        confidence: Valor da confiança (0-100)
        
    Returns:
        tuple: (status_saude, nivel_risco)
    """
    if confidence <= 55:
        return "Risco Crítico", "CRÍTICO"
    elif 56 <= confidence <= 65:
        return "Em Risco", "MODERADO"  
    else:  # >= 66
        return "Normal", "BAIXO"

def criar_saude_feto(confidence: float) -> SaudeFeto:
    """
    Cria objeto SaudeFeto baseado na confidence
    
    Args:
        confidence: Valor da confiança do modelo ML
        
    Returns:
        SaudeFeto: Objeto com status de saúde calculado
    """
    status_saude, nivel_risco = determinar_status_saude(confidence)
    
    return SaudeFeto(
        status_saude=status_saude,
        confidence_value=confidence,
        nivel_risco=nivel_risco
    ) 