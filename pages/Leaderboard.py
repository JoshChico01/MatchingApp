import streamlit as st
import pandas as pd
import boto3


st.set_page_config(
    page_title="Leaderboard",
    page_icon="👋",
)

s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-1',
        aws_access_key_id=  st.secrets["AWS_ACCESS_KEY_ID"], #os.environ['AWS_ACCESS_KEY_ID'] ,
        aws_secret_access_key= st.secrets["AWS_SECRET_ACCESS_KEY"] #os.environ['AWS_SECRET_ACCESS_KEY']
    )

bucket = s3.Bucket("photomatchingapp")

names = []
scores = []

for my_bucket_object in bucket.objects.all():
    object_ = my_bucket_object

    df = pd.read_csv(object_.get()["Body"])
    score = 0

    for col in df:
        if col == df[col][0]:
            score += 1
    
    name = str(object_.key).split(".")[0]

    names.append(name)
    scores.append(score)

    #response = s3.Object("photomatchingapp","/"+file_name)

    #df = pd.read_csv(response["Body"])


df = pd.DataFrame({
    "Name" : name,
    "Score" : scores
})

df.index = df.index + 1

st.table(df)
    