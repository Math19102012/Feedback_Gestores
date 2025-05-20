import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

st.set_page_config(page_title="Análise de Competências", layout="wide")
st.title("📈 Análise de Competências por Curso - FECAP")

# Carregar a base consolidada exportada do notebook
df_completo = pd.read_excel("data/df_completo_avaliacoes.xlsx")


# Filtrar registros válidos
df_validos = df_completo[df_completo['Curso (Matricula Atual) (Matricula)'].notna()].copy()

# Lista de competências esperadas
competencias = [
    "Conhecimentos", "Habilidades tecnicas", "Relacionamentos e parcerias",
    "Comunicação verbal e escrita", "Foco no cliente", "Gerenciamento do trabalho",
    "Orientação para resultados", "Aprendizagem pessoal"
]

# Preparar dados longos para visualização
df_validos['Curso (Matricula Atual) (Matricula)'] = df_validos['Curso (Matricula Atual) (Matricula)'].astype(str)
df_long = pd.melt(df_validos, id_vars=['RA', 'Curso (Matricula Atual) (Matricula)', 'Modelo'], value_vars=competencias,
                  var_name='Competência', value_name='Nota')
df_long['Nota'] = df_long['Nota'].astype(str)

# Filtro lateral
curso_sel = st.sidebar.selectbox("Selecione o curso:", sorted(df_validos['Curso (Matricula Atual) (Matricula)'].unique()))

# Gráfico 1 - Distribuição por curso
st.subheader("Distribuição de Alunos por Curso")
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.countplot(data=df_validos, y='Curso (Matricula Atual) (Matricula)', order=df_validos['Curso (Matricula Atual) (Matricula)'].value_counts().index, ax=ax1)
ax1.set_title("Distribuição de Alunos por Curso")
ax1.set_xlabel("Total de Alunos")
ax1.set_ylabel("Curso")
st.pyplot(fig1)

# Gráfico 2 - Avaliação por competência
df_filtrado = df_long[df_long['Curso (Matricula Atual) (Matricula)'] == curso_sel]
df_agrupado = df_filtrado.groupby(['Competência', 'Nota']).size().reset_index(name='Total')
df_pivot = df_agrupado.pivot(index='Competência', columns='Nota', values='Total').fillna(0)

ordem_notas = ['F', 'D', 'ND', 'NO']
df_pivot = df_pivot[[n for n in ordem_notas if n in df_pivot.columns]]

st.subheader(f"Avaliação das Competências - {curso_sel}")
fig2, ax2 = plt.subplots(figsize=(12, 6))
df_pivot.plot(kind='bar', stacked=True, ax=ax2, colormap='Set2')
ax2.set_xlabel("Competência")
ax2.set_ylabel("Total de Avaliações")
ax2.set_title(f"Notas atribuídas por competência - {curso_sel}")
ax2.legend(title='Nota')
st.pyplot(fig2)

# Bloco: Visualização detalhada dos alunos por Competência + Nota
st.subheader("🔍 Detalhar alunos por Competência e Nota")

col1, col2 = st.columns(2)

with col1:
    competencia_sel = st.selectbox("📘 Selecione a competência:", sorted(df_filtrado['Competência'].unique()))

with col2:
    nota_sel = st.selectbox("🏷️ Selecione a nota:", sorted(df_filtrado['Nota'].unique()))

# Filtrar os alunos com base na escolha
detalhe = df_filtrado[
    (df_filtrado['Competência'] == competencia_sel) & (df_filtrado['Nota'] == nota_sel)
]

if not detalhe.empty:
    st.markdown(f"**Alunos com nota '{nota_sel}' em '{competencia_sel}':**")
    st.dataframe(detalhe[['RA', 'Curso (Matricula Atual) (Matricula)', 'Competência', 'Nota']])
else:
    st.info("Nenhum aluno encontrado com essa combinação.")



