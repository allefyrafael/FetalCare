console.log('Records page loaded');

// Configuração da API
const API_BASE_URL = 'http://127.0.0.1:5001';

// Estado da aplicação
let currentPage = 0;
let currentLimit = 10;
let currentFilters = {};
let totalRecords = 0;
let isApiConnected = false;

// Inicialização
document.addEventListener('DOMContentLoaded', async function() {
    console.log('FetalCare Records - Página iniciada');
    setupEventListeners();
    
    // Verificar conexão e carregar dados
    await initializeApp();
});

async function initializeApp() {
    try {
        showLoading();
        
        // Verificar conexão com a API
        console.log('Verificando conexão com API...');
        const response = await fetch(`${API_BASE_URL}/`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            console.log('API conectada com sucesso');
            isApiConnected = true;
            updateConnectionStatus(true);
            showNotification('Sistema conectado com sucesso!', 'success');
            
            // Carregar dados
            await loadStats();
            await loadRecords();
        } else {
            throw new Error('API não está saudável');
        }
    } catch (error) {
        console.error('Erro ao conectar com API:', error);
        isApiConnected = false;
        updateConnectionStatus(false);
        showNotification('Erro ao conectar com a API. Verifique se o servidor está rodando.', 'error');
        showNoRecords();
    }
}

function setupEventListeners() {
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            initializeApp();
        });
    }

    const applyFiltersBtn = document.getElementById('applyFilters');
    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', applyFilters);
    }

    const filterInputs = document.querySelectorAll('#filterCpf');
    filterInputs.forEach(input => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                applyFilters();
            }
        });
        
        // Formatação automática do CPF
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length <= 11) {
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
                value = value.replace(/(\d{3})\.(\d{3})(\d)/, '$1.$2.$3');
                value = value.replace(/\.(\d{3})(\d)/, '.$1-$2');
                e.target.value = value;
            }
        });
    });
}

function updateConnectionStatus(connected) {
    const connectionStatus = document.getElementById('connectionStatus');
    if (connectionStatus) {
        connectionStatus.innerHTML = connected ? 
            '<i class="fas fa-circle"></i> Sistema Online' : 
            '<i class="fas fa-circle"></i> Sistema Offline';
        
        connectionStatus.className = connected ? 'status online' : 'status offline';
    }
}

async function loadStats() {
    console.log('Carregando estatísticas...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/records/stats`);
        
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }

        const stats = await response.json();
        console.log('Estatísticas recebidas:', stats);
        
        document.getElementById('totalRecords').textContent = stats.total_records || 0;
        document.getElementById('normalCount').textContent = stats.by_health_status?.Normal || 0;
        document.getElementById('riskCount').textContent = stats.by_health_status?.['Em Risco'] || 0;
        document.getElementById('criticalCount').textContent = stats.by_health_status?.['Risco Crítico'] || 0;
        
    } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
        showNotification('Erro ao carregar estatísticas', 'error');
    }
}

async function loadRecords() {
    console.log('Carregando registros...');
    
    try {
        const params = new URLSearchParams({
            limit: currentLimit,
            skip: currentPage * currentLimit,
            ...currentFilters
        });

        const url = `${API_BASE_URL}/records?${params}`;
        console.log('URL da requisição:', url);

        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }

        const data = await response.json();
        console.log('Dados dos registros recebidos:', data);
        
        totalRecords = data.total;
        
        if (data.records && data.records.length > 0) {
            displayRecords(data.records);
            updatePagination();
            updateRecordCount();
        } else {
            console.log('Nenhum registro encontrado');
            showNoRecords();
        }
        
    } catch (error) {
        console.error('Erro ao carregar registros:', error);
        showNotification(`Erro ao carregar registros: ${error.message}`, 'error');
        showNoRecords();
    }
}

function displayRecords(records) {
    console.log(`Exibindo ${records.length} registros`);
    
    const tableBody = document.getElementById('recordsTableBody');
    const loadingMessage = document.getElementById('loadingMessage');
    const noRecordsMessage = document.getElementById('noRecordsMessage');
    
    if (!tableBody) {
        console.error('Elemento recordsTableBody não encontrado!');
        return;
    }
    
    // Esconder mensagens de loading/no records
    if (loadingMessage) loadingMessage.style.display = 'none';
    if (noRecordsMessage) noRecordsMessage.style.display = 'none';
    
    // Limpar tabela
    tableBody.innerHTML = '';
    
    // Adicionar registros
    records.forEach((record, index) => {
        console.log(`Criando linha para registro ${index}:`, record);
        
        const row = document.createElement('tr');
        row.className = 'record-row';
        
        const patientData = record.dados_gestante || {};
        const resultData = record.resultado_ml || {};
        const healthData = record.saude_feto || {};
        const paramsData = record.parametros_monitoramento || {};
        
        const date = new Date(record.data_exame);
        const formattedDate = date.toLocaleString('pt-BR');
        
        const statusClass = getStatusClass(healthData.status_saude);
        const statusBadge = `<span class="status-badge ${statusClass}">${healthData.status_saude || 'N/A'}</span>`;
        
        const confidence = resultData.confidence || 0;
        const confidenceBar = createConfidenceBar(confidence);
        
        row.innerHTML = `
            <td>${formattedDate}</td>
            <td>${patientData.patient_name || 'N/A'}</td>
            <td>
                <span class="cpf-cell" onclick="quickSearchCpf('${patientData.patient_cpf}')" title="Clique para filtrar por este CPF">
                    ${formatCpf(patientData.patient_cpf)}
                </span>
            </td>
            <td>${patientData.patient_id || 'N/A'}</td>
            <td>${patientData.gestational_age || 'N/A'} sem</td>
            <td>${statusBadge}</td>
            <td>${confidenceBar}</td>
            <td>${paramsData.baseline_value || 'N/A'} bpm</td>
            <td>
                <button class="btn btn-sm btn-secondary" onclick="toggleRecordDetails('${record._id}', ${index})">
                    <i class="fas fa-eye"></i> Detalhes
                </button>
            </td>
        `;
        
        tableBody.appendChild(row);
        
        // Criar linha de detalhes
        const detailsRow = createDetailsRow(record, index);
        tableBody.appendChild(detailsRow);
    });
    
    console.log('Registros exibidos com sucesso');
}

function createDetailsRow(record, index) {
    const detailsRow = document.createElement('tr');
    detailsRow.id = `details-${index}`;
    detailsRow.style.display = 'none';
    
    const patientData = record.dados_gestante || {};
    const resultData = record.resultado_ml || {};
    const healthData = record.saude_feto || {};
    const paramsData = record.parametros_monitoramento || {};
    
    const detailsContent = `
        <td colspan="9">
            <div class="record-details" style="display: block;">
                <h4><i class="fas fa-info-circle"></i> Detalhes do Exame</h4>
                
                <div class="detail-grid">
                    <div>
                        <h5>Dados da Gestante</h5>
                        <div class="detail-item">
                            <span class="detail-label">Nome:</span>
                            <span class="detail-value">${patientData.patient_name || 'N/A'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">CPF:</span>
                            <span class="detail-value">${formatCpf(patientData.patient_cpf) || 'N/A'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Idade:</span>
                            <span class="detail-value">${patientData.patient_age || 'N/A'} anos</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Idade Gestacional:</span>
                            <span class="detail-value">${patientData.gestational_age || 'N/A'} semanas</span>
                        </div>
                    </div>
                    
                    <div>
                        <h5>Parâmetros Principais</h5>
                        <div class="detail-item">
                            <span class="detail-label">FCF Basal:</span>
                            <span class="detail-value">${paramsData.baseline_value || 'N/A'} bpm</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Acelerações:</span>
                            <span class="detail-value">${paramsData.accelerations || 'N/A'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Movimento Fetal:</span>
                            <span class="detail-value">${paramsData.fetal_movement || 'N/A'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Contrações:</span>
                            <span class="detail-value">${paramsData.uterine_contractions || 'N/A'}</span>
                        </div>
                    </div>
                    
                    <div>
                        <h5>Resultado da Análise</h5>
                        <div class="detail-item">
                            <span class="detail-label">Status:</span>
                            <span class="detail-value">${resultData.status || 'N/A'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Confidence:</span>
                            <span class="detail-value">${resultData.confidence || 'N/A'}%</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Predição:</span>
                            <span class="detail-value">${resultData.prediction || 'N/A'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Nível de Risco:</span>
                            <span class="detail-value">${healthData.nivel_risco || 'N/A'}</span>
                        </div>
                    </div>
                    
                    <div>
                        <h5>Variabilidade</h5>
                        <div class="detail-item">
                            <span class="detail-label">Var. Curto Prazo:</span>
                            <span class="detail-value">${paramsData.mean_value_of_short_term_variability || 'N/A'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Var. Longo Prazo:</span>
                            <span class="detail-value">${paramsData.mean_value_of_long_term_variability || 'N/A'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Decelerações Severas:</span>
                            <span class="detail-value">${paramsData.severe_decelerations || 'N/A'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Decelerações Prolongadas:</span>
                            <span class="detail-value">${paramsData.prolongued_decelerations || 'N/A'}</span>
                        </div>
                    </div>
                </div>
                
                ${resultData.recommendations ? `
                    <div style="margin-top: 20px;">
                        <h5><i class="fas fa-lightbulb"></i> Recomendações</h5>
                        <ul>
                            ${resultData.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
            </div>
        </td>
    `;
    
    detailsRow.innerHTML = detailsContent;
    return detailsRow;
}

function toggleRecordDetails(recordId, index) {
    const detailsRow = document.getElementById(`details-${index}`);
    const button = event.target.closest('button');
    
    if (detailsRow.style.display === 'none') {
        detailsRow.style.display = 'table-row';
        button.innerHTML = '<i class="fas fa-eye-slash"></i> Ocultar';
    } else {
        detailsRow.style.display = 'none';
        button.innerHTML = '<i class="fas fa-eye"></i> Detalhes';
    }
}

function createConfidenceBar(confidence) {
    const color = confidence <= 55 ? '#dc3545' : confidence <= 63 ? '#ffc107' : '#28a745';
    
    return `
        <div class="confidence-bar">
            <div class="confidence-fill" style="width: ${confidence}%; background-color: ${color};"></div>
            <div class="confidence-text">${confidence}%</div>
        </div>
    `;
}

function getStatusClass(status) {
    switch (status) {
        case 'Normal':
            return 'status-normal';
        case 'Em Risco':
            return 'status-risk';
        case 'Risco Crítico':
            return 'status-critical';
        default:
            return 'status-normal';
    }
}

function applyFilters() {
    currentFilters = {};
    currentPage = 0;
    
    const cpf = document.getElementById('filterCpf').value.trim();
    if (cpf) {
        // Remove formatação e mantém apenas números
        const cleanCpf = cpf.replace(/\D/g, '');
        if (cleanCpf.length >= 3) { // Permite busca parcial
            currentFilters.cpf = cleanCpf;
            console.log('Filtro CPF aplicado:', cleanCpf);
        }
    }
    
    const status = document.getElementById('filterStatus').value;
    if (status) {
        currentFilters.status_saude = status;
        console.log('Filtro Status aplicado:', status);
    }
    
    currentLimit = parseInt(document.getElementById('filterLimit').value) || 10;
    
    console.log('Filtros aplicados:', currentFilters);
    loadRecords();
}

function updatePagination() {
    const paginationContainer = document.getElementById('paginationContainer');
    const totalPages = Math.ceil(totalRecords / currentLimit);
    
    if (totalPages <= 1) {
        paginationContainer.style.display = 'none';
        return;
    }
    
    paginationContainer.style.display = 'flex';
    
    let paginationHTML = '';
    
    paginationHTML += `
        <button ${currentPage === 0 ? 'disabled' : ''} onclick="changePage(${currentPage - 1})">
            <i class="fas fa-chevron-left"></i> Anterior
        </button>
    `;
    
    const startPage = Math.max(0, currentPage - 2);
    const endPage = Math.min(totalPages - 1, currentPage + 2);
    
    if (startPage > 0) {
        paginationHTML += `<button onclick="changePage(0)">1</button>`;
        if (startPage > 1) {
            paginationHTML += `<span>...</span>`;
        }
    }
    
    for (let i = startPage; i <= endPage; i++) {
        paginationHTML += `
            <button class="${i === currentPage ? 'active' : ''}" onclick="changePage(${i})">
                ${i + 1}
            </button>
        `;
    }
    
    if (endPage < totalPages - 1) {
        if (endPage < totalPages - 2) {
            paginationHTML += `<span>...</span>`;
        }
        paginationHTML += `<button onclick="changePage(${totalPages - 1})">${totalPages}</button>`;
    }
    
    paginationHTML += `
        <button ${currentPage >= totalPages - 1 ? 'disabled' : ''} onclick="changePage(${currentPage + 1})">
            Próximo <i class="fas fa-chevron-right"></i>
        </button>
    `;
    
    paginationContainer.innerHTML = paginationHTML;
}

function changePage(page) {
    currentPage = page;
    loadRecords();
}

function updateRecordCount() {
    const recordCount = document.getElementById('recordCount');
    const start = currentPage * currentLimit + 1;
    const end = Math.min((currentPage + 1) * currentLimit, totalRecords);
    
    recordCount.textContent = `Mostrando ${start}-${end} de ${totalRecords} registros`;
}

function showLoading() {
    const loadingMessage = document.getElementById('loadingMessage');
    const noRecordsMessage = document.getElementById('noRecordsMessage');
    const tableBody = document.getElementById('recordsTableBody');
    
    if (loadingMessage) loadingMessage.style.display = 'block';
    if (noRecordsMessage) noRecordsMessage.style.display = 'none';
    if (tableBody) tableBody.innerHTML = '';
}

function showNoRecords() {
    const loadingMessage = document.getElementById('loadingMessage');
    const noRecordsMessage = document.getElementById('noRecordsMessage');
    const tableBody = document.getElementById('recordsTableBody');
    const recordCount = document.getElementById('recordCount');
    
    if (loadingMessage) loadingMessage.style.display = 'none';
    if (noRecordsMessage) noRecordsMessage.style.display = 'block';
    if (tableBody) tableBody.innerHTML = '';
    if (recordCount) recordCount.textContent = 'Nenhum registro encontrado';
}

function showNotification(message, type = 'info') {
    console.log('Mostrando notificação:', message, type);
    
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${getNotificationIcon(type)}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close">
            <i class="fas fa-times"></i>
        </button>
    `;

    const container = document.getElementById('notifications');
    if (container) {
        container.appendChild(notification);
    } else {
        console.error('Container de notificações não encontrado');
    }

    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);

    notification.querySelector('.notification-close').addEventListener('click', () => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    });
}

function getNotificationIcon(type) {
    switch (type) {
        case 'success': return 'fa-check-circle';
        case 'error': return 'fa-exclamation-circle';
        case 'warning': return 'fa-exclamation-triangle';
        default: return 'fa-info-circle';
    }
}

// Função para formatar CPF
function formatCpf(cpf) {
    if (!cpf || cpf === '00000000000') return 'Não informado';
    
    // Remove caracteres não numéricos
    const cleanCpf = cpf.replace(/\D/g, '');
    
    // Verifica se tem 11 dígitos
    if (cleanCpf.length === 11) {
        return cleanCpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
    }
    
    // Se não tem 11 dígitos, retorna como está
    return cpf;
}

// Função para limpar filtros
function clearFilters() {
    document.getElementById('filterCpf').value = '';
    document.getElementById('filterStatus').value = '';
    document.getElementById('filterLimit').value = '10';
    
    currentFilters = {};
    currentPage = 0;
    currentLimit = 10;
    
    loadRecords();
}

// Função para busca rápida por CPF
function quickSearchCpf(cpf) {
    const filterCpfInput = document.getElementById('filterCpf');
    if (filterCpfInput) {
        filterCpfInput.value = cpf;
        applyFilters();
    }
}
