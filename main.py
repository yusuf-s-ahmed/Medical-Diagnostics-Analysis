import streamlit as st
import openai
from dotenv import find_dotenv, load_dotenv
import os
from pydantic import BaseModel
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time
from twilio.rest import Client
import requests
import urllib.parse


# Set up the page configuration
st.set_page_config(
    page_title="AI Heart Rate Monitor",
    page_icon="🏥",
)

# Custom CSS
st.markdown("""
    <style>
    /* Import Roboto font for a professional look */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

    /* Change the background color to light */
    .stApp {
        background-color: #fffff;
    }
            
    

    /* Style for input boxes when focused (clicked) */
    input:focus, .stTextInput:focus, .stTextArea:focus, .stNumberInput:focus, .stDateInput:focus {
        outline: 2px solid #c0392b;  /* Darker red outline when focused */
        box-shadow: 0 0 5px rgba(219, 44, 44, 0.8);  /* Optional: adds a glowing effect */
    }


    /* Change the color of the sidebar */
    .css-1d391kg {  
        background-color: #e9ecef; 
    }

    /* Style for the navbar */
    .stToolbar {
        background-color: #e9ecef; 
    }

    /* Change styles for selectable boxes */
    .stSelectbox, .stCheckbox, .stRadio {
        background-color: #ffffff; 
        border-radius: 5px; 
        border: 1px solid #ced4da; 
        box-shadow: none; 
        outline: none; 
    }

    /* Change font style and size for the title */
    h1 {
        font-family: 'Roboto', sans-serif;
        font-size: 40px;
        color: #212529;
        font-weight: 500; 
    }

    h3 {
        font-family: 'Roboto', sans-serif;
        font-weight: 400; 
        color: #495057; 
        font-size: 20px;
    }

    /* Set regular text (paragraphs) to darker font weight */
    p, div, span, label {
        font-family: 'Roboto', sans-serif;
        font-weight: 400; 
        color: #495057; 
    }

    /* Style for buttons */
    .stButton button {
        background-color: rgba(240, 240, 240, 0.5);  /* Slightly grey background */
        font-family: 'Roboto', sans-serif;
        font-size: 15px;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid rgba(219, 44, 44, 0.8);  /* Red outline */
        color: #f5f5f5;  /* Light grey text */
    }

    .stButton button:hover {
        background-color: rgba(219, 44, 44, 0.1);  /* Light red background on hover */
        color: white;  /* White text on hover */
        border-color: #c0392b;  /* Darker red outline on hover */
    }

    /* Style for title "HeartGuard" with "Heart" in red */
    .heartguard-title {
        font-family: 'Roboto', sans-serif;
        font-size: 36px;
        font-weight: 400; 
    }
    .heartguard-title .heart {
        color: #b81111; /* red color for 'Heart' */
    }

    /* Style for sliders */
    .stSlider .st-1l9uh0ax {
        color: #007bff;
    }
    </style>
    """, unsafe_allow_html=True)

#Displaying the title with 'Heart' in red using HTML
st.markdown('<h1 class="heartguard-title"><span class="heart">Heart</span>Guard</h1>', unsafe_allow_html=True)



# Account SID and Auth Token from twilio.com/console
account_sid = '-'
auth_token = '-'
client = Client(account_sid, auth_token)

# Call details
twilio_phone_number = '-'
destination_phone_number = '-
webhook_url = 'https://demo.twilio.com/welcome/-/'



# Function to call a phone number using Twilio and speak the generated message
def make_call(message):
    call = client.calls.create(
        to=destination_phone_number,
        from_=twilio_phone_number,
        url=f"http://twimlets.com/message?Message[0]={message}"  # URL to convert text to speech
    )
    return call.sid


# OpenAI API key
openai.api_key = "-"


# Simulate data similar to your example
x = np.linspace(102080, 102140, 20)  # X-axis values (time or sample points)
y = np.array([195, 195, 195, 195, 195, 196, 196, 195, 194, 194, 193, 195, 195, 195, 195, 195, 195, 195, 195, 195])  # Y-axis values


# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = 1  # Set initial page to 1

# Define page navigation functions
def next_page():
    st.session_state.page += 1

def prev_page():
    st.session_state.page -= 1



# Natural Language Processing: OpenAI
# Function to generate emergency alert message using OpenAI GPT-3.5-turbo
def generate_emergency_alert(bpm, coordinates, contact_name, contact_phone):
    
    prompt = f"""
    An emergency alert is required for this patient, who has been detected with a critical heart rate of {bpm} BPM. 
    This value is in a dangerous zone and may indicate a life-threatening situation. The patient’s last known coordinates are {coordinates}.
    Generate an urgent message requesting immediate medical intervention, including location instructions and contact information.

    **Contact Information:**
    - **Emergency Contact Name:** {contact_name}
    - **Phone:** {contact_phone}

    Example:

    **Description:**  
    An emergency alert has been triggered due to a critically low heart rate reading of (enter_patients_BPM) beats per minute, 
    accompanied by a lack of response from the patient. Immediate medical intervention is required as this condition may indicate 
    potential cardiac distress or other life-threatening complications.

    **Requested Action:**  
    Please dispatch emergency medical services to the location provided. This alert is prioritized due to the critical nature of the low heart rate 
    and the unresponsive status of the patient.

    **Contact Information:**

    - **Emergency Contact Name:** [Emergency Contact’s Name]
    - **Phone:** [Emergency Contact’s Phone Number]

    This was an example of a very high BPM, but use your jugdement to craft a message in accordance with your given scenario.
    But MAKE SURE the format that you give this in is URL encoded.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an emergency medical alert assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        # Extract and return the generated message
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating alert: {e}"
# Function to generate a detailed medical report using GPT-4
def generate_medical_report(user_name, user_age, user_bpm, user_height, user_weight):
    try:
        prompt = """
        You are a health assistant specialized in interpreting heart rate data. 
        Use British spelling and form 5 very detailed paragraphs in a structured way to mimic a medical diagnostic report. 
        Do not state the formula for BMI, just mention the BMI value you calculate.
        Use ** <text> ** for headers, and do not use tentative language. Be direct and assertive as you are trained for this. 
        Your analysis should be clear, confident, and based on the user's provided data. Capitalize the name. And make sure the patient details are exact and not rounded.
        """

        user_data = f"""
        The user's name is {user_name}, age is {user_age}, heart rate (BPM) is {user_bpm}, height is {user_height}, weight is {user_weight}.
        Calculate the BMI based on the provided data and include it in your response. 
        Then provide an analysis of this BPM based on age, potential risks, and health recommendations.
        Format the response as follows:

        **Patient Details:**
        Name: {user_name}
        Age: {user_age} years
        Heart Rate (BPM): {user_bpm}
        Height: {user_height} meters
        Weight: {user_weight} kilograms

        **BMI Calculation:**
        Based on the provided measurements, the BMI is calculated as [calculated BMI].

        **BPM Analysis:**
        Provide a detailed analysis of the user's BPM, considering age, normal ranges for heart rate, and whether the BPM is within the expected range for the user.

        **Potential Risks:**
        Discuss any potential risks based on the user's BPM and health metrics. Consider lifestyle factors, health conditions, and the relevance of maintaining a healthy heart rate.

        **Health Recommendations:**
        Based on the current heart rate and age, provide actionable recommendations for maintaining or improving cardiovascular health.

        **Conclusion:**
        Summarise the findings, including the normalcy of the heart rate, any risks, and the importance of maintaining a healthy lifestyle for heart health.
        """

        # Updated call to openai.ChatCompletion.create with the new API structure
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_data}
            ]
        )

        # Extract and return the generated report
        analysis_text = response.choices[0].message.content.strip()
        return analysis_text
    
    except Exception as e:
        return f"Error generating report: {e}"



# Page 1: Introduction and User Details
if st.session_state.page == 1:
    
    
    st.subheader(
        "Monitoring your heart, guarding your life."
    )
    
    st.write("---")
    
    user_name = st.text_input("Enter Name:")
    user_email = st.text_input("Enter Email:")
    user_age = st.number_input("Enter Age: ", min_value=1, step=1)
    user_weight = st.number_input('Enter Weight (kg):', step=0.25)
    user_height = st.number_input('Enter Height (m):')
    user_bpm = st.number_input("Enter Average BPM:", min_value=0.0, step=0.1)  # BPM input

    st.write("Ensure ECG 3-Point Sensor is connected to the right forearm, left forearm, and right ankle.")

    # Initialize the flag for showing "View Analysis" button after BPM insights creation
    if 'bpm_insights_created' not in st.session_state:
        st.session_state.bpm_insights_created = False

    # Button to create BPM Insights
    if st.button("Create BPM Insights"):
        st.session_state.bpm_insights_created = True  # Set flag to True when button is clicked
        
        st.write("Generating Diagnostic...")
        medical_report = generate_medical_report(user_name, user_age, user_bpm, user_height, user_weight)
        st.session_state.medical_report = medical_report  # Store report in session state
    

    # Show the "View Analysis" button only if the "Create BPM Insights" button was clicked
    if st.session_state.bpm_insights_created:
        if 'view_analysis_triggered' not in st.session_state:
            st.session_state.view_analysis_triggered = False
        
        # When the user clicks "View Analysis", transition to next page
        if st.button("View Analysis >") and not st.session_state.view_analysis_triggered:
            st.session_state.view_analysis_triggered = True  # Set this flag to ensure transition happens only once
            next_page()  # Transition to the next page immediately


   

# Page 2: AI Overview with Analysis
elif st.session_state.page == 2:
    
    st.write("---")
    st.subheader("AI Heart Rate Analysis Report")


    # Visualization with Plotly
    x = np.linspace(102080, 102140, 20)
    y = np.array([195, 195, 195, 195, 195, 196, 196, 195, 194, 194, 193, 195, 195, 195, 195, 195, 195, 195, 195, 195])
    fig = go.Figure()

    # Add line plot
    fig.add_trace(go.Scatter(
        x=x, 
        y=y, 
        mode='lines+markers', 
        name='BPM Data', 
        line=dict(color='red', width=1.1),
        marker=dict(size=3)
    ))

    # Customize layout
    fig.update_layout(
        xaxis_title="Time (Sample)",
        yaxis_title="Sensor Value",
        xaxis=dict(range=[102080, 102140]),
        yaxis=dict(range=[193, 197]),
        template="plotly_white",
        font=dict(family="Roboto", color="#212529", size=12),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff"
    )

    st.plotly_chart(fig)
    # Display the generated medical report if available
    if st.session_state.get("bpm_insights_created") and st.session_state.get("medical_report"):
        st.write(st.session_state.medical_report)
    else:
        st.write("No analysis report available. Please generate insights on the previous page.")
    

    if st.button("< Back"):
        prev_page()

    if st.button("Simulate Critical Alert >"):
        next_page()

# Page 3: Emergency Critical Alert Simulation
if st.session_state.page == 3:
    st.write("---")
    st.subheader("Emergency Critical Alert Simulation")
    
    st.write("""
        This works by artificially sending a BPM value in a critical zone (>150 or <40) consistently. 
        To get started, enter a coordinate on the map.
        
        Hint: City University's coordinates are: **51.527, -0.1023**
    """)

    # Inputs for Simulated Extreme BPM, Coordinates, Name, and Phone Number
    simulated_bpm = st.number_input("Enter Simulated Extreme BPM:", min_value=0.0, step=0.1)
    user_coordinates = st.text_input("Enter Coordinates:")
    emergency_contact_name = st.text_input("Enter Emergency Contact Name:")
    emergency_contact_phone = st.text_input("Enter Emergency Contact Phone Number:")

    # Initialize flags for alert simulation and response handling
    if 'alert_simulated' not in st.session_state:
        st.session_state.alert_simulated = False
    if 'response_given' not in st.session_state:
        st.session_state.response_given = False

    # Simulate Alert button functionality
    if st.button("Simulate Alert"):
        st.session_state.alert_simulated = True  # Trigger the alert simulation
        st.write("Waiting for a response from the patient...")
        st.session_state.response_given = False  # Reset response flag for a new alert

        # Countdown simulation
        countdown_text = st.empty()  # Placeholder for countdown text
        for i in range(7, 0, -1):
            countdown_text.markdown(f"**Time remaining:** {i} seconds")
            time.sleep(1)  # 1-second delay per countdown step
        countdown_text.empty()  # Clear countdown after completion

        # Generate emergency alert message using OpenAI API with additional inputs
        emergency_message = generate_emergency_alert(simulated_bpm, user_coordinates, emergency_contact_name, emergency_contact_phone)
        st.session_state.emergency_message = emergency_message  # Store the generated message

        st.write(f"Generated Emergency Message: {emergency_message}")  # Debugging: Output generated message

    # Display the generated emergency message if alert is simulated
    if st.session_state.alert_simulated and not st.session_state.response_given:
        st.subheader("AI Generated Emergency Alert Message:")
        # Show the map after the countdown
        st.image("map2.jpeg", caption="Exact location of the patient.", use_column_width=True)
        st.write(st.session_state.emergency_message)

        encoded_message = urllib.parse.quote(emergency_message)
        call_sid = make_call(encoded_message)
            

    # Navigation button to go to the previous page
    if st.button(" < "):
        prev_page()
