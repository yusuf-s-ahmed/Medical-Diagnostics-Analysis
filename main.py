import streamlit as st
import openai
from dotenv import find_dotenv, load_dotenv
import os
from pydantic import BaseModel
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time



# Set up the page configuration
st.set_page_config(
    page_title="AI Heart Rate Monitor",
    page_icon="🏥",
)

# Custom CSS
st.markdown("""
    <style>
    /* Import Roboto font for a more medical, professional look */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

    /* Change the background color */
    .stApp {
        background-color: #18191c;
    }

    /* Change the color of the sidebar */
    .css-1d391kg {  
        background-color: #35383b; 
    }

    /* Style for the navbar */
    .stToolbar {
        background-color: #35383b; 
    }

    /* Change styles for selectable boxes */
    .stSelectbox, .stCheckbox, .stRadio {
        background-color: transparent; 
        border-radius: 5px; 
        border: none; 
        box-shadow: none; 
        outline: none; 
    }


    /* Change font style and size for the title */
    h1 {
        font-family: 'Roboto', sans-serif;
        font-size: 36px;
        color: #ababab;
        font-weight: 300; 
    }

    h3 {
        font-family: 'Roboto', sans-serif;
        font-weight: 370; 
        color: #ababab; 
        font-size: 20px;
    }

    /* Set regular text (paragraphs) to lighter font weight */
    p, div, span, label {
        font-family: 'Roboto', sans-serif;
        font-weight: 300; 
        color: #ababab; 
    }

    /* Style for buttons */
    .stButton button {
        
        font-family: 'Roboto', sans-serif;
        font-size: 15px;
        padding: 10px;
        border-radius: 5px;
        border: 0.2px solid white;  
        color: white;
    }

    .stButton button:hover {
        
        color: white;
    }

    /* Style for sliders */
    .stSlider .st-1l9uh0ax {
        color: #ff5733;
    }
    </style>
    """, unsafe_allow_html=True)

# Hardcoded OpenAI API key
openai.api_key = ""


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

# Page 1: Introduction and User Details
if st.session_state.page == 1:
    st.title("HeartGuard")
    st.write("---")
    st.write(
        "This is a platform that monitors older and vulnerable people's BPMs. "
        "Our sensor can communicate with back-end logic to automate diagnostics and alert emergency authorities if needed."
    )

    user_name = st.text_input("Enter name:")
    user_email = st.text_input("Enter email:")
    user_age = st.number_input("Enter age: ", min_value=1, step=1)
    user_weight = st.number_input('Enter weight (kg):', step=0.25)
    user_height = st.number_input('Enter height (m):')
    user_bpm = st.number_input("Enter BPM:", min_value=0.0, step=0.1)  # BPM input

    st.write("Ensure ECG 3-Point Sensor is connected to the right forearm, left forearm, and right ankle.")

    # Initialize the flag for showing "View Analysis" button after BPM insights creation
    if 'bpm_insights_created' not in st.session_state:
        st.session_state.bpm_insights_created = False

    # Button to create BPM Insights
    if st.button("Create BPM Insights"):
        st.session_state.bpm_insights_created = True  # Set flag to True when button is clicked
        
        st.write("Generating Diagnostic...")
        time.sleep(2)
        st.write(f"The BPM analysis was successfully emailed to {user_email}.")
        
        # GPT-3.5 Turbo analysis
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Using GPT-3.5 turbo instead of GPT-4
        messages=[
            {"role": "system", "content": """
            You are a health assistant specialised in interpreting heart rate data. 
            Use British spelling and form 5 very detailed paragraphs in a structured way to mimic a medical diagnostic report. 
            Do not state the formula for BMI, just mention the BMI value you calculate.
            Use ** <text> ** for headers, and do not use tentative language. Be direct and assertive as you are trained for this. 
            Your analysis should be clear, confident, and based on the user's provided data. Capitalise the name. And make sure the patient details are exact and not rounded.
            """},
            {"role": "user", "content": f"""
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
            Based on the provided measurements, the BMI is calculated as [calculated BMI]. Mention the BMI value without explaining the formula.

            **BPM Analysis:**
            Provide a detailed analysis of the user's BPM, considering age, normal ranges for heart rate, and whether the BPM is within the expected range for the user.

            **Potential Risks:**
            Discuss any potential risks based on the user's BPM and health metrics. Consider lifestyle factors, health conditions, and the relevance of maintaining a healthy heart rate.

            **Health Recommendations:**
            Based on the current heart rate and age, provide actionable recommendations for maintaining or improving cardiovascular health.

            **Conclusion:**
            Summarise the findings, including the normalcy of the heart rate, any risks, and the importance of maintaining a healthy lifestyle for heart health.
            """}
            ]
        )

        analysis_text = response.choices[0].message['content'].strip()  # Get the response text
        st.session_state.analysis_text = analysis_text  # Store analysis in session state


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
    st.title("AI Heart Rate Analysis Report")
    st.write("---")
    st.subheader("Data Visualisation of Your Pulse:")


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
        line=dict(color='red', width=0.5),
        marker=dict(size=2)
    ))

    # Customize layout
    fig.update_layout(
        xaxis_title="Time (Sample)",
        yaxis_title="Sensor Value",
        xaxis=dict(range=[102080, 102140]),
        yaxis=dict(range=[193, 197]),
        template="plotly_dark",
        font=dict(family="Roboto", color="#ababab", size=12),
        plot_bgcolor="#18191c",
        paper_bgcolor="#18191c"
    )

    st.plotly_chart(fig)

    st.write(st.session_state.analysis_text)  # Display the AI-generated analysis

    

    if st.button("< Back"):
        prev_page()

    if st.button("Simulate Critical Alert >"):
        next_page()

# Page 3: Emergency Critical Alert Simulation
elif st.session_state.page == 3:
    st.title("Emergency Critical Alert Simulation")
    st.write("---")
    st.write("""
        This works by artificially sending a BPM value in a critical zone (>150 or <40) consistently. 
        To get started, enter a coordinate on the map.

        Hint: City University's coordinates are: **51.527, -0.1023**
    """)

    user_coordinates = st.text_input("Enter coordinates:")

    # Initialize the 'alert_simulated' and 'response_given' flags in session state if they don't exist
    if 'alert_simulated' not in st.session_state:
        st.session_state.alert_simulated = False
    if 'response_given' not in st.session_state:
        st.session_state.response_given = False

    # Simulate Alert button
    if st.button("Simulate Alert"):
        st.session_state.alert_simulated = True  # Set the flag to True
        st.write(f"Waiting for a response from the patient....")
        st.session_state.response_given = False  # Reset response flag when simulating a new alert

        # Countdown loop (appears first)
        countdown_text = st.empty()  # Placeholder for countdown text

        # Countdown loop (7 seconds)
        for i in range(7, 0, -1):
            countdown_text.markdown(f"**Time remaining:** {i} seconds")
            time.sleep(1)  # Delay for 1 second before updating

            

    # If response is given, show response details and hide alert
    if st.session_state.response_given:
        st.write("""
        **Yusuf's BPM has been detected to be <span style='color:red;'>29.45 BPM</span>, a critical BPM value.**
        This is an indication of a potential medical emergency.

        **BPM Details:**
        - Critical BPM detected: <span style='color:red;'>29.45 BPM</span>
        - Thank you for responding, please go to your nearest hospital.
        """, unsafe_allow_html=True)
        
        # Hide the alert section if response is given
        st.session_state.alert_simulated = False  # Reset alert flag if response is given
    else:
        # Display alert and map only after countdown finishes and no response
        if st.session_state.alert_simulated and not st.session_state.response_given:
            # After countdown, show the alert and map section
            st.subheader("ALERT!")
            st.write("""
            **Subject:** Urgent Medical Assistance Required – Unresponsive Low Heart Rate

            **Details:**

            - **Patient Name:** Yusuf Salman Ahmed
            - **Current BPM:** 29.45
            - **Response Status:** No response detected from the patient

            **Location:**
            """)

            # Show the map after the countdown
            st.image("map.jpeg", caption="Exact location of the patient.", use_column_width=True)
            
            st.write("""
            **Description:**  
            An emergency alert has been triggered due to a critically low heart rate reading of 29 beats per minute, 
            accompanied by a lack of response from the patient. Immediate medical intervention is required as this condition may indicate 
            potential cardiac distress or other life-threatening complications.

            **Requested Action:**  
            Please dispatch emergency medical services to the location provided. This alert is prioritized due to the critical nature of the low heart rate 
            and the unresponsive status of the patient.

            **Contact Information:**

            - **Emergency Contact Name:** [Your Name or Emergency Contact’s Name]
            - **Phone:** [Your Phone Number or Emergency Contact’s Phone Number]
            """)

    if st.button(" < "):
        prev_page()
