import streamlit as st
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
    st.write(my_bucket_object.key)