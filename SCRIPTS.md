# Scripts Shell para SAEV Dashboard

Este documento descreve os scripts shell criados para facilitar a execução do SAEV Dashboard.

## 📜 Scripts Disponíveis

### 1. `iniciar.sh` - Script Principal Interativo

**Descrição**: Menu interativo colorido para escolher e gerenciar ambientes.

**Uso**: `./iniciar.sh`

**Funcionalidades**:
- 🎨 Interface visual com banner ASCII
- 📊 Verificação automática de status dos ambientes
- 🎯 Menu de opções numeradas
- 🛠️ Ferramentas de configuração integradas
- 💡 Ajuda e documentação incluída

**Opções do Menu**:
1. Iniciar ambiente de TESTE
2. Iniciar ambiente de PRODUÇÃO
3. Verificar status detalhado
4. Configurar ambiente de teste
5. Mostrar ajuda dos scripts
6. Sair

### 2. `iniciar_teste.sh` - Ambiente de Teste

**Descrição**: Execução direta do dashboard no ambiente de teste.

**Uso**: `./iniciar_teste.sh [porta]`

**Características**:
- 🧪 Ambiente seguro com dados ofuscados (MD5)
- ✅ Auto-configuração se o banco não existir
- 🟢 Execução direta sem confirmação
- 🔧 Criação automática da estrutura do banco
- 📁 Usa: `db/avaliacao_teste.db`

**Validações**:
- ✓ Verifica se Python está instalado
- ✓ Verifica se Streamlit está disponível
- ✓ Valida a porta especificada
- ✓ Cria estrutura do banco se necessário
- ✓ Valida ambiente antes da execução

**Exemplos**:
```bash
./iniciar_teste.sh          # Porta padrão (8501)
./iniciar_teste.sh 8502     # Porta customizada
```

### 3. `iniciar_prod.sh` - Ambiente de Produção

**Descrição**: Execução do dashboard no ambiente de produção com medidas de segurança.

**Uso**: `./iniciar_prod.sh [porta]`

**Características**:
- 🔴 Ambiente com dados reais e sensíveis
- ⚠️ Requer confirmação explícita do usuário
- 🔐 Validações rigorosas de segurança
- 🛡️ Verificações de integridade obrigatórias
- 📁 Usa: `db/avaliacao_prod.db`

**Medidas de Segurança**:
- 🚨 Banner de alerta vermelho
- 🔍 Verificação obrigatória do banco de produção
- 💬 Confirmação manual (digite "SIM")
- 🛡️ Validação completa do ambiente
- ⚠️ Avisos sobre dados sensíveis

**Exemplos**:
```bash
./iniciar_prod.sh           # Porta padrão (8501)
./iniciar_prod.sh 8503      # Porta customizada
```

## 🔧 Funcionalidades Comuns

### Validações Automáticas

Todos os scripts incluem:
- ✓ Verificação do diretório de execução
- ✓ Validação da instalação do Python
- ✓ Verificação da disponibilidade do Streamlit
- ✓ Validação de portas (1024-65535)
- ✓ Verificação de permissões de execução

### Tratamento de Erros

- 🔍 Detecção automática de problemas
- 💡 Sugestões de solução incluídas
- 🎨 Mensagens coloridas para melhor visibilidade
- 📋 Códigos de saída apropriados

### Compatibilidade

- 🐧 Linux
- 🍎 macOS  
- 🖥️ WSL no Windows
- 🐚 Bash/Zsh compatível

## 🎨 Códigos de Cores

Os scripts usam cores ANSI para melhor experiência:

- 🔴 **Vermelho**: Erros, produção, alertas críticos
- 🟢 **Verde**: Sucesso, confirmações, teste
- 🟡 **Amarelo**: Avisos, informações importantes
- 🔵 **Azul**: Informações gerais, ajuda
- 🟣 **Roxo**: Banner principal, destaque
- 🟦 **Ciano**: Ambiente de teste, elementos secundários

## 🚨 Troubleshooting

### Problema: "Permission denied"
**Solução**: `chmod +x *.sh`

### Problema: "Python not found"
**Solução**: Instalar Python 3.8+ ou verificar PATH

### Problema: "Streamlit not installed"
**Solução**: `pip install -r requirements.txt`

### Problema: "Database not found"
**Solução**: Executar script de carga apropriado

### Problema: "Invalid port"
**Solução**: Usar porta entre 1024-65535

## 📞 Suporte

Para problemas ou dúvidas:
1. Execute `./iniciar.sh` e escolha opção 5 (ajuda)
2. Execute `python manage_env.py status` para diagnóstico
3. Verifique logs de erro exibidos pelos scripts
4. Consulte a documentação principal no README.md
