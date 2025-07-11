// Configuração da API
const API_BASE_URL = 'http://127.0.0.1:5001';

// Estado da aplicação
let currentPatient = null;
let isApiConnected = false;

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    checkApiConnection();
});

/**
 * Inicializar aplicação
 */
function initializeApp() {
    console.log('FetalCare - Sistema iniciado');
    loadDefaultValues();
}

/**
 * Configurar event listeners
 */
function setupEventListeners() {
    // Formulário de dados da gestante
    const patientForm = document.getElementById('patientForm');
    if (patientForm) {
        patientForm.addEventListener('submit', handlePatientSubmit);
    }

    // Formulário de monitoramento
    const monitoringForm = document.getElementById('monitoringForm');
    if (monitoringForm) {
        monitoringForm.addEventListener('submit', handleMonitoringSubmit);
    }

    // Botão carregar padrões
    const loadDefaultsBtn = document.getElementById('loadDefaults');
    if (loadDefaultsBtn) {
        loadDefaultsBtn.addEventListener('click', loadDefaultValues);
    }

    // Botões de teste
    const testButtons = document.querySelectorAll('.test-btn');
    testButtons.forEach(button => {
        button.addEventListener('click', function() {
            const scenario = this.getAttribute('data-scenario');
            runTestScenario(scenario);
        });
    });

    // Botão salvar resultados
    const saveResultsBtn = document.getElementById('saveResults');
    if (saveResultsBtn) {
        saveResultsBtn.addEventListener('click', saveResults);
    }

    // Botão ver registros
    const viewRecordsBtn = document.getElementById('viewRecordsBtn');
    if (viewRecordsBtn) {
        viewRecordsBtn.addEventListener('click', function() {
            window.location.href = 'records.html';
        });
    }
}

/**
 * Verificar conexão com API
 */
async function checkApiConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            updateConnectionStatus(true);
            isApiConnected = true;
            showNotification('Sistema conectado com sucesso!', 'success');
        } else {
            updateConnectionStatus(false);
        }
    } catch (error) {
        console.error('Erro ao conectar com API:', error);
        updateConnectionStatus(false);
        showNotification('Modo offline - usando simulação local', 'warning');
    }
}

/**
 * Atualizar status de conexão
 */
function updateConnectionStatus(connected) {
    const connectionStatus = document.getElementById('connectionStatus');
    if (connectionStatus) {
        connectionStatus.innerHTML = connected ? 
            '<i class="fas fa-circle"></i> Sistema Online' : 
            '<i class="fas fa-circle"></i> Sistema Offline';
        
        connectionStatus.className = connected ? 'status online' : 'status offline';
    }
}

/**
 * Manipular submissão do formulário de gestante
 */
function handlePatientSubmit(event) {
    event.preventDefault();
    
    try {
        const patientData = collectPatientData();
        currentPatient = patientData;
        
        showNotification(`Dados da gestante ${patientData.name} salvos com sucesso!`, 'success');
        
        // Scroll para seção de monitoramento
        const monitoringSection = document.querySelector('.card:nth-of-type(2)');
        if (monitoringSection) {
            monitoringSection.scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
            });
        }
        
    } catch (error) {
        showNotification(`Erro: ${error.message}`, 'error');
    }
}

/**
 * Manipular submissão do formulário de monitoramento
 */
async function handleMonitoringSubmit(event) {
    event.preventDefault();
    
    if (!currentPatient) {
        showNotification('Por favor, preencha primeiro os dados da gestante.', 'warning');
        document.getElementById('patientName').focus();
        return;
    }
    
    showLoading(true);
    
    try {
        const monitoringData = collectMonitoringData();
        const prediction = await makePrediction(monitoringData);
        
        displayResult(prediction, monitoringData);
        
    } catch (error) {
        console.error('Erro na análise:', error);
        showNotification('Erro ao realizar análise. Verifique os dados e tente novamente.', 'error');
    } finally {
        showLoading(false);
    }
}

/**
 * Coletar dados da gestante
 */
function collectPatientData() {
    const name = document.getElementById('patientName').value.trim();
    const id = document.getElementById('patientId').value.trim();
    const cpf = document.getElementById('patientCpf').value.trim();
    const gestationalAge = document.getElementById('gestationalAge').value;
    const age = document.getElementById('patientAge').value;
    
    if (!name || !id || !gestationalAge) {
        throw new Error('Preencha todos os campos obrigatórios da gestante');
    }
    
    return {
        name,
        id,
        cpf: cpf || '00000000000',
        gestational_age: parseInt(gestationalAge),
        age: age ? parseInt(age) : null,
        timestamp: new Date().toISOString()
    };
}

/**
 * Coletar dados de monitoramento
 */
function collectMonitoringData() {
    const monitoringForm = document.getElementById('monitoringForm');
    const formData = new FormData(monitoringForm);
    const data = {};
    
    // Campos obrigatórios
    const requiredFields = [
        'baseline_value',
        'accelerations', 
        'fetal_movement',
        'mean_value_of_short_term_variability',
        'mean_value_of_long_term_variability'
    ];
    
    // Verificar campos obrigatórios
    for (let field of requiredFields) {
        const value = formData.get(field);
        if (!value || value.trim() === '') {
            const label = document.querySelector(`label[for="${field.replace(/_/g, '')}"]`)?.textContent || field;
            throw new Error(`Campo obrigatório não preenchido: ${label}`);
        }
    }
    
    // Coletar todos os campos
    for (let [key, value] of formData.entries()) {
        if (key === 'histogram_tendency') {
            data[key] = value || 'normal';
        } else {
            data[key] = parseFloat(value) || 0;
        }
    }
    
    return data;
}

/**
 * Fazer predição
 */
async function makePrediction(data) {
    if (isApiConnected) {
        try {
            // Combinar dados da gestante com dados de monitoramento
            const fullData = {
                ...data,
                patient_name: currentPatient.name,
                patient_id: currentPatient.id,
                patient_cpf: currentPatient.cpf || '00000000000',
                gestational_age: currentPatient.gestational_age,
                patient_age: currentPatient.age || 0
            };

            const response = await fetch(`${API_BASE_URL}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(fullData)
            });

            if (!response.ok) {
                throw new Error('Erro na API');
            }

            const result = await response.json();
            
            // Verificar se foi salvo no banco
            if (result.saved_to_database) {
                showNotification('Dados salvos no banco de dados com sucesso!', 'success');
                console.log('Registro salvo com ID:', result.record_id);
            }
            
            return {
                confidence: result.confidence,
                prediction: result.prediction,
                status: determineStatus(result.confidence),
                recommendations: result.recommendations || generateRecommendations(result.confidence),
                record_id: result.record_id,
                saved_to_database: result.saved_to_database
            };
            
        } catch (error) {
            console.log('API indisponível, usando simulação');
            return generateIntelligentSimulation(data);
        }
    } else {
        return generateIntelligentSimulation(data);
    }
}

/**
 * Gerar simulação inteligente
 */
function generateIntelligentSimulation(data) {
    let riskScore = 0;
    
    // Análise do baseline
    if (data.baseline_value < 110 || data.baseline_value > 160) {
        riskScore += 30;
    } else if (data.baseline_value < 120 || data.baseline_value > 150) {
        riskScore += 15;
    }
    
    // Análise das acelerações
    if (data.accelerations === 0) {
        riskScore += 20;
    } else if (data.accelerations < 2) {
        riskScore += 10;
    }
    
    // Análise do movimento fetal
    if (data.fetal_movement === 0) {
        riskScore += 25;
    } else if (data.fetal_movement < 2) {
        riskScore += 15;
    }
    
    // Análise das decelerações
    if (data.severe_decelerations > 0) {
        riskScore += 35;
    }
    if (data.prolongued_decelerations > 0) {
        riskScore += 30;
    }
    if (data.light_decelerations > 2) {
        riskScore += 15;
    }
    
    // Análise das contrações
    if (data.uterine_contractions > 3) {
        riskScore += 10;
    }
    
    // Análise da variabilidade
    if (data.abnormal_short_term_variability > 50) {
        riskScore += 20;
    }
    if (data.mean_value_of_short_term_variability < 1.0) {
        riskScore += 15;
    }
    
    // Converter score de risco em confiança
    let confidence;
    if (riskScore >= 60) {
        confidence = Math.max(30, 55 - (riskScore - 60) * 0.5);
    } else if (riskScore >= 30) {
        confidence = 56 + (63 - 56) * (1 - (riskScore - 30) / 30);
    } else {
        confidence = 64 + (94 - 64) * (1 - riskScore / 30);
    }
    
    confidence = Math.max(30, Math.min(94, confidence));
    
    return {
        confidence: confidence,
        prediction: confidence <= 55 ? 3 : (confidence <= 63 ? 2 : 1),
        status: determineStatus(confidence),
        recommendations: generateRecommendations(confidence)
    };
}

/**
 * Determinar status baseado na confiança
 */
function determineStatus(confidence) {
    if (confidence <= 55) {
        return {
            text: 'Risco Crítico',
            class: 'danger',
            description: 'Situação crítica que requer intervenção médica imediata'
        };
    } else if (confidence <= 63) {
        return {
            text: 'Risco',
            class: 'warning', 
            description: 'Situação de risco que necessita acompanhamento médico próximo'
        };
    } else {
        return {
            text: 'Saudável',
            class: 'success',
            description: 'Feto saudável - parâmetros dentro da normalidade'
        };
    }
}

/**
 * Gerar recomendações baseadas na confiança
 */
function generateRecommendations(confidence) {
    if (confidence <= 55) {
        return [
            'URGENTE: Contate médico imediatamente',
            'Considere internação hospitalar',
            'Monitoramento contínuo necessário',
            'Avalie necessidade de parto de emergência'
        ];
    } else if (confidence <= 63) {
        return [
            'Aumente a frequência do monitoramento',
            'Considere realizar cardiotocografia adicional',
            'Agende consulta médica em 24-48 horas',
            'Monitore movimentos fetais de perto'
        ];
    } else {
        return [
            'Continue o monitoramento de rotina',
            'Mantenha consultas pré-natais regulares',
            'Acompanhe os movimentos fetais diariamente',
            'Mantenha estilo de vida saudável'
        ];
    }
}

/**
 * Exibir resultado
 */
function displayResult(prediction, monitoringData) {
    const status = prediction.status;
    const resultsSection = document.getElementById('resultsSection');
    
    // Mostrar seção de resultados
    resultsSection.style.display = 'block';
    
    // Atualizar ícone de status
    const statusIcon = document.getElementById('statusIcon');
    if (statusIcon) {
        statusIcon.className = `status-icon ${status.class}`;
    }
    
    // Atualizar texto de status
    const statusText = document.getElementById('statusText');
    if (statusText) {
        statusText.textContent = status.text;
    }
    
    // Atualizar descrição
    const statusDescription = document.getElementById('statusDescription');
    if (statusDescription) {
        statusDescription.textContent = status.description;
    }
    
    // Atualizar barra de status
    const statusBarFill = document.getElementById('statusBarFill');
    const statusLabel = document.getElementById('statusLabel');
    if (statusBarFill && statusLabel) {
        let barWidth;
        if (prediction.confidence <= 55) {
            barWidth = 25;
        } else if (prediction.confidence <= 63) {
            barWidth = 60;
        } else {
            barWidth = 90;
        }
        
        statusBarFill.style.width = `${barWidth}%`;
        statusBarFill.className = `status-bar-fill ${status.class}`;
        statusLabel.textContent = status.text;
    }
    
    // Mostrar detalhes
    const resultDetails = document.getElementById('resultDetails');
    if (resultDetails) {
        resultDetails.style.display = 'block';
        
        // Atualizar valores
        const detailBaseline = document.getElementById('detailBaseline');
        const detailAccelerations = document.getElementById('detailAccelerations');
        const detailMovement = document.getElementById('detailMovement');
        const detailTimestamp = document.getElementById('detailTimestamp');
        
        if (detailBaseline) detailBaseline.textContent = `${monitoringData.baseline_value} bpm`;
        if (detailAccelerations) detailAccelerations.textContent = monitoringData.accelerations;
        if (detailMovement) detailMovement.textContent = monitoringData.fetal_movement;
        if (detailTimestamp) detailTimestamp.textContent = new Date().toLocaleString('pt-BR');
    }
    
    // Atualizar recomendações
    const recommendationsList = document.getElementById('recommendationsList');
    if (recommendationsList && prediction.recommendations) {
        recommendationsList.innerHTML = prediction.recommendations
            .map(rec => `<li>${rec}</li>`)
            .join('');
    }
    
    // Scroll para resultados
    resultsSection.scrollIntoView({ behavior: 'smooth' });
    
    // Mostrar notificação
    showNotification(`Análise concluída: ${status.text}`, status.class === 'success' ? 'success' : 
                    status.class === 'warning' ? 'warning' : 'error');
}

/**
 * Carregar valores padrão
 */
function loadDefaultValues() {
    const defaults = {
        baselineValue: 140,
        accelerations: 2,
        fetalMovement: 3,
        uterineContractions: 0,
        lightDecelerations: 0,
        severeDecelerations: 0,
        prolonguedDecelerations: 0,
        abnormalShortTermVariability: 20,
        meanValueOfShortTermVariability: 1.5,
        percentageOfTimeWithAbnormalLongTermVariability: 10,
        meanValueOfLongTermVariability: 8.5,
        histogramWidth: 150,
        histogramMin: 110,
        histogramMax: 160,
        histogramNumberOfPeaks: 3,
        histogramNumberOfZeroes: 0,
        histogramMode: 140,
        histogramMean: 142,
        histogramMedian: 141,
        histogramVariance: 25,
        histogramTendency: 'normal'
    };
    
    Object.entries(defaults).forEach(([key, value]) => {
        const element = document.getElementById(key);
        if (element) {
            element.value = value;
        }
    });
    
    showNotification('Valores padrão carregados com sucesso!', 'success');
}

/**
 * Executar cenário de teste
 */
async function runTestScenario(scenario) {
    const loadingOverlay = document.getElementById('loadingOverlay');
    if (loadingOverlay) loadingOverlay.style.display = 'flex';
    
    try {
        const scenarios = {
            normal: {
                name: "Maria da Silva",
                id: "G2024001",
                gestational_age: 32,
                age: 28,
                monitoring: {
                    baseline_value: 140,
                    accelerations: 3,
                    fetal_movement: 5,
                    uterine_contractions: 0,
                    light_decelerations: 0,
                    severe_decelerations: 0,
                    prolongued_decelerations: 0,
                    abnormal_short_term_variability: 20,
                    mean_value_of_short_term_variability: 1.5,
                    percentage_of_time_with_abnormal_long_term_variability: 10,
                    mean_value_of_long_term_variability: 8.5,
                    histogram_width: 150,
                    histogram_min: 110,
                    histogram_max: 160,
                    histogram_number_of_peaks: 3,
                    histogram_number_of_zeroes: 0,
                    histogram_mode: 140,
                    histogram_mean: 142,
                    histogram_median: 141,
                    histogram_variance: 25,
                    histogram_tendency: 'normal'
                }
            },
            risk: {
                name: "Ana Santos",
                id: "G2024002",
                gestational_age: 36,
                age: 32,
                monitoring: {
                    baseline_value: 165,
                    accelerations: 1,
                    fetal_movement: 2,
                    uterine_contractions: 3,
                    light_decelerations: 2,
                    severe_decelerations: 0,
                    prolongued_decelerations: 0,
                    abnormal_short_term_variability: 45,
                    mean_value_of_short_term_variability: 0.8,
                    percentage_of_time_with_abnormal_long_term_variability: 25,
                    mean_value_of_long_term_variability: 5.2,
                    histogram_width: 180,
                    histogram_min: 120,
                    histogram_max: 180,
                    histogram_number_of_peaks: 5,
                    histogram_number_of_zeroes: 2,
                    histogram_mode: 165,
                    histogram_mean: 158,
                    histogram_median: 162,
                    histogram_variance: 45,
                    histogram_tendency: 'increasing'
                }
            },
            critical: {
                name: "Carla Oliveira",
                id: "G2024003",
                gestational_age: 38,
                age: 35,
                monitoring: {
                    baseline_value: 95,
                    accelerations: 0,
                    fetal_movement: 0,
                    uterine_contractions: 5,
                    light_decelerations: 0,
                    severe_decelerations: 3,
                    prolongued_decelerations: 2,
                    abnormal_short_term_variability: 75,
                    mean_value_of_short_term_variability: 0.3,
                    percentage_of_time_with_abnormal_long_term_variability: 60,
                    mean_value_of_long_term_variability: 2.1,
                    histogram_width: 80,
                    histogram_min: 80,
                    histogram_max: 110,
                    histogram_number_of_peaks: 8,
                    histogram_number_of_zeroes: 15,
                    histogram_mode: 95,
                    histogram_mean: 92,
                    histogram_median: 94,
                    histogram_variance: 85,
                    histogram_tendency: 'decreasing'
                }
            }
        };
        
        const testData = scenarios[scenario];
        if (!testData) {
            throw new Error('Cenário de teste não encontrado');
        }
        
        // Preencher dados da gestante
        document.getElementById('patientName').value = testData.name;
        document.getElementById('patientId').value = testData.id;
        document.getElementById('gestationalAge').value = testData.gestational_age;
        document.getElementById('patientAge').value = testData.age;
        
        currentPatient = {
            name: testData.name,
            id: testData.id,
            gestational_age: testData.gestational_age,
            age: testData.age,
            timestamp: new Date().toISOString()
        };
        
        // Preencher parâmetros de monitoramento
        Object.entries(testData.monitoring).forEach(([key, value]) => {
            const elementId = key.replace(/_([a-z])/g, (g) => g[1].toUpperCase());
            const element = document.getElementById(elementId);
            if (element) {
                element.value = value;
            }
        });
        
        // Fazer predição
        const prediction = await makePrediction(testData.monitoring);
        displayResult(prediction, testData.monitoring);
        
        showNotification(`Teste "${testData.name}" executado com sucesso!`, 'success');
        
    } catch (error) {
        console.error('Erro no teste:', error);
        showNotification('Erro ao executar teste.', 'error');
    } finally {
        if (loadingOverlay) loadingOverlay.style.display = 'none';
    }
}

/**
 * Salvar resultados
 */
function saveResults() {
    if (!currentPatient) {
        showNotification('Nenhum resultado para salvar.', 'warning');
        return;
    }
    
    // Simular salvamento (localStorage)
    const timestamp = new Date().toISOString();
    const resultData = {
        patient: currentPatient,
        timestamp: timestamp,
        saved: true
    };
    
    localStorage.setItem(`fetalcare_result_${timestamp}`, JSON.stringify(resultData));
    showNotification('Resultados salvos com sucesso!', 'success');
}

/**
 * Mostrar/esconder loading
 */
function showLoading(show) {
    const loadingOverlay = document.getElementById('loadingOverlay');
    if (loadingOverlay) {
        loadingOverlay.style.display = show ? 'flex' : 'none';
    }
}

/**
 * Mostrar notificação
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    
    const icon = getNotificationIcon(type);
    notification.innerHTML = `
        <i class="fas fa-${icon}"></i>
        <span>${message}</span>
        <button class="close-notification">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    const container = document.getElementById('notifications');
    if (container) {
        container.appendChild(notification);
    } else {
        document.body.appendChild(notification);
    }
    
    // Auto-remover após 5 segundos
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
    
    // Evento de fechar
    const closeBtn = notification.querySelector('.close-notification');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        });
    }
}

/**
 * Obter ícone da notificação
 */
function getNotificationIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-triangle',
        warning: 'exclamation-circle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}
