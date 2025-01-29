# **Documentação do Microserviço de Registro de Histórico de Solicitações**  
Este documento descreve o fluxo de funcionamento do microserviço responsável por receber mensagens de um RabbitMQ e registrar no banco de dados PostgreSQL o histórico das solicitações, incluindo informações como status, origem do bucket S3, data e hora, entre outros detalhes relevantes.

---

### **Visão Geral do Sistema**  
O sistema monitora e registra eventos recebidos via RabbitMQ em um banco de dados PostgreSQL. Ele captura informações de solicitações processadas por outros serviços, armazena o histórico detalhado e fornece uma base confiável para auditorias, análises e rastreamento de falhas.

---

### **Objetivo do Microserviço**  
O microserviço é responsável por:  

1. **Receber Mensagens do RabbitMQ**:  
   Consumir mensagens de uma fila configurada no RabbitMQ, representando solicitações de processamento realizadas por outros serviços.  

2. **Registrar Informações no PostgreSQL**:  
   Salvar no banco de dados informações detalhadas sobre cada solicitação, incluindo:  
   - Nome do vídeo  
   - Origem do bucket S3  
   - Data e hora do evento  
   - Identificador único (ID) da solicitação  
   - Status da solicitação (sucesso, criado, falha, etc.)  

3. **Gerar Log para Monitoramento**:  
   Registrar logs para facilitar a depuração e o rastreamento de mensagens processadas.  

---

### **Fluxo de Funcionamento**  

#### **Recepção de Mensagem**  
1. O microserviço se conecta a uma fila no RabbitMQ (ex.: `queue-requests-log`).  
2. Consome mensagens contendo detalhes das solicitações realizadas por outros serviços.  
3. A mensagem deve conter os seguintes campos:  
   - ID da solicitação  
   - Nome do vídeo  
   - Origem do bucket S3  
   - Data e hora do evento  
   - Status da solicitação  

#### **Processamento e Persistência**  
1. A mensagem recebida é processada e validada.  
2. Os dados são inseridos em uma tabela do PostgreSQL chamada `requests_history`.  
3. O registro no banco deve conter os seguintes campos:  
   - **id**: Identificador único da solicitação  
   - **video_name**: Nome do vídeo  
   - **bucket_origin**: Origem do bucket S3  
   - **timestamp**: Data e hora do evento  
   - **status**: Status da solicitação (sucesso, falha, criado, etc.)  

#### **Geração de Log**  
1. Após o registro no banco, um log é gerado para indicar o sucesso ou falha no processamento da mensagem.  

---

### **Integrações e Dependências**  

1. **RabbitMQ**  
   - Fila de mensagens configurada para consumo.  
   - Garantia de que todas as mensagens sejam processadas em ordem (se necessário).  

2. **PostgreSQL**  
   - Armazenamento de histórico das solicitações.  
   - Estrutura de tabelas bem definida para suportar consultas eficientes.  

---

### **Tecnologias e Ferramentas Utilizadas**  
- **Linguagem**: Python, Node.js ou .NET Core  
- **Banco de Dados**: PostgreSQL  
- **Mensageria**: RabbitMQ  
- **Orquestração**: Kubernetes (AWS EKS, opcional)  

---

### **Regras de Negócio e Pontos Críticos**  

1. **Validação das Mensagens**  
   Garantir que as mensagens recebidas contenham todos os campos obrigatórios antes de processá-las.  

2. **Persistência no Banco**  
   Garantir que os dados sejam salvos de forma consistente no PostgreSQL, utilizando transações para evitar corrupção de dados.  

3. **Resiliência e Retry**  
   Implementar lógica de retry para mensagens que não puderam ser processadas devido a falhas temporárias (ex.: conexão com o banco ou RabbitMQ).  

4. **Gerenciamento de Erros**  
   Manter logs detalhados sobre mensagens que falharam e não puderam ser processadas.  

---

### **Estrutura do Projeto**  

#### **Estrutura de Diretórios**  
```plaintext
ms-loghistory-app/
├── src/
│   ├── application/
│   │   ├── ports/
│   │   │   ├── MessageConsumerPort.cs
│   │   │   ├── DatabasePort.cs
│   │   │   └── LoggingPort.cs
│   │   └── usecases/
│   │       ├── ProcessMessageUseCase.cs
│   │       └── SaveRequestLogUseCase.cs
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── RequestLog.cs
│   │   ├── exceptions/
│   │   │   └── LogProcessingException.cs
│   │   └── services/
│   │       └── LogProcessingService.cs
│   ├── infrastructure/
│   │   ├── adapters/
│   │   │   ├── RabbitMqConsumerAdapter.cs
│   │   │   ├── PostgreSQLAdapter.cs
│   │   │   └── LoggingAdapter.cs
│   │   ├── configuration/
│   │   │   ├── DependencyInjectionConfig.cs
│   │   │   └── AppSettings.json
│   │   └── framework/
│   │       └── KubernetesWorkerService.cs
│   ├── api/
│   │   └── RequestLogController.cs
│   └── Program.cs
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
├── kubernetes/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── hpa.yaml
└── README.md
```

---

### **Detalhamento do Fluxo de Trabalho**  

1. **Recepção de Mensagem**:  
   O caso de uso `ProcessMessageUseCase` é acionado ao consumir uma mensagem do RabbitMQ.  

2. **Validação e Processamento**:  
   - `LogProcessingService` valida a mensagem.  
   - `SaveRequestLogUseCase` grava as informações no PostgreSQL.  

3. **Registro de Log**:  
   - `LoggingPort` gera logs para monitoramento.  

4. **Manuseio de Erros**:  
   - Mensagens inválidas ou falhas de persistência são registradas para depuração posterior.  

--- 

Esta estrutura garante robustez, rastreabilidade e escalabilidade para o microserviço. Se precisar de mais detalhes ou ajustes, é só avisar!
