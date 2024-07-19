import streamlit as st
import os
import boto3
import pandas as pd
import random
from io import StringIO

def done(chosen_images, images, name, placeholder):
    st.session_state.done = True

    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-1',
        aws_access_key_id=  st.secrets["AWS_ACCESS_KEY_ID"], #os.environ['AWS_ACCESS_KEY_ID'] ,
        aws_secret_access_key= st.secrets["AWS_SECRET_ACCESS_KEY"] #os.environ['AWS_SECRET_ACCESS_KEY']
    )



    score = 0

    guess_dict = {}


    for img, target in zip(chosen_images, [i.split("/")[2] for i in images]):

        guess_dict[target] = [img]

    df_guesses = pd.DataFrame(guess_dict)
    
    
    csv_buffer = StringIO()
    df_guesses.to_csv(csv_buffer, index = False)

    s3.Object('photomatchingapp', f'{name}.csv').put(Body=csv_buffer.getvalue())

    placeholder.empty()

    with placeholder.container():
        st.header("Good Job!")
    

@st.cache_data
def getImgs():

    images = ["./Images/" + img_string for img_string in os.listdir("./Images") ]
    random.shuffle(images)

    return images

if "done" not in st.session_state:
    st.session_state.done = False

random.seed(10)

placeholder = st.empty()

images = getImgs()
with placeholder.container():
    if not st.session_state.done:
        st.header("Baby Photo Matching")
        st.write("Match the baby photo with the person!")

        players = ["Sarah", "Shavani", "Yvonne", "Titia","Tester", "Pina", "Zoe", "Angela", "Amy I", "Tiff", "Courtney", "Megan", "Jess", "Renae", "Amie H", "Britt", "Jenny", "Gabs"]

        name = st.selectbox(label  = "Enter your name: ", options = players, key = "name" )
        #name = st.text_input(label = "Enter your name:")

        chosen_images = []


        for img in images:

            left_col, divider_col, right_col = st.columns([0.2,0.02,0.78])
            left_col.image(img)
            
            with right_col:
                img_options = [img_file.split(".")[-2] for img_file in os.listdir("./Images")]
                random.shuffle(img_options)     
                chosen_img = st.selectbox(label  = "Select: ", options = img_options, key = img )
                chosen_images.append(chosen_img)

            st.markdown("""---""")

        images = [img.split(".")[-2] for img in images]

        st.button("Done ✓", on_click=done, args=(chosen_images, images, name, placeholder))
