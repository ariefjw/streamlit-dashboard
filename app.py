import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
from groq import Groq
from PIL import Image

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
data = conn.query('''SELECT * FROM movies_data;''', ttl="10m")



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
  <center><h1 class="title" style="color:#A9A9A9;">Dashboard BBBBBBBB</h1></center>"""

creator = """<p>Created by :<br> - Amsiki Bagus R<br> - Mirza Rendra S<br> - Lusitania Ragil C<br> - Felix Giancarlo<br> - Arief Joko W</p>"""

#chart
product_type_price = data.groupby('product_type')['harga'].sum().reset_index()
fig_count_status = px.bar(product_type_price, x='product_type', y='harga', title='Distribution Genre')
# fig_trend_sales = px.line(data, x="release_year", y="jumlah", title='Movie Trend')


logo, page_title = st.columns([0.1,0.9])
with logo:
  st.image(image, width=100)
with page_title:
  st.markdown(title, unsafe_allow_html=True)
st.markdown('---')

pilihan = st.selectbox('Pilih kolom:',('Age','Weight','Height','ShootingTotal'))
created_by, chart1, chart2 = st.columns([0.1,0.45,0.45])
with created_by:
  st.markdown(creator, unsafe_allow_html=True)
with chart1:
  st.plotly_chart(fig_count_status, use_container_width=True)
# with chart2:
#   st.plotly_chart(fig_trend_sales, use_container_width=True)


__ , chat_ai = st.columns([0.1, 0.9])


with chat_ai:
  chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f" Analisa berdasarkan data {data}",
        }
    ],
    model="llama3-8b-8192",
  )
  
  st.write(f"{chat_completion.choices[0].message.content}")

