import streamlit as st
import os
import boto3
import pandas as pd
from io import StringIO

def done(chosen_images, images, name):
    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-1',
        aws_access_key_id=  st.secrets["AWS_ACCESS_KEY_ID"], #os.environ['AWS_ACCESS_KEY_ID'] ,
        aws_secret_access_key= st.secrets["AWS_SECRET_ACCESS_KEY"] #os.environ['AWS_SECRET_ACCESS_KEY']
    )



    score = 0

    for img, target in zip(chosen_images, [i.split("/")[2] for i in images]):
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


st.header("Baby Photo Matching")
st.write("Match the baby photo with the person!")

name = st.text_input(label = "Name:")

chosen_images = []


for img in images:

    left_col, divider_col, right_col = st.columns([0.2,0.02,0.78])
    left_col.image(img)
    
    with right_col:        
        chosen_img = st.selectbox(label  = "Select: ", options = os.listdir("./Images"), key = img )
        chosen_images.append(chosen_img)

    st.markdown("""---""")

st.button("Done ✓", on_click=done, args=(chosen_images, images, name))
