# Requisitos Funcionais

## RF1 - Importação e Estruturação de Dados
**ID Base:** RF1-DATA

### RF1-DATA-INGEST - Ingestão de Dados Regulatórios
- O sistema deve consumir arquivos CSV e Geodatabase compactados (ZIP) provenientes da ANEEL (BDGD, DEC, FEC e Perdas).
- O sistema deve processar os dados dos arquivos, realizando limpeza e validação das colunas obrigatórias para os cálculos.
- O sistema deve armazenar os dados processados no MongoDB.

---

## RF2 - Análise de Mercado e Criticidade
**ID Base:** RF2-ANALYTICS

### RF2-ANALYTICS-TAM - Dimensionamento Físico (TAM)
- O sistema deve calcular a extensão das linhas de Média Tensão para identificar a potencialidade de mercado dos sensores da Tecsys.

### RF2-ANALYTICS-PERD - Análise Comparativa Perdas
- O sistema deve ranquear os conjuntos elétricos cruzando dados de DEC, FEC e limites regulatórios.
- O sistema deve comparar visualmente (em MWh) as perdas técnicas e não técnicas.

### RF2-ANALYTICS-SAM - Índice de Potencial de Sensoriamento (SAM)
- O sistema deve cruzar os dados de extensão de rede, criticidade e presença de religadores para qualificar e ranquear as regiões com maior potencial de prioridade para instalação de sensores.

### RF2-ANALYTICS-CRIT - Cálculo e Visualização de Criticidade e Perdas
- O sistema deve calcular e ranquear os conjuntos elétricos cruzando dados de DEC, FEC e limites regulatórios da ANEEL.
- O sistema deve exibir uma tabela (ou gráfico) de classificação listando os conjuntos elétricos ordenados do mais crítico (pior eficiência) para o menos crítico.

---

## RF3 - Motor Preditivo e Inteligência Artificial
**ID Base:** RF3-PREDICT

### RF3-PREDICT-API - API de Aconselhamento (Machine Learning)
- O sistema deve possuir uma API dedicada para execução do modelo preditivo.

---

## RF4 - Visualização Georreferenciada (GIS)
**ID Base:** RF4-MAPS

### RF4-MAPS-HEATMAP - Mapas de Calor e Polígonos
- O sistema deve renderizar um mapa georreferenciado, colorindo os segmentos de rede com base no Índice de Criticidade.

---

## RF5 - Gestão de Usuários e Autenticação
**ID Base:** RF5-AUTH

### RF5-AUTH-CRUD - Criação de Conta e Login
- O sistema deve permitir que usuários criem suas próprias contas de forma autônoma.
- O sistema deve autenticar usuários via e-mail e senha criptografada.
- O sistema deve permitir a edição de dados básicos e exclusão da conta.
- *Nota de Arquitetura:* Todos os dados de usuários e credenciais devem ser armazenados no banco de dados relacional (legado), compondo a parte estruturada da arquitetura híbrida.
---

# Requisitos Não Funcionais

## RNF1 - Documentação Obrigatória do Projeto
**ID Base:** RNF1-DOCS

### RNF1-DOCS-USER - Manuais de Instalação
- A equipe deve elaborar um Manual de Instalação do sistema.
- A equipe deve elaborar um Manual do Usuário detalhando o uso das funcionalidades.

### RNF1-DOCS-TECH - Documentação Técnica
- A equipe deve fornecer a documentação da API (Application Programming Interface), contendo os endpoints.

---

## RNF2 - Arquitetura de Banco de Dados
**ID Base:** RNF2-DATA

### RNF2-DATA-BASE - Modelagem de Banco de Dados
- A equipe deve entregar a modelagem de banco de dados ou a estrutura dos arquivos de dados.

### RNF2-DATA-TESTS - Integridade de Dados
- O sistema deve possuir testes automatizados básicos para validar a integridade do banco de dados.

---

## RNF3 - Conformidade LGPD e Segurança
**ID Base:** RNF3-SEC

### RNF3-SEC-LGPD - Privacidade e Anonimização
- O sistema deve adicionar regras de conformidade com a LGPD.
- O sistema deve implementar rotinas de anonimização de dados pessoais em caso de exclusão de conta, conforme exigido pela LGPD.

### RNF3-SEC-AUDIT - Rastreabilidade (Logs)
- O sistema deve realizar o registro obrigatório de logs de acesso.
- O sistema deve registrar detalhadamente logs de manipulação de dados em uma tabela de auditoria.

---

## RF6 - Relatórios e Exportação de Dados
**ID Base:** RF6-EXPORT

### RF6-EXPORT-PDF - Geração de Proposta Comercial em PDF
- O sistema deve permitir a exportação das análises geradas (dashboards) para um documento em formato PDF.
- O PDF gerado deve consolidar as informações de forma estruturada, servindo como um relatório técnico/comercial pronto para ser entregue à concessionária.
