import streamlit as st
import streamlit_image_select as stis
import os
import boto3
import pandas as pd
from io import StringIO

def done(chosen_images, images, name):
    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-1',
        aws_access_key_id= os.environ['AWS_ACCESS_KEY_ID'] ,
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
    )



    score = 0

    for img, target in zip(chosen_images, images):
        if img == target:
            score += 1

    _dict = {
        "name" : [name],
        "score" : [score]
    }

    df = pd.DataFrame(_dict)
    
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)

    s3.Object('photomatchingapp', f'{name}.csv').put(Body=csv_buffer.getvalue())




    

images = ["./Images/" + img_string for img_string in os.listdir("./Images") ]


st.markdown("<h1 style='text-align: center; color: black;'>Baby Photo Matching!</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: black;'>Match each baby photo with the correct person</p>", unsafe_allow_html=True)

name = st.text_input(label = "Name:")

chosen_images = []


for img in images:

    left_col, divider_col, right_col = st.columns([0.2,0.02,0.78])

    divider_col.markdown("""<style>
            h2 {
  border-left-style: solid;
  border-left-color: gray;
  padding-left: 25px;
  }         
            </style>""", unsafe_allow_html=True)
    
    divider_col.markdown("<h2 style='padding-bottom : 550px;'></h2>", unsafe_allow_html=True)

    left_col.image(img)
    
    with right_col:
        chosen_img = stis.image_select(label="",images=images, key = img)
        chosen_images.append(chosen_img)

    st.markdown("""---""")



st.button("Done ✓", on_click=done, args=(chosen_images, images, name))
