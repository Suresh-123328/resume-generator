import streamlit as st
import google.generativeai as genai

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

def generate_resume(name, job_title):
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
    )

    context = f"""
    name: {name}
    job_title: {job_title}
    Write a complete professional resume based on the above details.
    Include summary, skills, dummy experience, education, and projects.
    Output in Markdown format.
    """
    chat_session = model.start_chat(history=[{"role": "user", "parts": [context]}])
    response = chat_session.send_message(context)
    text = (
        response.candidates[0].content
        if isinstance(response.candidates[0].content, str)
        else response.candidates[0].content.parts[0].text
    )
    return text

def clean_resume_text(text):
    cleaned_text = text.replace("[Add Email Address]", "[Your Email Address]")
    cleaned_text = cleaned_text.replace("[Add Phone Number]", "[Your Phone Number]")
    cleaned_text = cleaned_text.replace("[Add LinkedIn Profile URL (optional)]", "[Your LinkedIn URL]")
    cleaned_text = cleaned_text.replace("[University Name]", "[Your University]")
    cleaned_text = cleaned_text.replace("[Graduation Year]", "[Your Graduation Year]")
    return cleaned_text

st.title("AI Resume Generator")
name = st.text_input("Enter your name")
job_title = st.text_input("Enter your job title")

if st.button("Generate Resume"):
    if name and job_title:
        resume = generate_resume(name, job_title)
        final_resume = clean_resume_text(resume)
        st.markdown(final_resume)
    else:
        st.warning("Please enter both name and job title.")