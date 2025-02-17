import os
import io
from dotenv import load_dotenv
import streamlit as st
from agno.agent import Agent
from agno.media import Image as AgnoImage
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from PIL import Image as PILImage

# Load environment variables from .env file
load_dotenv()

# Check for GOOGLE_API_KEY in .env or Streamlit secrets
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    st.session_state.GOOGLE_API_KEY = GOOGLE_API_KEY
else:
    GOOGLE_API_KEY = None

# Streamlit UI
st.sidebar.title("ℹ️ Configuration")

if not GOOGLE_API_KEY:
    api_key = st.sidebar.text_input("Enter your Google API Key:", type="password")
    st.sidebar.caption(
        "Get your API key from [Google AI Studio](https://aistudio.google.com/apikey) 🔑"
    )
    if api_key:
        GOOGLE_API_KEY = api_key
        st.session_state.GOOGLE_API_KEY = GOOGLE_API_KEY
        st.success("API Key saved!")
        st.rerun()
else:
    st.sidebar.success("API Key is configured")
    if st.sidebar.button("🔄 Reset API Key"):
        st.session_state.GOOGLE_API_KEY = None
        st.rerun()

st.sidebar.info(
    "This tool provides AI-powered analysis of medical imaging data using advanced computer vision and radiological expertise."
)
st.sidebar.warning(
    "⚠DISCLAIMER: This tool is for educational and informational purposes only. All analyses should be reviewed by qualified healthcare professionals. Do not make medical decisions based solely on this analysis."
)


# Initialize Agno Agent
if GOOGLE_API_KEY:
    agent = Agent(
        model=Gemini(id="gemini-2.0-flash-exp", api_key=GOOGLE_API_KEY),
        tools=[DuckDuckGoTools()],
        markdown=True,
    )
else:
    agent = None
    st.warning("Please configure your API key in the sidebar to continue")


# Medical Analysis Query (Structured for better parsing)
QUERY = """You are a highly skilled medical imaging expert. Analyze the patient's medical image. Provide a structured report with these sections:

1.  **Image Type & Region:**
    *   Imaging Modality: (e.g., X-ray, MRI, CT, Ultrasound)
    *   Anatomical Region: (e.g., Chest, Abdomen, Brain)
    *   Positioning: (e.g., AP, PA, Lateral)
    *   Image Quality: (e.g., Adequate, Suboptimal - explain why)

2.  **Key Findings:**
    *   (Systematic list of observations. Be precise. Include measurements, densities, and characteristics of abnormalities. Use bullet points.)

3.  **Diagnostic Assessment:**
    *   Primary Diagnosis: (with confidence level: High, Moderate, Low)
    *   Differential Diagnoses: (in order of likelihood)
    *   Supporting Evidence: (for each diagnosis, cite specific image findings)

4.  **Patient-Friendly Explanation:**
    *   (Explain the findings in simple language, avoiding jargon. Include visual analogies if helpful.)

5.  **Research Context:**
    *   (Use DuckDuckGo to find relevant medical literature, treatment protocols, and technological advances. Provide 2-3 key references with links.)

Format your response using markdown.
"""


st.title("🏥 Medical Imaging Diagnosis Agent")
st.write("Upload a medical image for professional analysis")

# Upload Image
uploaded_file = st.file_uploader(
    "Upload Medical Image",
    type=["jpg", "jpeg", "png", "dicom"],
    help="Supported formats: JPG, JPEG, PNG, DICOM",
)


if uploaded_file is not None:
    try:
        image = PILImage.open(uploaded_file)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            resized_image = image.resize((500, int(500 * image.height / image.width)))
            st.image(resized_image, caption="Uploaded Medical Image", use_container_width=True)

        if st.button("🔍 Analyze Image", type="primary", use_container_width=True):
            if agent:
                with st.spinner("Analyzing image..."):
                    # Save the image to a temporary file to get its URL
                    temp_image_path = "temp_image.jpg"
                    image.save(temp_image_path)
                    
                    # Create an Agno Image object with the correct filepath parameter
                    agno_image = AgnoImage(filepath=os.path.abspath(temp_image_path))
                    
                    # Create a placeholder for streaming output
                    response_placeholder = st.empty()
                    
                    # Get the analysis using the agent with streaming
                    response_stream = agent.run(
                        QUERY,
                        images=[agno_image],
                        stream=True
                    )
                    
                    # Initialize full response
                    full_response = ""
                    
                    # Stream the response
                    for chunk in response_stream:
                        if hasattr(chunk, 'content') and chunk.content:
                            full_response += str(chunk.content)
                            response_placeholder.markdown(full_response)
                    
                    # Clean up temporary file
                    os.remove(temp_image_path)
            else:
                st.error("Please configure your API key to proceed with the analysis.")
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        if "GOOGLE_API_KEY" in str(e):
            st.warning("Please check your Google API key configuration.")