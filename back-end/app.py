from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import os
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Carregar o modelo ML
model_path = os.path.join('IA', 'model.sav')
try:
    import warnings
    # Suprimir warnings de versão durante o carregamento
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        warnings.filterwarnings("ignore", category=FutureWarning)
        model = joblib.load(model_path)
    logger.info("Modelo carregado com sucesso!")
    logger.info(f"Tipo do modelo: {type(model).__name__}")
    
    # Verificar se o modelo tem os métodos necessários
    if hasattr(model, 'predict'):
        logger.info("Método predict disponível")
    if hasattr(model, 'predict_proba'):
        logger.info("Método predict_proba disponível")
    else:
        logger.warning("Método predict_proba não disponível - usando confiança padrão")
        
except Exception as e:
    logger.error(f"Erro ao carregar o modelo: {e}")
    logger.error(f"Caminho do modelo: {os.path.abspath(model_path)}")
    logger.error(f"Arquivo existe: {os.path.exists(model_path)}")
    model = None

# Mapeamento dos resultados do modelo
HEALTH_STATUS = {
    1: {"status": "Normal", "description": "Feto saudável - sem indicações de risco", "color": "success"},
    2: {"status": "Suspeito", "description": "Necessita acompanhamento médico mais próximo", "color": "warning"},
    3: {"status": "Patológico", "description": "Requer intervenção médica imediata", "color": "danger"}
}

# Lista dos campos esperados pelo modelo (na ordem correta)
EXPECTED_FEATURES = [
    'baseline_value',
    'accelerations', 
    'fetal_movement',
    'uterine_contractions',
    'light_decelerations',
    'severe_decelerations',
    'prolongued_decelerations',
    'abnormal_short_term_variability',
    'mean_value_of_short_term_variability',
    'percentage_of_time_with_abnormal_long_term_variability',
    'mean_value_of_long_term_variability',
    'histogram_width',
    'histogram_min',
    'histogram_max',
    'histogram_number_of_peaks',
    'histogram_number_of_zeroes',
    'histogram_mode',
    'histogram_mean',
    'histogram_median',
    'histogram_variance',
    'histogram_tendency'
]

@app.route('/')
def health_check():
    """Endpoint para verificar se o serviço está funcionando"""
    return jsonify({
        "status": "healthy",
        "service": "FetalCare ML API",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint principal para fazer predições de saúde fetal"""
    try:
        if model is None:
            return jsonify({
                "error": "Modelo não está carregado",
                "status": "error"
            }), 500

        # Obter dados do request
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "Nenhum dado fornecido",
                "status": "error"
            }), 400

        # Extrair features na ordem correta
        features = []
        missing_features = []
        
        for feature in EXPECTED_FEATURES:
            if feature in data:
                # Converter histogram_tendency para valor numérico se necessário
                if feature == 'histogram_tendency':
                    tendency_map = {
                        'normal': 0,
                        'increasing': 1,
                        'decreasing': -1,
                        'stable': 0
                    }
                    value = tendency_map.get(data[feature], 0)
                else:
                    value = float(data[feature])
                features.append(value)
            else:
                missing_features.append(feature)
                features.append(0)  # Valor padrão para features faltantes

        if len(missing_features) > 5:  # Permitir algumas features faltantes
            return jsonify({
                "error": f"Muitas features obrigatórias faltando: {missing_features[:5]}...",
                "status": "error"
            }), 400

        # Converter para array numpy e fazer predição
        features_array = np.array(features).reshape(1, -1)
        
        # Suprimir warnings durante a predição
        import warnings
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            
            # Fazer predição
            prediction = model.predict(features_array)[0]
            
            # Tentar obter probabilidades se o modelo suportar
            try:
                probabilities = model.predict_proba(features_array)[0]
                confidence = float(max(probabilities))
            except:
                confidence = 0.85  # Confiança padrão se não conseguir calcular

        # Mapear resultado
        result = HEALTH_STATUS.get(int(prediction), {
            "status": "Desconhecido",
            "description": "Resultado não mapeado",
            "color": "secondary"
        })

        # Preparar resposta
        response = {
            "prediction": int(prediction),
            "status": result["status"],
            "description": result["description"],
            "color": result["color"],
            "confidence": round(confidence * 100, 2),
            "timestamp": datetime.now().isoformat(),
            "patient_data": {
                "baseline_value": data.get('baseline_value'),
                "accelerations": data.get('accelerations'),
                "fetal_movement": data.get('fetal_movement')
            }
        }

        # Adicionar recomendações baseadas no resultado
        if prediction == 1:
            response["recommendations"] = [
                "Continue o monitoramento de rotina",
                "Mantenha consultas pré-natais regulares",
                "Acompanhe os movimentos fetais diariamente"
            ]
        elif prediction == 2:
            response["recommendations"] = [
                "Aumente a frequência do monitoramento",
                "Considere realizar cardiotocografia adicional",
                "Agende consulta médica em 24-48 horas"
            ]
        else:  # prediction == 3
            response["recommendations"] = [
                "URGENTE: Contate médico imediatamente",
                "Considere internação hospitalar",
                "Monitoramento contínuo necessário"
            ]

        logger.info(f"Predição realizada: {result['status']} (confiança: {confidence:.2%})")
        
        return jsonify(response)

    except Exception as e:
        logger.error(f"Erro na predição: {e}")
        return jsonify({
            "error": f"Erro interno do servidor: {str(e)}",
            "status": "error"
        }), 500

@app.route('/test-scenarios', methods=['GET'])
def get_test_scenarios():
    """Endpoint para obter cenários de teste pré-definidos"""
    scenarios = {
        "normal": {
            "name": "Feto Saudável",
            "data": {
                "baseline_value": 140,
                "accelerations": 3,
                "fetal_movement": 4,
                "uterine_contractions": 0,
                "light_decelerations": 0,
                "severe_decelerations": 0,
                "prolongued_decelerations": 0,
                "abnormal_short_term_variability": 0,
                "mean_value_of_short_term_variability": 5.5,
                "percentage_of_time_with_abnormal_long_term_variability": 10,
                "mean_value_of_long_term_variability": 25,
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
            }
        },
        "suspicious": {
            "name": "Feto Suspeito",
            "data": {
                "baseline_value": 160,
                "accelerations": 1,
                "fetal_movement": 2,
                "uterine_contractions": 2,
                "light_decelerations": 2,
                "severe_decelerations": 0,
                "prolongued_decelerations": 0,
                "abnormal_short_term_variability": 15,
                "mean_value_of_short_term_variability": 3.2,
                "percentage_of_time_with_abnormal_long_term_variability": 25,
                "mean_value_of_long_term_variability": 18,
                "histogram_width": 80,
                "histogram_min": 110,
                "histogram_max": 170,
                "histogram_number_of_peaks": 2,
                "histogram_number_of_zeroes": 5,
                "histogram_mode": 160,
                "histogram_mean": 158,
                "histogram_median": 160,
                "histogram_variance": 25,
                "histogram_tendency": "decreasing"
            }
        },
        "pathological": {
            "name": "Feto Patológico",
            "data": {
                "baseline_value": 110,
                "accelerations": 0,
                "fetal_movement": 0,
                "uterine_contractions": 5,
                "light_decelerations": 5,
                "severe_decelerations": 3,
                "prolongued_decelerations": 2,
                "abnormal_short_term_variability": 45,
                "mean_value_of_short_term_variability": 1.8,
                "percentage_of_time_with_abnormal_long_term_variability": 60,
                "mean_value_of_long_term_variability": 8,
                "histogram_width": 40,
                "histogram_min": 80,
                "histogram_max": 130,
                "histogram_number_of_peaks": 1,
                "histogram_number_of_zeroes": 15,
                "histogram_mode": 110,
                "histogram_mean": 108,
                "histogram_median": 110,
                "histogram_variance": 45,
                "histogram_tendency": "decreasing"
            }
        }
    }
    
    return jsonify(scenarios)

@app.route('/model-info', methods=['GET'])
def get_model_info():
    """Endpoint para obter informações sobre o modelo"""
    if model is None:
        return jsonify({
            "error": "Modelo não carregado",
            "status": "error"
        }), 500
    
    try:
        model_info = {
            "model_type": str(type(model).__name__),
            "features_count": len(EXPECTED_FEATURES),
            "features": EXPECTED_FEATURES,
            "health_classes": HEALTH_STATUS,
            "model_loaded": True,
            "timestamp": datetime.now().isoformat()
        }
        
        # Tentar obter mais informações do modelo se disponível
        if hasattr(model, 'n_features_in_'):
            model_info["n_features_in"] = model.n_features_in_
        
        if hasattr(model, 'classes_'):
            model_info["classes"] = model.classes_.tolist()
            
        return jsonify(model_info)
        
    except Exception as e:
        logger.error(f"Erro ao obter informações do modelo: {e}")
        return jsonify({
            "error": f"Erro ao obter informações: {str(e)}",
            "status": "error"
        }), 500

# Endpoint para servir arquivos estáticos do front-end
@app.route('/frontend/<path:filename>')
def serve_frontend(filename):
    """Servir arquivos do front-end"""
    return send_from_directory('../front-end', filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Iniciando servidor na porta {port}")
    logger.info(f"Modelo carregado: {'Sim' if model else 'Não'}")
    
    app.run(host='0.0.0.0', port=port, debug=debug) 