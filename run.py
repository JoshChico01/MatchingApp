import streamlit as st
import os
import boto3
import pandas as pd
import random
from io import StringIO

st.set_page_config(
    page_title="Quiz!",
    page_icon="👋",
)

def done(chosen_images, images, name, placeholder):
    st.session_state.done = True

    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-1',
        aws_access_key_id=  st.secrets["AWS_ACCESS_KEY_ID"], #os.environ['AWS_ACCESS_KEY_ID'] ,
        aws_secret_access_key= st.secrets["AWS_SECRET_ACCESS_KEY"] #os.environ['AWS_SECRET_ACCESS_KEY']
    )

    guess_dict = {}


    for img, target in zip(chosen_images, [i.split("/")[2] for i in images]):

        guess_dict[target] = [img]

    df_guesses = pd.DataFrame(guess_dict)
    
    
    csv_buffer = StringIO()
    df_guesses.to_csv(csv_buffer, index = False)

    

    s3.Object('photomatchingapp', f'{name}.csv').put(Body=csv_buffer.getvalue())

    placeholder.empty()

def getImgs():

    images = ["./Images/" + img_string for img_string in os.listdir("./Images") ]
    random.shuffle(images)

    return images

def getScore(guesses, images):
    score = 0
    total = 0

    for g, i in zip(guesses, images):
        if g == i.split("/")[-1]:
            score += 1
        total += 1

    return [score, total]

def try_pass(password):
    if password == "baby":
        st.session_state.password = True
    else:
        st.session_state.incorrrect = True

if "password" not in st.session_state:
    st.session_state.password = False
    
if "incorrect" not in st.session_state:
    st.session_state.incorrrect = False

if "done" not in st.session_state:
    st.session_state.done = False

if "bundle" not in st.session_state:
    st.session_state.bundle = None

random.seed(11)

placeholder = st.empty()

images = getImgs()

bundle = None
with placeholder.container():
    if (not st.session_state.done) and st.session_state.password:
        st.header("Baby Photo Matching")
        st.write("Match the baby photo with the person!")

        players = ["Sarah", "Shavani", "Yvonne", "Titia", "Pina", "Zoe", "Angela", "Amy I", "Tiff", "Courtney", "Megan", "Jess", "Renae", "Amie H", "Britt", "Jenny", "Gabs", "Alex", "Josh", "John"]

        name = st.selectbox(label  = "Enter your name: ", options = players, key = "name" )
        #name = st.text_input(label = "Enter your name:")
        st.markdown("""---""")
        chosen_images = []


        for img in images:

            left_col, divider_col, right_col = st.columns([0.2,0.02,0.78])
            left_col.image(img)
            
            with right_col:
                img_options = [img_file.split(".")[-2] for img_file in os.listdir("./Images")]
                chosen_img = st.selectbox(label  = "Select: ", options = img_options, key = img )
                chosen_images.append(chosen_img)

            st.markdown("""---""")

        images = [img.split(".")[-2] for img in images]

        bundle = getScore(chosen_images, images)
        st.session_state.bundle = bundle

        st.button("Done ✓", on_click=done, args=(chosen_images, images, name, placeholder))

    if st.session_state.done:

        bundle = st.session_state.bundle

        messages = ["Really.. you didn't even get Koda?"] + ["Hmmm.. good try..."] * 2 + ["You just guessed didn't you.."] * 2 + ["Well, you tried"] * 3+ ["Not a bad effort"] * 2 + ["Over 50%? That's a pass!"] * 3 + ["Good job!"] * 3 + ["Wow! So close to perfect!"] *2 + ["Perfect! Great job!"]

        if bundle:
            st.header(messages[bundle[0]])
            st.write(f"You scored {bundle[0]}/{bundle[1]}")
        else:
            st.header("Good job!")
            st.write("Score is not available.")

    if not st.session_state.password:
        st.header("Baby Photo Matcher!")
        st.write("Enter the password to get started")
        password = st.text_input(label = "Password:")
        if st.session_state.incorrrect:
            st.write("Incorrect password, try again...")
        st.button("Go", on_click=try_pass, kwargs ={"password" : password})
