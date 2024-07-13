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

for my_bucket_object in bucket.objects.all():
    file_name = my_bucket_object.key

    response = s3.Object("photomatchingapp",file_name)

    df = pd.read_csv(response["Body"])

    st.table(df)
    