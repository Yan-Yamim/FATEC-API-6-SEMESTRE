<h1 align="center">
API 6º Semestre Banco de Dados
<br/>
Thunderstone
</h1>

<h3 align="center">
  <img src="docs/img/logo-pokemon.png" alt="logo" width="30" style="vertical-align: middle;"> Equipe Pokémon
</h3>

<p align="center">
  | <a href ="#desafio"> Desafio</a>  |
  <a href ="#solucao"> Solução</a>  |   
  <a href ="#backlog"> Backlog do Produto</a>  |
  <a href ="#dor">DoR</a>  |
  <a href ="#dod">DoD</a>  |
  <a href ="#padroes"> Padrões do Projeto</a>  |
  <a href ="#sprint"> Cronograma de Sprints</a>  |
  <a href ="#tecnologias">Tecnologias</a> |
  <a href ="#equipe"> Equipe</a> |
</p>

> Status do Projeto: Em execução 
>
> Pasta de Documentação: [docs](docs)
> 
> Video do Projeto: 🚧

## 🏅 Desafio <a id="desafio"></a>

Dimensionar o sistema de distribuição de energia para viabilizar a expansão das tecnologias de telemetria da Tecsys. O obstáculo central a ser superado é a padronização dos cálculos e a alta complexidade no tratamento do vasto volume de dados da ANEEL.

## 🏅 Solução <a id="solucao"></a>

A solução consiste no desenvolvimento de uma plataforma capaz de processar os dados massivos e desestruturados da ANEEL e padronizar o cálculo de perdas. O sistema traduz esses dados em visualizações estratégicas, como mapas de calor e rankings, que destacam geograficamente os trechos mais precários da rede elétrica.

---

## 📋 Backlog do Produto <a id="backlog"></a>

| Rank | Prioridade | User Story | Story Points | Sprint | Requisito do Cliente | Status |
| :--: | :--------: | ---------- | :----------: | :----: | :------------------: | :----: |
| 1 |  Alta | Como um consultor comercial/técnico da Tecsys, eu quero visualizar uma tabela de classificação calculando o Índice de Criticidade (desvio percentual de DEC e FEC com base nos limites da ANEEL) de cada conjunto elétrico, para que eu possa identificar e priorizar rapidamente quais regiões possuem a pior eficiência estrutural. | 18 | 1 | [`RF1-DATA-INGEST`](process/requisitos.md#rf1-data-ingest---ingestão-de-dados-regulatórios)<br>[`RF2-ANALYTICS-CRIT`](process/requisitos.md#rf2-analytics-crit---cálculo-de-criticidade-e-perdas) | ✅|
| 2 |  Alta | Como um membro do time comercial/técnico, eu quero visualizar um gráfico de barras ordenado pelos conjuntos elétricos com maior índice SAM, para que eu saiba rapidamente quais regiões têm prioridade máxima de implantação de sensores. | 10 | 1 |  [`RF1-DATA-INGEST`](process/requisitos.md#rf1-data-ingest---ingestão-de-dados-regulatórios)<br>[`RF2-ANALYTICS-CRIT`](process/requisitos.md#rf2-analytics-crit---cálculo-de-criticidade-e-perdas) | ✅ |
| 3 |  Alta | Como um membro do time comercial/técnico, eu quero visualizar um gráfico de barras empilhadas que compare o volume absoluto (em MWh) das Perdas Técnicas (PT) e Não Técnicas (PNT) de cada conjunto elétrico, para evidenciar a magnitude das falhas estruturais da rede. | 10 |1  |  [`RF1-DATA-INGEST`](process/requisitos.md#rf1-data-ingest---ingestão-de-dados-regulatórios)<br>[`RF2-ANALYTICS-CRIT`](process/requisitos.md#rf2-analytics-crit---cálculo-de-criticidade-e-perdas) |✅ |
| 4 |  Alta | Como um consultor comercial/técnico da Tecsys, eu quero visualizar um ranking com os 10 conjuntos elétricos com maior extensão de média tensão (TAM), para demonstrar os pontos de maior vulnerabilidade operacional. | 12 | 1 | [`RF1-DATA-INGEST`](process/requisitos.md#rf1-data-ingest---ingestão-de-dados-regulatórios)<br>[`RF2-ANALYTICS-TAM`](process/requisitos.md#rf2-analytics-tam---dimensionamento-físico-tam) | ✅ |
| 5 |  Média | Como um consultor comercial/técnico da Tecsys, eu quero visualizar um mapa de calor georreferenciado indicando os circuitos mais críticos com base no Índice de Criticidade, para justificar investimentos em sensores inteligentes. | 8 | 2 | [`RF4-MAPS-HEATMAP`](process/requisitos.md#rf4-maps-heatmap---mapas-de-calor-e-polígonos) | ✅|
| 6 |  Média | Como um consultor comercial da Tecsys, Eu quero gerar automaticamente a análise completa de uma distribuidora selecionada, Para que eu possa preparar e conduzir apresentações comerciais com autonomia, em que eu precise entender ou interagir com nenhuma etapa técnica do processo. |  | 2 | [`RF1-DATA-INGEST`](process/requisitos.md#rf1-data-ingest---ingestão-de-dados-regulatórios)<br>[`RF2-ANALYTICS-CRIT`](process/requisitos.md#rf2-analytics-crit---cálculo-de-criticidade-e-perdas) |  |
| 7 |  Média | Como consultor de vendas da Tecsys, Eu quero que o sistema gere automaticamente um relatório em PDF consolidando os gráficos de SAM, PT/PNT, TAM, Índice de Criticidade e Mapa de Calor assim que os cálculos forem concluídos, Para que eu tenha o material de apresentação pronto sem nenhuma ação manual, podendo focar na abordagem comercial com o engenheiro da concessionária. |  | 2 | [`RF6-EXPORT-PDF`](process/requisitos.md#rf6-export-pdf---geração-de-proposta-comercial-em-pdf) |  |
| 8 |  Média | Como consultor de vendas da Tecsys, Eu quero ter acesso exclusivo e seguro à plataforma usando minhas credenciais corporativas, Para que apenas membros autenticados do time consigam visualizar as análises e relatórios estratégicos, e eu possa gerenciar minha conta com total autonomia, sem depender de suporte técnico. |  | 2 | [`RF5-AUTH-CRUD`](process/requisitos.md#rf5-auth-crud---criação-de-conta-e-login) |  |
| 9 |  Média | Como consultor de vendas da Tecsys, Eu quero enviar o relatório em PDF gerado pela plataforma diretamente para um e-mail de minha escolha com meu endereço corporativo já sugerido, Para que eu possa ter acesso ao material de apresentação. |  | 2 | [`RF6-EXPORT-PDF`](process/requisitos.md#rf6-export-pdf---geração-de-proposta-comercial-em-pdf) |  |
| 10 |  Baixa | Como um consultor cadastrado, Eu quero ter a clareza e a garantia de que minhas informações pessoais estão blindadas e serão usadas única e exclusivamente para o funcionamento da plataforma, Para que tenha a segurança de que a minha privacidade está sendo totalmente respeitada. |  | 3 | [`RNF3-SEC-LGPD`](process/requisitos.md#rnf3-sec-lgpd---privacidade-e-anonimização) |  |
| 11 |  Baixa | Como gestor da Tecsys, Eu quero ter um histórico claro de quem acessou, gerou, alterou ou excluiu informações dentro da plataforma, Para que eu possa entender exatamente o que aconteceu em caso de erros, auditorias ou comportamentos suspeitos, garantindo a proteção do nosso negócio. |  | 3 | [`RNF3-SEC-AUDIT`](process/requisitos.md#rnf3-sec-audit---rastreabilidade-logs) |  |
| 12 |  Baixa | Como consultor técnico da Tecsys, Eu quero que a plataforma identifique tendências e preveja quais trechos deverá possuir maior risco de sofrer apagões e multas no futuro, Para que eu possa vender os sensores como solução preventiva, ajudando o cliente a agir antes que o problema e o prejuízo aconteçam.|  | 3  | [`RF3-PREDICT-API`](process/requisitos.md#rf3-predict-api---api-de-aconselhamento-machine-learning) |  |
---

## 🏃‍ DoR - Definition of Ready
<a id="dor"></a>

Uma User Story será considerada **pronta para desenvolvimento** quando atender aos seguintes critérios:

- A história possui a narrativa estruturada no formato padrão ("Como um... Eu quero... Para que...")
- O tamanho da tarefa é viável, podendo ser codificada, testada e entregue dentro de um ciclo único de Sprint.
- Os cenários de uso (Caminho Feliz) estão descritos passo a passo.
- Os requisitos não funcionais específicos daquela entrega, como regras de LGPD, geração de logs de auditoria ou tempo de resposta, estão explícitos nos critérios.
- Caso a história impacte na interface visual, o protótipo, wireframe ou esboço da tela está anexado. 
> Todos os critérios de aceite e detalhamentos das User Stories podem ser verificados no Confluence: [Acessar US's no Confluence](https://jeanroodrigues.atlassian.net/wiki/spaces/~611d654d4016870069296c0d/folder/20742146?atlOrigin=eyJpIjoiOGRhY2I4NzRjMWVlNDEyYzk0YTc1ZDg0OGE5MDFhYWQiLCJwIjoiYyJ9)


## 🏆 DoD - Definition of Done <a id="dod"></a>

* Manual de Usuário
* Manual da Aplicação
* Documentação da API (Application Programming Interface)
* Código completo
* Vídeos de cada etapa de entrega

---
## 📖 Padrões do Projeto <a id="padroes"></a>

Nossos padrões de versionamento — incluindo **padrões de commits, Pull Requests (PR) e convenção de nomenclatura de branches** — ficam centralizados em nossa plataforma Confluence. Para consultar os guias, regras ou buscar alinhamento sobre as práticas do time, acesse o link:

> 🔗 **[Acessar Padrões de Commit, PR e Branch no Confluence](https://jeanroodrigues.atlassian.net/wiki/x/BID5)**

---

## 📅 Cronograma de Sprints <a id="sprint"></a>

| Sprint          |    Período    | Documentação                                     | Vídeo Entrega                                     |
| --------------- | :-----------: | ------------------------------------------------ | ------------------------------------------------ |
| 🔖 **SPRINT 1** | 16/03 - 05/04 |[doc](https://github.com/c137santos/FATEC-API-6-SEMESTRE/blob/main/process/sprints-backlog/sprint-1.md)| [video](https://drive.google.com/file/d/14Rk7tpzycikkkxXpeZZ4nF5BHbvCanvW/view?usp=drive_link)
| 🔖 **SPRINT 2** | 13/04 - 03/05 |🚧|🚧|
| 🔖 **SPRINT 3** | 11/05 - 31/05 |🚧 | 🚧 |

---

## 💻 Tecnologias <a id="tecnologias"></a>

<div align="">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D" alt="Vue.js" />
  <img src="https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/DBeaver-382923?style=for-the-badge&logo=dbeaver&logoColor=white" alt="DBeaver" />
  <img src="https://img.shields.io/badge/Google_Colab-F9AB00?style=for-the-badge&logo=googlecolab&color=525252" alt="Google Colab" />
</div>

---

## 🎓 Equipe <a id="equipe"></a>

<div align="center">
  <table>
    <tr>
      <th>Membro</th>
      <th>Função</th>
      <th>Github</th>
      <th>Linkedin</th>
    </tr>
    <tr>
      <td>Jean Rodrigues</td>
      <td>Scrum Master</td>
      <td><a href="https://github.com/JeanRodrigues1"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/jean-rodrigues-0569a0251/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Paloma Soares</td>
      <td>Product Owner</td>
      <td><a href="https://github.com/PalomaSoaresR"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/paloma-soares-rocha/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Isaque de Souza</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/Isaque-BD"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/isaque-souza-6760b8270/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Marília Moraes</td>
      <td>Desenvolvedora</td>
      <td><a href="https://github.com/marilia-borgo"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/mariliaborgo/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Maria Clara Santos</td>
      <td>Desenvolvedora</td>
      <td><a href="https://github.com/c137santos"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/c137santos/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Yan Yamim</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/YanYamim"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/yan-yamim-185220278/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
  </table>
</div>

---


