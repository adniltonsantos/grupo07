# Projeto Grupo 32 - SENAC

## Tema do Projeto
O projeto tem como tema a análise comparativa da COVID-19 entre países. Buscando destacar a posição do Brasil em relação ao cenário internacional, avaliando indicadores de impacto, recuperação e crescimento da pandemia. Link do banco https://www.kaggle.com/datasets/imdevskp/corona-virus-report?resource=download

## Integrantes
- Adnilton Santos
- Adriano Limeira
- Vitor Silva
- Matheus Rocha
- Gabriela Astoni
- Joao Alencar
## Objetivo da Análise
O objetivo principal do projeto é analisar e comparar o impacto da COVID-19 entre diferentes países, com foco na identificação de padrões, avaliar a posição do Brasil em relação a outros países, identificar países com maior e menor impacto da pandemia, analisar indicadores de eficiência (recuperação vs mortalidade), explorar diferenças entre regiões globais (OMS) e detectar países com crescimento acelerado de casos.

## 📊 Planejamento das Tarefas

### 🔹 Tarefa 1 – Coleta e Preparação dos Dados
**Responsáveis:** Adriano Limeira + Adnilton Santos  

### Atividades:
- Buscar datasets confiáveis (Our World in Data, OMS, Kaggle)  
- Importar dados (CSV/API)  
- Limpar dados:
  - Remover inconsistências  
  - Tratar valores nulos  
  - Padronizar nomes de países/regiões  
- Criar colunas importantes:
  - Taxa de letalidade = mortes / casos  
  - Taxa de recuperação = recuperados / casos  
- Salvar dataset final tratado  

### Ferramentas:
- Python (pandas, numpy)  
- Jupyter Notebook / Google Colab  

---

## 🔹 Tarefa 2 – Análise Exploratória (EDA)
**Responsáveis:** Vitor Silva + Matheus Rocha  

### Atividades:
- Identificar:
  - Países com mais casos, mortes e recuperações  
  - Evolução da pandemia ao longo do tempo  
- Comparar:
  - Brasil vs mundo  
  - Brasil vs top 10 países  
- Analisar:
  - Crescimento de casos (diário/semanal)  
  - Diferenças entre regiões (OMS)  
- Gerar insights iniciais (texto para apresentação)  

### Ferramentas:
- Python (pandas, matplotlib, seaborn)  
- Jupyter Notebook  

---

## 🔹 Tarefa 3 – Construção do Dashboard
**Responsáveis:** Joao Alencar + Gabriela Copfield  

### Atividades:
- Definir ferramenta:
  - Python (Streamlit)  
- Criar visualizações:
  - Ranking de países  
  - Gráficos de linha (evolução)  
  - Comparação Brasil vs mundo  
  - Gráficos por região  
- Implementar filtros:
  - País  
  - Região  
  - Métricas  
- Destacar automaticamente o Brasil  

### Ferramentas:
**Opção recomendada:**
👉 Opção recomendada: Power BI (mais rápido)
👉 Diferencial: Python (Streamlit)

## Ideia Inicial do Dashboard
Queremos que o dashboard seja projetado para fornecer uma visão interativa e comparativa dos principais indicadores da COVID-19 em nível global, com destaque para o Brasil.  
Ranquear países por:  
-	Casos confirmados  
-	Mortes  
-	Casos ativos  
-	Letalidade (Deaths / Confirmed)  
-	Recuperação (Recovered / Confirmed)  
	  
Comparação do Brasil com:  
-	Média mundial  
-	Top 10 países mais afetados 
-	Taxa de letalidade  
-	Taxa de recuperação  
Comparação entre regiões:  
-	Média de casos  
-	Mortalidade  
-	Crescimento  
Se possível, poderíamos fazer dashboard para interação com usuário de maneira que ele possa:   
-	Filtrar por país  
-	Selecionar regiões da OMS  
-	Ordenar rankings por diferentes métricas  
-	Destacar o Brasil automaticamente nas visualizações  
-	Explorar comparações entre países  



---

**Data de criação:** 25 de fevereiro de 2026
