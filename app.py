from pathlib import Path
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Dashboard Cotação Dólar | Mini Lakehouse",
    layout="wide",
)

st.title("Dashboard de Cotação do Dólar (USD/BRL)")
st.markdown(
    "Exibindo dados processados da **Camada Gold** da arquitetura Medallion."
)

gold_path = Path("data/3_gold/usd_metrics.parquet")

if not gold_path.exists():
  st.error(
      "O arquivo da Camada Gold não foi encontrado. Execute o `main.py`"
      " primeiro!"
  )
else:
  # Leitura do Parquet da Camada Gold
  df = pd.read_parquet(gold_path)
  df["dt_cotacao"] = pd.to_datetime(df["dt_cotacao"])
  df = df.sort_values(by="dt_cotacao", ascending=True)

  # KPI Cards (Métricas Principais)
  col1, col2, col3, col4 = st.columns(4)

  ultima_cotacao = df["cotacao_usd"].iloc[-1]
  cotacao_anterior = (
      df["cotacao_usd"].iloc[-2] if len(df) > 1 else ultima_cotacao
  )
  variacao = ((ultima_cotacao - cotacao_anterior) / cotacao_anterior) * 100

  max_periodo = df["cotacao_usd"].max()
  min_periodo = df["cotacao_usd"].min()
  media_periodo = df["cotacao_usd"].mean()

  col1.metric("Última Cotação", f"R$ {ultima_cotacao:.4f}", f"{variacao:+.2f}%")
  col2.metric("Média do Período", f"R$ {media_periodo:.4f}")
  col3.metric("Máxima no Período", f"R$ {max_periodo:.4f}")
  col4.metric("Mínima no Período", f"R$ {min_periodo:.4f}")

  st.markdown("---")

  # Gráfico Interativo de Cotação + Média Móvel
  st.subheader("Histórico de Cotação e Média Móvel (7 Dias)")

  fig = go.Figure()
  fig.add_trace(
      go.Scatter(
          x=df["dt_cotacao"],
          y=df["cotacao_usd"],
          mode="lines+markers",
          name="Cotação Diária (USD)",
          line=dict(color="#1f77b4", width=2),
      )
  )
  fig.add_trace(
      go.Scatter(
          x=df["dt_cotacao"],
          y=df["media_movel_7d"],
          mode="lines",
          name="Média Móvel (7 Dias)",
          line=dict(color="#ff7f0e", width=2, dash="dash"),
      )
  )

  fig.update_layout(
      xaxis_title="Data",
      yaxis_title="Valor (R$)",
      hovermode="x unified",
      template="plotly_white",
      margin=dict(l=20, r=20, t=30, b=20),
  )

  st.plotly_chart(fig, use_container_width=True)

  # Tabela com visualização dos dados brutos da Gold
  with st.expander("Visualizar Tabela de Dados (Camada Gold)"):
    st.dataframe(
        df.sort_values(by="dt_cotacao", ascending=False),
        use_container_width=True,
    )