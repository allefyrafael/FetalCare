# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import os
import logging
from datetime import datetime
import warnings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Importar módulos do banco de dados
try:
    from banco.database import get_sync_collection
    from banco.models import determinar_status_saude
    DATABASE_AVAILABLE = True
    logger.info("Módulos do banco de dados importados com sucesso")
except ImportError as e:
    logger.warning(f"Banco de dados não disponível: {e}")
    DATABASE_AVAILABLE = False

# Carregar o modelo ML
model_path = os.path.join('IA', 'model.sav')
try:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        warnings.filterwarnings("ignore", category=FutureWarning)
        model = joblib.load(model_path)
    logger.info("Modelo ML carregado com sucesso!")
    logger.info(f"Tipo do modelo: {type(model).__name__}")
except Exception as e:
    logger.error(f"Erro ao carregar o modelo: {e}")
    model = None

# Mapeamento dos resultados do modelo
HEALTH_STATUS = {
    1: {"status": "Normal", "description": "Feto saudável - sem indicações de risco", "color": "success"},
    2: {"status": "Suspeito", "description": "Necessita acompanhamento médico mais próximo", "color": "warning"},
    3: {"status": "Patológico", "description": "Requer intervenção médica imediata", "color": "danger"}
}

# Lista dos campos esperados pelo modelo
EXPECTED_FEATURES = [
    'baseline_value', 'accelerations', 'fetal_movement', 'uterine_contractions',
    'light_decelerations', 'severe_decelerations', 'prolongued_decelerations',
    'abnormal_short_term_variability', 'mean_value_of_short_term_variability',
    'percentage_of_time_with_abnormal_long_term_variability',
    'mean_value_of_long_term_variability', 'histogram_width', 'histogram_min',
    'histogram_max', 'histogram_number_of_peaks', 'histogram_number_of_zeroes',
    'histogram_mode', 'histogram_mean', 'histogram_median', 'histogram_variance',
    'histogram_tendency'
]

def save_prediction_to_database(data, prediction_result):
    """Salva a predição no banco de dados"""
    if not DATABASE_AVAILABLE:
        logger.warning("Banco de dados não disponível - dados não salvos")
        return None
    
    try:
        collection = get_sync_collection()
        
        # Determinar status de saúde baseado na confidence
        status_saude, nivel_risco = determinar_status_saude(prediction_result['confidence'])
        
        # Montar documento completo
        registro_data = {
            "dados_gestante": {
                "patient_id": data.get('patient_id', f"AUTO_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
                "patient_name": data.get('patient_name', 'Paciente Não Identificado'),
                "patient_cpf": data.get('patient_cpf', '00000000000'),
                "gestational_age": data.get('gestational_age', 0),
                "patient_age": data.get('patient_age', 0)
            },
            "parametros_monitoramento": {key: data.get(key, 0) for key in EXPECTED_FEATURES},
            "resultado_ml": {
                "prediction": prediction_result['prediction'],
                "confidence": prediction_result['confidence'],
                "status": prediction_result['status'],
                "description": prediction_result['description'],
                "recommendations": prediction_result.get('recommendations', [])
            },
            "saude_feto": {
                "status_saude": status_saude,
                "confidence_value": prediction_result['confidence'],
                "nivel_risco": nivel_risco
            },
            "data_exame": datetime.utcnow(),
            "medico_responsavel": data.get('medico_responsavel'),
            "observacoes": data.get('observacoes')
        }
        
        # Inserir no banco
        result = collection.insert_one(registro_data)
        
        logger.info(f"Registro salvo no banco com ID: {result.inserted_id}")
        logger.info(f"Status saúde: {status_saude} (Confidence: {prediction_result['confidence']}%)")
        
        return str(result.inserted_id)
        
    except Exception as e:
        logger.error(f"Erro ao salvar no banco: {e}")
        return None

@app.route('/')
def health_check():
    """Endpoint para verificar se o serviço está funcionando"""
    database_status = "available" if DATABASE_AVAILABLE else "unavailable"
    
    try:
        if DATABASE_AVAILABLE:
            collection = get_sync_collection()
            total_records = collection.count_documents({})
            database_status = f"available ({total_records} records)"
    except:
        database_status = "available but connection failed"
    
    return jsonify({
        "status": "healthy",
        "service": "FetalCare ML API with Database",
        "model_loaded": model is not None,
        "database_status": database_status,
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

        data = request.get_json()
        if not data:
            return jsonify({
                "error": "Nenhum dado fornecido",
                "status": "error"
            }), 400

        # Extrair features na ordem correta
        features = []
        for feature in EXPECTED_FEATURES:
            if feature in data:
                if feature == 'histogram_tendency':
                    tendency_map = {'normal': 0, 'increasing': 1, 'decreasing': -1, 'stable': 0}
                    value = tendency_map.get(data[feature], 0)
                else:
                    value = float(data[feature])
                features.append(value)
            else:
                features.append(0)

        # Fazer predição
        features_array = np.array(features).reshape(1, -1)
        
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            prediction = model.predict(features_array)[0]
            
            try:
                probabilities = model.predict_proba(features_array)[0]
                confidence = float(max(probabilities))
            except:
                confidence = 0.85

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

        # Adicionar recomendações
        if prediction == 1:
            response["recommendations"] = [
                "Continue o monitoramento de rotina",
                "Mantenha consultas pré-natais regulares",
                "Acompanhe os movimentos fetais diariamente",
                "Mantenha estilo de vida saudável"
            ]
        elif prediction == 2:
            response["recommendations"] = [
                "Aumente a frequência do monitoramento",
                "Considere realizar cardiotocografia adicional",
                "Agende consulta médica em 24-48 horas",
                "Monitore movimentos fetais de perto"
            ]
        else:  # prediction == 3
            response["recommendations"] = [
                "URGENTE: Contate médico imediatamente",
                "Considere internação hospitalar",
                "Monitoramento contínuo necessário",
                "Avalie necessidade de parto de emergência"
            ]

        # Salvar no banco de dados
        record_id = save_prediction_to_database(data, response)
        
        # Adicionar informações sobre salvamento
        response["saved_to_database"] = record_id is not None
        if record_id:
            response["record_id"] = record_id

        logger.info(f"Predição realizada: {result['status']} (Confidence: {response['confidence']}%)")
        
        return jsonify(response)

    except Exception as e:
        logger.error(f"Erro na predição: {e}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/records', methods=['GET'])
def get_records():
    """Endpoint para buscar registros do banco de dados"""
    if not DATABASE_AVAILABLE:
        return jsonify({
            "error": "Banco de dados não disponível",
            "records": [],
            "total": 0
        }), 503
    
    try:
        collection = get_sync_collection()
        
        # Parâmetros de paginação
        limit = int(request.args.get('limit', 10))
        skip = int(request.args.get('skip', 0))
        
        # Filtros
        filters = {}
        
        # Filtro por CPF (busca parcial)
        cpf = request.args.get('cpf')
        if cpf:
            # Permite busca parcial usando regex
            filters['dados_gestante.patient_cpf'] = {'$regex': cpf, '$options': 'i'}
        
        # Filtro por status de saúde
        status_saude = request.args.get('status_saude')
        if status_saude:
            filters['saude_feto.status_saude'] = status_saude
        
        # Buscar registros
        cursor = collection.find(filters).sort('data_exame', -1).skip(skip).limit(limit)
        records = list(cursor)
        
        # Converter ObjectId para string
        for record in records:
            record['_id'] = str(record['_id'])
        
        # Contar total
        total = collection.count_documents(filters)
        
        return jsonify({
            "records": records,
            "total": total,
            "limit": limit,
            "skip": skip,
            "filters_applied": filters
        })
        
    except Exception as e:
        logger.error(f"Erro ao buscar registros: {e}")
        return jsonify({
            "error": str(e),
            "records": [],
            "total": 0
        }), 500

@app.route('/records/stats', methods=['GET'])
def get_records_stats():
    """Endpoint para obter estatísticas dos registros"""
    if not DATABASE_AVAILABLE:
        return jsonify({
            "error": "Banco de dados não disponível",
            "total_records": 0
        }), 503
    
    try:
        collection = get_sync_collection()
        
        # Total de registros
        total_records = collection.count_documents({})
        
        # Estatísticas por status de saúde
        pipeline = [
            {
                "$group": {
                    "_id": "$saude_feto.status_saude",
                    "count": {"$sum": 1}
                }
            }
        ]
        
        status_stats = list(collection.aggregate(pipeline))
        by_health_status = {item['_id']: item['count'] for item in status_stats}
        
        # Estatísticas por nível de risco
        pipeline_risk = [
            {
                "$group": {
                    "_id": "$saude_feto.nivel_risco",
                    "count": {"$sum": 1}
                }
            }
        ]
        
        risk_stats = list(collection.aggregate(pipeline_risk))
        by_risk_level = {item['_id']: item['count'] for item in risk_stats}
        
        return jsonify({
            "total_records": total_records,
            "by_health_status": by_health_status,
            "by_risk_level": by_risk_level,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {e}")
        return jsonify({
            "error": str(e),
            "total_records": 0
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    logger.info(f"Iniciando servidor na porta {port}")
    logger.info(f"Banco de dados: {'Disponível' if DATABASE_AVAILABLE else 'Não disponível'}")
    app.run(host='0.0.0.0', port=port, debug=True) 