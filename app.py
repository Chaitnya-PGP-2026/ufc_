import streamlit as st
import os
import pandas as pd
from markitdown import MarkItDown
from io import BytesIO

# Initialize MarkItDown engine
md = MarkItDown()

def format_size(size_bytes):
    """Convert bytes to a readable MB string."""
    mb = size_bytes / (1024 * 1024)
    return f"{mb:.2f} MB"

# Page configuration
st.set_page_config(page_title="Universal Doc Reader", page_icon="📄", layout="wide")

st.title("📄 Universal Document-to-Text Converter")

# --- UI: Sidebar ---
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
    for uploaded_file in uploaded_files:
        st.divider()
        st.subheader(f"📁 File: {uploaded_file.name}")
        
        # Create Tabs
        tab1, tab2 = st.tabs(["📄 Document Preview", "📊 File Size Comparison"])
        
        try:
            # Process File
            file_bytes = uploaded_file.getvalue()
            original_size = len(file_bytes)
            
            result = md.convert_stream(BytesIO(file_bytes), file_ext=os.path.splitext(uploaded_file.name)[1])
            converted_text = result.text_content
            converted_size = len(converted_text.encode('utf-8'))
            
            # --- TAB 1: PREVIEW ---
            with tab1:
                st.text_area("Converted Content", value=converted_text, height=400, key=f"text_{uploaded_file.name}")
                
                download_filename = f"{os.path.splitext(uploaded_file.name)[0]}_converted{extension}"
                st.download_button(
                    label=f"📥 Download {download_filename}",
                    data=converted_text,
                    file_name=download_filename,
                    mime="text/plain",
                    key=f"dl_{uploaded_file.name}"
                )

            # --- TAB 2: SIZE COMPARISON ---
            with tab2:
                # Calculate percentage reduction
                reduction = ((original_size - converted_size) / original_size) * 100
                
                # Create Comparison Table
                comparison_data = {
                    "File Version": ["Original File", "Converted Text"],
                    "Size": [format_size(original_size), format_size(converted_size)]
                }
                df = pd.DataFrame(comparison_data)
                
                st.table(df)
                
                if reduction > 0:
                    st.success(f"**Efficiency:** Text version is {reduction:.1f}% smaller.")
                else:
                    st.info("The text version is roughly the same size as the original.")

        except Exception as e:
            st.error(f"⚠️ Could not read {uploaded_file.name}. Please check the format.")
            st.caption(f"Error details: {str(e)}")
else:
    st.info("Please upload one or more files to begin.")
