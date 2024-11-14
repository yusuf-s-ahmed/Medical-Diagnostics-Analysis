import streamlit as st
from fastapi import FastAPI
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

app = FastAPI()
# Define the schema for BPM data
class BPMData(BaseModel):
    bpm: float
# Create an endpoint that accepts POST requests with BPM data
@app.post("/bpm")
async def receive_bpm(data: BPMData):
    # Here you can store or process the BPM data as needed
    print(f"Received BPM: {data.bpm}")
    return {"message": "BPM received successfully"}

# Helper function to play alert sound (HTML integration)
def play_alert_sound():
    alert_sound_html = """
    <audio autoplay>
        <source src="https://www.soundjay.com/button/beep-07.wav" type="audio/wav">
        Your browser does not support the audio element.
    </audio>
    """
    st.markdown(alert_sound_html, unsafe_allow_html=True)

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
    st.title("AI Heart Rate Monitor")
    st.write("---")
    st.write(
        "This is a platform that monitors older and vulnerable people's BPMs. "
        "Our sensor can communicate with back-end logic to automate diagnostics and alert a siren, "
        "emergency authorities, and pinpoint your exact location on the map if no response by the wearer of the device is given."
    )

    user_name = st.text_input("Enter name:")
    user_email = st.text_input("Enter email:")
    user_weight = st.number_input('Enter weight (kg):', step=0.25)
    user_height = st.number_input('Enter height (m):')

    st.write("Ensure ECG 3-Point Sensor is connected to the right forearm, left forearm, and right ankle.")

    # Initialize the flag for showing "View Analysis" button after BPM insights creation
    if 'bpm_insights_created' not in st.session_state:
        st.session_state.bpm_insights_created = False

    # Button to create BPM Insights
    if st.button("Create BPM Insights"):
        st.session_state.bpm_insights_created = True  # Set flag to True when button is clicked
        st.write(f"The BPM analysis was successfully emailed to {user_email}.")

    # Show the "View Analysis" button only if the "Create BPM Insights" button was clicked
    if st.session_state.bpm_insights_created:
        if 'view_analysis_triggered' not in st.session_state:
            st.session_state.view_analysis_triggered = False
        
        # When the user clicks "View Analysis", transition to next page
        if st.button("View Analysis >") and not st.session_state.view_analysis_triggered:
            st.session_state.view_analysis_triggered = True  # Set this flag to ensure transition happens only once
            next_page()  # Transition to the next page immediately

    


    




# Page 2: AI Overview
elif st.session_state.page == 2:
    st.title("Heart Rate Analysis Report")
    st.write("---")
    st.write("""BPM: **87.38**""")
    
    


    # Create a Plotly figure
    fig = go.Figure()

    # Add a line plot with a thinner red line
    fig.add_trace(go.Scatter(
        x=x, 
        y=y, 
        mode='lines+markers', 
        name='Value 1', 
        line=dict(color='red', width=0.5),  # Thinner line width
        marker=dict(size=2)
    ))

    st.subheader("Average Pulse Data Visualisation")

    # Customize the layout to match the app's theme
    fig.update_layout(
        
        xaxis_title="Time (Sample)",
        yaxis_title="Sensor Value",
        xaxis=dict(range=[102080, 102140]),  # Set range similar to your screenshot
        yaxis=dict(range=[193, 197]),
        template="plotly_dark",
        font=dict(family="Roboto", color="#ababab", size=12),  # Font styling to match the app
        plot_bgcolor="#18191c",  # Background color to match the Streamlit app
        paper_bgcolor="#18191c"  # Overall chart background
    )

    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig)

    

    
    st.write("Your measured heart rate is **87.38 BPM**.")  

    st.write("### Percentile Comparison")
    st.write("""
        Your heart rate falls within the **16th percentile** for your age group. 
        This means that approximately **78% of 18-year-olds** (within the 18-21 age range) 
        have a lower resting heart rate than you.
    """)

    st.write("### Interpretation of Your Resting Heart Rate")
    st.write("""
        A resting heart rate between **60-100 beats per minute** is generally considered normal for most adults. 
        For young adults like yourself (18-21 years old), resting heart rates can vary widely based on fitness level, lifestyle, 
        and genetics. 
    """)

    st.write("### Health and Fitness Insights")
    st.write("""
        - **Slightly Higher than Average**: Your heart rate is on the higher end of the average range, which could be due to various factors, 
        including stress, caffeine intake, hydration levels, or physical conditioning.
      
        - **Impact of Physical Activity**: Individuals who are physically active or athletes often have lower resting heart rates, 
        sometimes as low as 40-60 BPM, due to the heart’s increased efficiency.

        - **Considerations for Health Monitoring**: A slightly elevated resting heart rate isn’t necessarily a cause for concern, 
        but monitoring it over time can be useful. If it frequently exceeds 100 BPM at rest, consulting a healthcare provider may be beneficial.
    """)

    st.write("### Tips for Maintaining a Healthy Heart Rate")
    st.write("""
        - **Regular Exercise**: Engaging in cardiovascular activities, such as running, swimming, or cycling, 
        can improve your heart’s efficiency and lower your resting heart rate.
    
        - **Manage Stress**: Chronic stress can elevate your heart rate. Practices like meditation, deep breathing exercises, 
        and adequate sleep can help maintain a healthy heart rate.
    
        - **Stay Hydrated**: Dehydration can lead to an increased heart rate as your heart works harder to pump blood. 
        Ensuring you drink enough water daily can help stabilize it.
    """)    

    st.write("### Conclusion")
    st.write("""
        Overall, your heart rate is within the normal range but slightly higher than average for your age group. 
        Maintaining a healthy lifestyle through regular exercise, stress management, and proper hydration can help 
        keep your heart rate within an optimal range.
    """)


    if st.button("<"):
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
        st.write("Waiting for a response from Yusuf....")
        st.session_state.response_given = False  # Reset response flag when simulating a new alert

        # Countdown loop (appears first)
        countdown_text = st.empty()  # Placeholder for countdown text

        # Countdown loop (7 seconds)
        for i in range(7, 0, -1):
            countdown_text.markdown(f"**Time remaining:** {i} seconds")
            time.sleep(1)  # Delay for 1 second before updating

            # If no response, proceed to alert
            if not st.session_state.response_given and i == 1:
                st.session_state.page = 5  # Trigger alert view within same page
                st.write("No response detected, alert triggered!")
                play_alert_sound()  # Play alert sound
                break

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
