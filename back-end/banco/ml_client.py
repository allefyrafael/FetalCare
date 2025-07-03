import httpx
import logging
from typing import Dict, Any
from .models import ParametrosMonitoramento, ResultadoML

logger = logging.getLogger(__name__)

class MLClient:
    """Cliente para comunicação com a API do modelo ML"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.timeout = 30.0
    
    async def fazer_predicao(self, parametros: ParametrosMonitoramento) -> ResultadoML:
        """
        Faz predição no modelo ML
        
        Args:
            parametros: Parâmetros de monitoramento fetal
            
        Returns:
            ResultadoML: Resultado da predição
        """
        try:
            # Converte os parâmetros para o formato esperado pela API
            dados_ml = self._converter_parametros_para_api(parametros)
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/predict",
                    json=dados_ml,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code != 200:
                    raise Exception(f"API ML retornou erro {response.status_code}: {response.text}")
                
                resultado_api = response.json()
                
                # Converte o resultado da API para nosso modelo
                resultado_ml = self._converter_resultado_da_api(resultado_api)
                
                logger.info(f"✅ Predição realizada: {resultado_ml.status} ({resultado_ml.confidence}%)")
                
                return resultado_ml
                
        except httpx.RequestError as e:
            logger.error(f"❌ Erro de conexão com API ML: {e}")
            raise Exception(f"Erro de conexão com o modelo ML: {e}")
        except Exception as e:
            logger.error(f"❌ Erro na predição ML: {e}")
            raise
    
    def _converter_parametros_para_api(self, parametros: ParametrosMonitoramento) -> Dict[str, Any]:
        """
        Converte parâmetros do nosso modelo para o formato da API ML
        
        Args:
            parametros: Parâmetros de monitoramento
            
        Returns:
            Dict: Dados no formato da API ML
        """
        return {
            "baseline_value": parametros.baseline_value,
            "accelerations": parametros.accelerations,
            "fetal_movement": parametros.fetal_movement,
            "uterine_contractions": parametros.uterine_contractions,
            "light_decelerations": parametros.light_decelerations,
            "severe_decelerations": parametros.severe_decelerations,
            "prolongued_decelerations": parametros.prolongued_decelerations,
            "abnormal_short_term_variability": parametros.abnormal_short_term_variability,
            "mean_value_of_short_term_variability": parametros.mean_value_of_short_term_variability,
            "percentage_of_time_with_abnormal_long_term_variability": parametros.percentage_of_time_with_abnormal_long_term_variability,
            "mean_value_of_long_term_variability": parametros.mean_value_of_long_term_variability,
            "histogram_width": parametros.histogram_width,
            "histogram_min": parametros.histogram_min,
            "histogram_max": parametros.histogram_max,
            "histogram_number_of_peaks": parametros.histogram_number_of_peaks,
            "histogram_number_of_zeroes": parametros.histogram_number_of_zeroes,
            "histogram_mode": parametros.histogram_mode,
            "histogram_mean": parametros.histogram_mean,
            "histogram_median": parametros.histogram_median,
            "histogram_variance": parametros.histogram_variance,
            "histogram_tendency": parametros.histogram_tendency or "normal"
        }
    
    def _converter_resultado_da_api(self, resultado_api: Dict[str, Any]) -> ResultadoML:
        """
        Converte resultado da API ML para nosso modelo
        
        Args:
            resultado_api: Resposta da API ML
            
        Returns:
            ResultadoML: Resultado convertido
        """
        return ResultadoML(
            prediction=resultado_api.get("prediction", 1),
            confidence=resultado_api.get("confidence", 0.0),
            status=resultado_api.get("status", "Unknown"),
            description=resultado_api.get("description", "Análise realizada"),
            recommendations=resultado_api.get("recommendations", [])
        )
    
    async def verificar_saude_api(self) -> Dict[str, Any]:
        """
        Verifica se a API ML está funcionando
        
        Returns:
            Dict: Status da API
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/")
                
                if response.status_code == 200:
                    return {
                        "status": "healthy",
                        "api_response": response.json()
                    }
                else:
                    return {
                        "status": "unhealthy",
                        "error": f"Status code: {response.status_code}"
                    }
                    
        except Exception as e:
            logger.error(f"❌ API ML indisponível: {e}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    async def obter_cenarios_teste(self) -> Dict[str, Any]:
        """
        Obtém cenários de teste da API ML
        
        Returns:
            Dict: Cenários disponíveis
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/test-scenarios")
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {}
                    
        except Exception as e:
            logger.error(f"❌ Erro ao obter cenários: {e}")
            return {}
    
    async def obter_info_modelo(self) -> Dict[str, Any]:
        """
        Obtém informações do modelo ML
        
        Returns:
            Dict: Informações do modelo
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/model-info")
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {}
                    
        except Exception as e:
            logger.error(f"❌ Erro ao obter info do modelo: {e}")
            return {}

# Instância global
ml_client = MLClient() 