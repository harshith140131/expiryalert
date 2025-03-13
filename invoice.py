from dotenv import load_dotenv
import datetime
import streamlit as st
from PIL import Image
import database as db
import google.generativeai as genai
import os
# Load environment variables
load_dotenv()
print("Starting-----")
# Configure Google API
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
genai.configure()
# Set the API key directly
genai.api_key = "AIzaSyDDCDRrlOFb0RJJ3kXtEeAmvkctx1_DJUU"
st.set_page_config(page_title="ExpiRem")
st.header("Invoice items app")

def submitted():
   st.session_state.submitted = True
def reset():
   st.session_state.submitted = False

# Function to load Google Gemini Pro Vision API And get response
def get_gemini_repsonse(input, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')

    response = model.generate_content([input, image[0], prompt])
    return response.text

# Function to setup input image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")



# Input Prompt
input_prompt = """
You are an expert in identifying different items from the image of an invoice
               is below format

               1. Item 1 
               2. Item 2
               ----
               ----
"""

# Form Submission

        
def first_load():
    # Email Input Field
    input_email = st.text_input("Enter email:", key="input_email", help="Your email address",autocomplete="email")

    # Uploaded Image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    # Submit Button
    # if st.session_state.submitted==False:
    st.button("Tell me the items in the image", key="submit_button",on_click=reset)


    return input_email,uploaded_file

def second_load(email,uploaded_file=None):
    # if submit_button:
    if uploaded_file:
        # image_data = input_image_setup(uploaded_file)
        # response = get_gemini_repsonse(input_email, image_data, input_prompt)
        # st.subheader("The Response is")
        # items_list = [line.split('. ', 1)[-1].strip() for line in response.split('\n') if line.strip()]
        name=uploaded_file.name
        name=name.replace(" ","_")
        if "mail" in st.session_state and  email+name  in st.session_state.mail.keys():   
                print("reaading from cache")
                items_list = st.session_state.mail[email+name]
        else:
            print("Not there in cache reading from gemini")
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_repsonse(email, image_data, input_prompt)
            st.subheader("The Response is")
            items_list = [line.split('. ', 1)[-1].strip() for line in response.split('\n') if line.strip()]
            st.session_state.mail={email+name:items_list}
        print("hi",st.session_state)
        # items_list=['SUNRISE SNACKS', 'OREO-BISCUITS', 'NABATI-WAFER B', 'AGARABATHI', 'LOLLI POP', 'CHOCOLATES', 'BRITANIA-CAKES', 'POTATO CHIPS', 'COOL DRINKS']
        # print(items_list)
        render_form(items_list,email)
    # else:
    #     st.write("please upload your invoice")


def render_form(items_list,email):
    entered_dates = {}  # Dictionary to store entered dates for each item

    with st.form(key='my_form'):
        for item in items_list:
            st.write(item)
            entered_dates[item] = st.date_input(f"Enter Expiry Date for {item}", key=f"text_input_{item}")
        
        st.form_submit_button("Submit", on_click=submitted)
        
        if st.session_state.submitted == True:
            print("Form submitted!")  # This will appear in the Streamlit server console
            print("Entered Dates:")
            for item, date in entered_dates.items():
                try:
                    db.insert_data(email=email,item=item,expiry_date=date)
                    db.commit()
                    st.write(f"{item}: {date}")
                except:
                    pass
            db.close()
            # callFun()
            reset()

        



if __name__=='__main__':
    try:
        db.create_table()
    except:
        pass
    input_email,uploaded_file=first_load()
    if "submitted" in st.session_state:

        second_load(input_email,uploaded_file)
