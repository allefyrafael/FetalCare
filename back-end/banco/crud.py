from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
from bson import ObjectId

from .database import get_collection
from .models import (
    RegistroExame, 
    RegistroExameCreate, 
    ResultadoML, 
    criar_saude_feto,
    determinar_status_saude
)

logger = logging.getLogger(__name__)

class RegistroExameCRUD:
    """Operações CRUD para registros de exames fetais"""
    
    def __init__(self):
        self._collection = None
    
    @property
    def collection(self):
        """Lazy loading da collection"""
        if self._collection is None:
            self._collection = get_collection()
        return self._collection
    
    async def criar_registro(
        self,
        dados_exame: RegistroExameCreate,
        resultado_ml: ResultadoML
    ) -> RegistroExame:
        """
        Cria um novo registro de exame
        
        Args:
            dados_exame: Dados do exame (gestante + parâmetros)
            resultado_ml: Resultado do modelo ML
            
        Returns:
            RegistroExame: Registro criado com ID
        """
        try:
            # Calcula status de saúde baseado na confidence
            saude_feto = criar_saude_feto(resultado_ml.confidence)
            
            # Monta o registro completo
            registro_data = {
                "dados_gestante": dados_exame.dados_gestante.model_dump(),
                "parametros_monitoramento": dados_exame.parametros_monitoramento.model_dump(),
                "resultado_ml": resultado_ml.model_dump(),
                "saude_feto": saude_feto.model_dump(),
                "data_exame": datetime.utcnow(),
                "medico_responsavel": dados_exame.medico_responsavel,
                "observacoes": dados_exame.observacoes
            }
            
            # Insere no banco
            result = await self.collection.insert_one(registro_data)
            
            # Busca o registro criado
            registro_criado = await self.collection.find_one({"_id": result.inserted_id})
            
            logger.info(f"✅ Registro criado com ID: {result.inserted_id}")
            logger.info(f"📊 Status saúde: {saude_feto.status_saude} (Confidence: {resultado_ml.confidence}%)")
            
            return RegistroExame(**registro_criado)
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar registro: {e}")
            raise
    
    async def buscar_todos_registros(
        self,
        skip: int = 0,
        limit: int = 100,
        ordenar_por: str = "data_exame",
        ordem_desc: bool = True
    ) -> List[RegistroExame]:
        """
        Busca todos os registros com paginação
        
        Args:
            skip: Quantos registros pular
            limit: Limite de registros por página
            ordenar_por: Campo para ordenação
            ordem_desc: Se True, ordem decrescente
            
        Returns:
            List[RegistroExame]: Lista de registros
        """
        try:
            ordem = -1 if ordem_desc else 1
            
            cursor = self.collection.find().sort(ordenar_por, ordem).skip(skip).limit(limit)
            registros = await cursor.to_list(length=limit)
            
            return [RegistroExame(**registro) for registro in registros]
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar registros: {e}")
            raise
    
    async def buscar_por_cpf(
        self,
        cpf: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[RegistroExame]:
        """
        Busca registros por CPF da gestante
        
        Args:
            cpf: CPF para busca
            skip: Quantos registros pular
            limit: Limite de registros
            
        Returns:
            List[RegistroExame]: Registros da gestante
        """
        try:
            # Remove caracteres especiais do CPF
            cpf_limpo = ''.join(filter(str.isdigit, cpf))
            
            filtro = {"dados_gestante.patient_cpf": {"$regex": cpf_limpo}}
            
            cursor = self.collection.find(filtro).sort("data_exame", -1).skip(skip).limit(limit)
            registros = await cursor.to_list(length=limit)
            
            logger.info(f"🔍 Encontrados {len(registros)} registros para CPF: {cpf}")
            
            return [RegistroExame(**registro) for registro in registros]
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar por CPF: {e}")
            raise
    
    async def buscar_por_id(self, registro_id: str) -> Optional[RegistroExame]:
        """
        Busca registro por ID
        
        Args:
            registro_id: ID do registro
            
        Returns:
            RegistroExame: Registro encontrado ou None
        """
        try:
            if not ObjectId.is_valid(registro_id):
                return None
                
            registro = await self.collection.find_one({"_id": ObjectId(registro_id)})
            
            if registro:
                return RegistroExame(**registro)
            return None
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar por ID: {e}")
            raise
    
    async def buscar_por_status_saude(
        self,
        status: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[RegistroExame]:
        """
        Busca registros por status de saúde
        
        Args:
            status: Status de saúde (Normal, Em Risco, Risco Crítico)
            skip: Quantos registros pular
            limit: Limite de registros
            
        Returns:
            List[RegistroExame]: Registros com o status especificado
        """
        try:
            filtro = {"saude_feto.status_saude": status}
            
            cursor = self.collection.find(filtro).sort("data_exame", -1).skip(skip).limit(limit)
            registros = await cursor.to_list(length=limit)
            
            return [RegistroExame(**registro) for registro in registros]
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar por status: {e}")
            raise
    
    async def atualizar_registro(
        self,
        registro_id: str,
        dados_atualizacao: Dict[str, Any]
    ) -> Optional[RegistroExame]:
        """
        Atualiza um registro existente
        
        Args:
            registro_id: ID do registro
            dados_atualizacao: Dados para atualizar
            
        Returns:
            RegistroExame: Registro atualizado ou None
        """
        try:
            if not ObjectId.is_valid(registro_id):
                return None
            
            # Adiciona timestamp de última atualização
            dados_atualizacao["ultima_atualizacao"] = datetime.utcnow()
            
            result = await self.collection.update_one(
                {"_id": ObjectId(registro_id)},
                {"$set": dados_atualizacao}
            )
            
            if result.modified_count > 0:
                return await self.buscar_por_id(registro_id)
            return None
            
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar registro: {e}")
            raise
    
    async def deletar_registro(self, registro_id: str) -> bool:
        """
        Deleta um registro
        
        Args:
            registro_id: ID do registro
            
        Returns:
            bool: True se deletado com sucesso
        """
        try:
            if not ObjectId.is_valid(registro_id):
                return False
            
            result = await self.collection.delete_one({"_id": ObjectId(registro_id)})
            
            if result.deleted_count > 0:
                logger.info(f"🗑️ Registro {registro_id} deletado com sucesso")
                return True
            return False
            
        except Exception as e:
            logger.error(f"❌ Erro ao deletar registro: {e}")
            raise
    
    async def contar_registros(self, filtro: Dict[str, Any] = None) -> int:
        """
        Conta registros no banco
        
        Args:
            filtro: Filtro opcional para contagem
            
        Returns:
            int: Número de registros
        """
        try:
            if filtro is None:
                filtro = {}
            
            return await self.collection.count_documents(filtro)
            
        except Exception as e:
            logger.error(f"❌ Erro ao contar registros: {e}")
            raise
    
    async def obter_estatisticas(self) -> Dict[str, Any]:
        """
        Obtém estatísticas dos registros
        
        Returns:
            Dict: Estatísticas do banco
        """
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$saude_feto.status_saude",
                        "count": {"$sum": 1},
                        "confidence_media": {"$avg": "$saude_feto.confidence_value"}
                    }
                }
            ]
            
            stats = await self.collection.aggregate(pipeline).to_list(length=None)
            
            total_registros = await self.contar_registros()
            
            return {
                "total_registros": total_registros,
                "distribuicao_status": stats,
                "ultima_atualizacao": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao obter estatísticas: {e}")
            raise

# Instância global para uso nas rotas - será inicializada quando necessário
crud = RegistroExameCRUD() 