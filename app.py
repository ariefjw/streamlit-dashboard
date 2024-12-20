import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
from groq import Groq
from PIL import Image
from typing import Generator

#setup groq
client = Groq(
    api_key= st.secrets["GROQ_API_KEY"],
)

#page configuration
st.set_page_config(
    page_title="Dashboard",
    page_icon=":earth_asia:",
    layout="wide",
    initial_sidebar_state="expanded")

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
data = conn.query('''SELECT * FROM data_clean_fp;''', ttl="10m")
depedency = conn.query('''SELECT * FROM fact_depedency_ratio;''', ttl="10m")
workforce = conn.query('''SELECT * FROM fact_workforce_ratio;''', ttl="10m")
unemployee = conn.query('''SELECT * FROM fact_unemployment_ratio;''', ttl="10m")
industri = pd.read_csv('data_non_5.csv')



#setup layout
image = Image.open("src/img/logo.png")

title = """
  <style>
  .title-test {
  font-weight:bold;
  padding:5px;
  border-radius:6px;
  }
  </style>
  <center><h1 class="title" style="color:#A9A9A9;"> Workforce Analysis </h1></center>"""

creator = """<p>Created by :<br> - Amsiki Bagus R<br> - Mirza Rendra S<br> - Lusitania Ragil C<br> - Felix Giancarlo<br> - Arief Joko W</p>"""

#filter data
filter_workforce = workforce[workforce['country'].isin(['Argentina',
 'Brazil',
 'China',
 'Dominican Republic',
 'Ecuador',
 'Ghana',
 'Indonesia'])]
filter_depedency = depedency[depedency['country'].isin(['Argentina',
 'Brazil',
 'China',
 'Dominican Republic',
 'Ecuador',
 'Ghana',
 'Indonesia'])]
filter_unemployee = unemployee[unemployee['country'].isin(['Argentina',
 'Brazil',
 'China',
 'Dominican Republic',
 'Ecuador',
 'Ghana',
 'Indonesia'])]

#chart

fig_count_status = px.bar(filter_workforce, x='labor_force_ratio', y='country', title='Labor Force Ratio',text_auto='.2s', hover_data=['labor_force_ratio']).update_layout(xaxis_title="Percentage Labor Force", yaxis_title=" ")
fig2 = px.bar(filter_depedency, x='df_depedency_ratio', y='country', title='Depedency Ratio',text_auto='.2s').update_layout(xaxis_title="Percentage Depedency", yaxis_title=" ")
fig3 = px.bar(filter_unemployee, x='unemployed_ratio', y='country', title='Unemployment Ratio',text_auto='.2s').update_layout(xaxis_title="Percentage Unemployee", yaxis_title=" ")



logo, page_title = st.columns([0.15,0.85])
with logo:
  st.image(image, width=100)
with page_title:
  st.markdown(title, unsafe_allow_html=True)
st.markdown('---')

created_by, chart1, chart2, chart3 = st.columns([0.15,0.26,0.26,0.26])
with created_by:
  st.markdown(creator, unsafe_allow_html=True)
with chart1:
  st.plotly_chart(fig_count_status, use_container_width=True)
with chart2:
  st.plotly_chart(fig2, use_container_width=True)
with chart3:
  st.plotly_chart(fig3, use_container_width=True)

_4_ , pilihan = st.columns([0.15, 0.85])
with pilihan:
  filter_negara = st.selectbox('Pilih Negara:',('Argentina',
  'Brazil',
  'China',
  'Dominican Republic',
  'Ecuador',
  'Ghana',
  'Indonesia'))

_3_ , chart4, chart5 = st.columns([0.15, 0.42, 0.43])
with chart4:
  industri_filter = industri[industri['Country or Area']==filter_negara].sort_values('Value', ascending=False).head(5)
  fig4 = px.bar(industri_filter, x='Industry', y='Value', title=f'Industry in {filter_negara} (Value)',text_auto='.2s').update_layout(xaxis_title="Name Industry", yaxis_title=" ")
  st.plotly_chart(fig4, use_container_width=100)
with chart5:
  industri_filter_percentage = industri[industri['Country or Area']==filter_negara].sort_values('ratio', ascending=False).head(5)
  fig5 = px.bar(industri_filter, x='Industry', y='ratio', title=f'Industry in {filter_negara} (Percentage)',text_auto='.2s').update_layout(xaxis_title="Name Industry", yaxis_title=" ")
  st.plotly_chart(fig5, use_container_width=100)




_2_ , pilih1, pilih2, pilih3 = st.columns([0.15, 0.26,0.26,0.26])
with pilih1:
  negara = st.multiselect('Informasi tentang:',('Argentina',
 'Brazil',
 'China',
 'Dominican Republic',
 'Ecuador',
 'Ghana',
 'Indonesia'))
# with pilih2:
#   Topic = st.multiselect('Pilih Topic', ('Rasion Pekerja', 'Rasion Pengangguran'))


_1_ , chat_ai = st.columns([0.15, 0.85])


with chat_ai:

  if input_user := negara:
    if len(negara)==1:
      input_user = f'Jelaskan tentang {negara} bedasar pada data {data}, Jawab dengan bahasa Indonesia bahasa'
    elif len(negara)>1:
      banding = ''
      for i in negara:
        banding+= i+','
      input_user = f"bandingkan antara {banding} dari data : {workforce},{unemployee},{depedency}. Jawab dengan bahasa Indonesia bahasa"
    else:
      input_user = negara

  chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"{input_user}",
        }
    ],
    model="llama3-8b-8192",
  )
  st.write(f"{chat_completion.choices[0].message.content}")
