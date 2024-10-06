from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(model_name="gemini-1.5-flash")


def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]

        return image_parts
    else:
        raise FileNotFoundError("No file uploaded!")


st.set_page_config(
    page_title="Multilanguage Invoice Extractor", page_icon="📝", layout="wide"
)
st.header("Gemini AI Application")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader(
    "Choose an image of the invoice...", type=["jpg", "jpeg", "png"]
)
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Invoice", use_column_width=True)


submit = st.button("Tell me about the invoice")
input_prompt = """You are an invoice summarizer. You will be summarizing the invoice and 
                  providing the important information in points within 250 words. The invoice is: """

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input, image_data, input_prompt)
    st.subheader("The Response is")
    st.write(response)
