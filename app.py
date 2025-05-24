import streamlit as st
import requests
# OpenRouter API setup
API_KEY = "OPEN_ROUTER_KEY"
URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
def convert_code(legacy_code, language):
    if not legacy_code.strip():
        return "Error: No code provided."
    prompt = f"Convert this {language} code to Python:\n```\n{legacy_code}\n```\nEnsure the Python code is functional. Add English comments for each line.\nFormat comments like: # [comment]"
    data = {"model": "qwen/qwen3-32b", "provider": {"only": ["Cerebras"]}, "messages": [{"role": "system", "content": "You are a code modernization expert."}, {"role": "user", "content": prompt}]}
    try:
        response = requests.post(URL, headers=HEADERS, json=data)
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "Error: API call failed."
st.title("Legacy Code Converter 🕰️")
st.write("Select a legacy language and paste your code to convert to Python!")
# Dropdown for selecting legacy language
language = st.selectbox("Select Legacy Language:", ["COBOL", "Fortran", "PL/I"])
legacy_code = st.text_area(f"{language} Code:", height=150)
if st.button("Convert"):
    if legacy_code:
        with st.spinner("Converting..."):
            result = convert_code(legacy_code, language)
            if result.startswith("Error"):
                st.error(result)
            else:
                st.markdown("### Python Code")
                st.code(result, language="python")
    else:
        st.error(f"Enter {language} code!")
st.write("Cerebras & OpenRouter Qwen 3 Hackathon. #CodeConverter")
