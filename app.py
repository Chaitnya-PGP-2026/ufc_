import streamlit as st
import os
from markitdown import MarkItDown
from io import BytesIO

# Initialize MarkItDown engine
md = MarkItDown()

# ... rest of your code ...

# Page configuration
st.set_page_config(page_title="Universal Doc Reader", page_icon="📄", layout="wide")

st.title("📄 Universal Document-to-Text Converter")
st.markdown("Convert Office docs, PDFs, and HTML into clean, readable Markdown.")

# --- UI: Sidebar & Settings ---
st.sidebar.header("Settings")
output_format = st.sidebar.radio("Download Format", ["Markdown (.md)", "Plain Text (.txt)"])
extension = ".md" if "Markdown" in output_format else ".txt"

# --- UI: Upload Area ---
uploaded_files = st.file_uploader(
    "Drag and drop files here", 
    type=["docx", "xlsx", "pptx", "pdf", "html", "zip"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.divider()
    
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        base_name = os.path.splitext(file_name)[0]
        
        with st.status(f"Processing {file_name}...", expanded=True) as status:
            try:
                # To handle Streamlit's UploadedFile object, we read it into memory
                # MarkItDown's convert method can handle file streams
                file_bytes = uploaded_file.getvalue()
                
                # Resilient Processing with Error Handling [3]
                # Note: MarkItDown handles web requests internally if passed a URL; 
                # for local uploads, we process the stream directly.
                result = md.convert_stream(BytesIO(file_bytes), file_ext=os.path.splitext(file_name)[1])
                converted_text = result.text_content
                
                # --- UI: Instant Preview [2] ---
                st.subheader(f"Preview: {file_name}")
                st.text_area(
                    label="Converted Content",
                    value=converted_text,
                    height=300,
                    key=f"preview_{file_name}"
                )
                
                # --- UI: Download Options [2] & [4] ---
                download_filename = f"{base_name}_converted{extension}"
                st.download_button(
                    label=f"📥 Download {download_filename}",
                    data=converted_text,
                    file_name=download_filename,
                    mime="text/markdown" if extension == ".md" else "text/plain",
                    key=f"dl_{file_name}"
                )
                status.update(label=f"✅ {file_name} processed!", state="complete")
                
            except Exception as e:
                # Resilience: Catch errors without crashing the app [3]
                status.update(label=f"⚠️ Could not read {file_name}. Please check the format.", state="error")
                st.error(f"Error details: {str(e)}")

else:
    st.info("Please upload one or more files to begin.")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Powered by Microsoft MarkItDown & Streamlit")
