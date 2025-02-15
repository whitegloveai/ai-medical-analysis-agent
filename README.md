# 🩻 Medical Imaging Diagnosis Agent

Use Case: 
- Equip nurses to streamline radiology workflows in hospitals by having prelimnary analysis for Doctors and speed care time.
- Radiology analysis is a bottleneck in operational effeciency of Hospitals

## Features

- **Comprehensive Image Analysis**
  - Image Type Identification (X-ray, MRI, CT scan, ultrasound)
  - Anatomical Region Detection
  - Key Findings and Observations
  - Potential Abnormalities Detection
  - Image Quality Assessment
  - Research and Reference

## How to Run

1. **Setup Environment**
   ```bash
   # Clone the repository
   git clone https://github.com/whitegloveai/ai-medical-analysis-agent.git
   cd ai-medical-analysis-agent

   # Install dependencies
   uv pip install -r requirements.txt
   ```

2. **Configure API Keys**
   - Get Google API key from [Google AI Studio](https://aistudio.google.com)

3. **Run the Application**
   ```bash
   streamlit run ai-medical-analysis-team.py
   ```

## Analysis Components

- **Image Type and Region**
  - Identifies imaging modality
  - Specifies anatomical region

- **Key Findings**
  - Systematic listing of observations
  - Detailed appearance descriptions
  - Abnormality highlighting

- **Diagnostic Assessment**
  - Potential diagnoses ranking
  - Differential diagnoses
  - Severity assessment

- **Patient-Friendly Explanations**
  - Simplified terminology
  - Detailed first-principles explanations
  - Visual reference points

## Notes

- Uses Gemini 2.0 Flash for analysis
- Requires stable internet connection
- API usage costs apply
- For educational and development purposes only
- Not a replacement for professional medical diagnosis

## Disclaimer

This tool is for educational and informational purposes only. All analyses should be reviewed by qualified healthcare professionals. Do not make medical decisions based solely on this analysis.
