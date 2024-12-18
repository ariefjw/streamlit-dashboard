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

df = pd.read_csv('data_for_database.csv')
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


logo, page_title = st.columns([0.15,0.85])
with logo:
  st.image(image, width=100)
with page_title:
  st.markdown(title, unsafe_allow_html=True)
st.markdown('---')

created_by, chart1, chart2 = st.columns([0.15,0.4,0.4])
with created_by:
  st.markdown(creator, unsafe_allow_html=True)
with chart1:
  st.plotly_chart(fig_count_status, use_container_width=True)
# with chart2:
#   st.plotly_chart(fig_trend_sales, use_container_width=True)







_1_ , chat_ai = st.columns([0.15, 0.85])


with chat_ai:
  def chat_respon(text) -> Generator[str, None, None]:
    """
    Memberikan respon kepada user dari API respon groq
    """
    for word in text:
        if word.choices[0].delta.content:
            yield word.choices[0].delta.content
 
  if "messages" not in st.session_state:
      st.session_state.messages = []
  
  if prompt := st.chat_input("Anda ingin bertanya?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar='🐣'):
      st.markdown(prompt)
    
    try:
        chat_completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": m["role"],
                    "content": f"{m["content"]}, berikan jawaban berkaitan dengan {df}. Jawab dengan bahasa sesuai dengan bahasa di : ({m["content"]})"
                }
                for m in st.session_state.messages
            ],
            stream=True
        )
        with st.chat_message("assistant", avatar='👩‍🏫'):
            prompt_respon = chat_respon(chat_completion)
            full_response = st.write_stream(prompt_respon)
    except Exception as e:
        st.error(e, icon="⚠️")

     
    if isinstance(full_response, str):
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response})
    else:
        response_convert = "\n".join(str(item) for item in full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": response_convert})


