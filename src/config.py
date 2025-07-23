"""
Configurações do Sistema SAEV
"""
import os
from pathlib import Path
from typing import Dict, Any

class SAEVConfig:
    """Classe para gerenciar configurações do sistema SAEV"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.db_directory = self.project_root / "db"
        
        # Configurações dos bancos de dados
        self.databases = {
            "teste": {
                "name": "avaliacao_teste.db",
                "description": "Banco de teste com dados ofuscados (MD5)",
                "can_be_in_repo": True,
                "sample_data": True
            },
            "producao": {
                "name": "avaliacao_prod.db", 
                "description": "Banco de produção com dados reais",
                "can_be_in_repo": False,
                "sample_data": False
            }
        }
    
    def get_database_path(self, environment: str = None) -> str:
        """
        Retorna o caminho do banco de dados baseado no ambiente
        
        Args:
            environment: 'teste' ou 'producao'. Se None, detecta automaticamente
            
        Returns:
            String com o caminho completo do banco de dados
        """
        if environment is None:
            environment = self.detect_environment()
        
        if environment not in self.databases:
            raise ValueError(f"Ambiente '{environment}' não é válido. Use 'teste' ou 'producao'")
        
        db_name = self.databases[environment]["name"]
        db_path = self.db_directory / db_name
        
        return str(db_path)
    
    def detect_environment(self) -> str:
        """
        Detecta automaticamente qual ambiente usar baseado nos arquivos disponíveis
        
        Returns:
            'teste' ou 'producao'
        """
        prod_path = self.db_directory / self.databases["producao"]["name"]
        test_path = self.db_directory / self.databases["teste"]["name"]
        
        # Verificar variável de ambiente primeiro
        env_var = os.getenv('SAEV_ENVIRONMENT', '').lower()
        if env_var in ['teste', 'test']:
            return 'teste'
        elif env_var in ['producao', 'prod', 'production']:
            return 'producao'
        
        # Se produção existe, usar produção
        if prod_path.exists():
            return 'producao'
        
        # Caso contrário, usar teste
        return 'teste'
    
    def get_environment_info(self, environment: str = None) -> Dict[str, Any]:
        """
        Retorna informações sobre o ambiente
        
        Args:
            environment: 'teste' ou 'producao'. Se None, detecta automaticamente
            
        Returns:
            Dicionário com informações do ambiente
        """
        if environment is None:
            environment = self.detect_environment()
        
        db_path = self.get_database_path(environment)
        db_exists = Path(db_path).exists()
        
        info = {
            "environment": environment,
            "database_path": db_path,
            "database_exists": db_exists,
            "description": self.databases[environment]["description"],
            "can_be_in_repo": self.databases[environment]["can_be_in_repo"],
            "sample_data": self.databases[environment]["sample_data"]
        }
        
        if db_exists:
            # Adicionar informações do arquivo
            db_file = Path(db_path)
            info["file_size_mb"] = round(db_file.stat().st_size / (1024 * 1024), 2)
            info["last_modified"] = db_file.stat().st_mtime
        
        return info
    
    def list_available_environments(self) -> Dict[str, Dict[str, Any]]:
        """
        Lista todos os ambientes disponíveis com suas informações
        
        Returns:
            Dicionário com informações de todos os ambientes
        """
        environments = {}
        
        for env_name in self.databases.keys():
            try:
                environments[env_name] = self.get_environment_info(env_name)
            except Exception as e:
                environments[env_name] = {
                    "environment": env_name,
                    "error": str(e),
                    "database_exists": False
                }
        
        return environments
    
    def validate_environment(self, environment: str) -> tuple[bool, str]:
        """
        Valida se um ambiente é válido e utilizável
        
        Args:
            environment: Nome do ambiente a ser validado
            
        Returns:
            Tupla (é_válido, mensagem)
        """
        if environment not in self.databases:
            return False, f"Ambiente '{environment}' não existe. Ambientes válidos: {list(self.databases.keys())}"
        
        db_path = self.get_database_path(environment)
        
        if not Path(db_path).exists():
            return False, f"Banco de dados não encontrado em: {db_path}"
        
        return True, f"Ambiente '{environment}' válido e disponível"

# Instância global da configuração
config = SAEVConfig()
