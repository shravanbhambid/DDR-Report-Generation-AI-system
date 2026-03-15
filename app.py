import streamlit as st
import fitz  # PyMuPDF
from llm_client import DDRGenerator
import time
import docx

# --- Helper Functions ---
def extract_text_from_upload(uploaded_file) -> str:
    """Extracts text from a Streamlit UploadedFile (PDF or TXT) in memory."""
    if uploaded_file.name.lower().endswith(".pdf"):
        text_content = []
        try:
            # Read from memory stream
            with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    text_content.append(page.get_text())
            return "\n".join(text_content)
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
            return ""
    elif uploaded_file.name.lower().endswith(".docx"):
        try:
            doc = docx.Document(uploaded_file)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            st.error(f"Error reading DOCX: {e}")
            return ""
    else:  # Assumes .txt
        try:
            return uploaded_file.getvalue().decode("utf-8")
        except Exception as e:
            st.error(f"Error reading TXT: {e}")
            return ""

# --- App Configuration ---
st.set_page_config(
    page_title="DDR Generator AI",
    page_icon="🏗️",
    layout="wide"
)

# --- UI Header ---
st.title("🏗️ Detailed Diagnostic Report (DDR) AI Generator")
st.markdown("Upload your existing **Site Inspection** and **Thermal Imaging** reports. Our AI will automatically merge them into a single, standardized, client-ready DDR.")

st.divider()

# --- Sidebar / Input Section ---
st.sidebar.header("1. Upload Documents")
inspection_file = st.sidebar.file_uploader("📋 Upload Site Inspection Report", type=["pdf", "txt", "docx"])
thermal_file = st.sidebar.file_uploader("🔥 Upload Thermal Imaging Report", type=["pdf", "txt", "docx"])

# --- Main Logic ---
col1, col2 = st.columns([1, 1])

if inspection_file and thermal_file:
    st.sidebar.success("Both files uploaded successfully!")
    
    if st.sidebar.button("⚙️ Generate DDR Report", type="primary", use_container_width=True):
        
        with st.spinner("Extracting text from documents..."):
            inspection_text = extract_text_from_upload(inspection_file)
            thermal_text = extract_text_from_upload(thermal_file)
            
        if not inspection_text or not thermal_text:
            st.error("Failed to extract text from one or both files. Please check the file formats.")
            st.stop()
            
        with st.spinner("🧠 AI is analyzing the reports and drafting the DDR... (This may take 30-60 seconds)"):
            try:
                generator = DDRGenerator()
                start_time = time.time()
                report_markdown = generator.generate_report(inspection_text, thermal_text)
                end_time = time.time()
                
                # Store report in session state so it doesn't disappear on re-render
                st.session_state["generated_report"] = report_markdown
                st.session_state["generation_time"] = round(end_time - start_time, 2)
                
            except Exception as e:
                st.error(f"An error occurred during generation: {e}")
else:
    st.info("👈 Please upload both a Site Inspection Report and a Thermal Imaging Report from the sidebar to begin.")

# --- Results Section ---
if "generated_report" in st.session_state:
    st.toast("Report Generation Complete!", icon="✅")
    
    st.subheader("📄 Generated DDR Report")
    
    # Action Buttons row
    action_col1, action_col2 = st.columns([1, 5])
    with action_col1:
        st.download_button(
            label="💾 Download as Markdown",
            data=st.session_state["generated_report"],
            file_name="DDR_Report.md",
            mime="text/markdown",
            use_container_width=True
        )
    with action_col2:
        st.caption(f"⏱️ Generated in {st.session_state['generation_time']} seconds.")
        
    # Render the markdown report
    st.markdown("---")
    st.markdown(st.session_state["generated_report"])
    st.markdown("---")
