import pdfkit
import tempfile
import streamlit as st
import cohere
from dotenv import load_dotenv
import os
from prompt_template import generate_prompt

load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(cohere_api_key)

st.set_page_config(page_title="Startup Pitch Assistant", page_icon="🚀")

st.title("🚀 Startup Pitch Assistant")

industry = st.text_input("🌍 Industry (e.g., Healthtech, Edtech)")
idea = st.text_area("💡 Describe your startup idea briefly")
audience = st.selectbox("🎯 Audience", ["Investors", "Accelerator", "Hackathon Judges", "VC Partner"])

if st.button("Generate Pitch"):
    with st.spinner("Thinking..."):
        prompt = generate_prompt(industry, idea, audience)
        try:
            response = co.generate(
                model="command-r-plus",
                prompt=prompt,
                max_tokens=500,
                temperature=0.7
            )

            pitch_text = response.generations[0].text
            st.markdown("### 🗣️ Pitch Output")
            st.write(pitch_text)

            # Export to PDF
            if st.button("📄 Download as PDF"):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_html:
                    html_content = f"<html><body><pre>{pitch_text}</pre></body></html>"
                    tmp_html.write(html_content.encode("utf-8"))
                    tmp_html_path = tmp_html.name

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                    pdfkit.from_file(tmp_html_path, tmp_pdf.name)
                    with open(tmp_pdf.name, "rb") as f:
                        st.download_button(
                            label="Download PDF",
                            data=f.read(),
                            file_name="startup_pitch.pdf",
                            mime="application/pdf"
                        )
        except Exception as e:
            st.error(f"Something went wrong: {e}")
