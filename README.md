# Mini Lakehouse Local - Medallion Architecture

Pipeline de dados *End-to-End* desenvolvido em Python, simulando a arquitetura de dados **Medallion (Bronze, Silver e Gold)** para ingestão, tratamento e agregação analítica de eventos de e-commerce.

---

#Arquitetura da Solução

O fluxo de dados foi construído seguindo o padrão moderno de Data Lakehouse:

```text
[ Origem (JSON) ] 
       │
       ▼
 [ 1_BRONZE ] ──► Raw Data (Auditabilidade & Ingestão Bruta)
       │
       ▼
 [ 2_SILVER ] ──► Cleaned Data (Deduplicação, Castings e Filtros em Parquet)
       │
       ▼
 [ 3_GOLD ]   ──► Aggregated Data (Visões de Negócio via DuckDB)