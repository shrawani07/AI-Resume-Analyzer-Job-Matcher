import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import pdfplumber
import time
import random
from resume_improver import extract_text_from_pdf, improve_resume, save_resume_as_pdf

# Load environment variables
load_dotenv()
# Streamlit UI Configuration
st.set_page_config(page_title="AI Resume & Job Matcher", layout="wide")

# Configure Google Gemini AI
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    api_key = st.text_input("🔑 Enter your Google Gemini API Key", type="password")
genai.configure(api_key=api_key)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        return text.strip() if text.strip() else "⚠️ No text extracted!"
    except Exception as e:
        st.error(f"⚠️ Direct text extraction failed: {e}")
        return ""

# Function to extract key skills from resume using AI
def extract_skills(resume_text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    You are an AI career advisor. Analyze the resume and extract only the key skills relevant to the candidate's domain.
    
    Resume:
    {resume_text}
    
    Provide the skills in a bullet point list format like this:
    - Python
    - Machine Learning
    - SQL
    - Cloud Computing
    - Data Science
    """
    try:
        response = model.generate_content(prompt)
        skills_text = response.text.strip()
        
        # Ensure AI response follows the expected format
        skills = [skill.replace("-", "").strip() for skill in skills_text.split("\n") if skill.startswith("- ")]
        
        return skills if skills else []
    except Exception as e:
        return []



# Function to analyze resume using AI
def analyze_resume(resume_text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    You are an AI HR expert. Analyze the given resume and extract:
    - Key skills
    - Job roles
    - Relevant experience
    - Strengths & Weaknesses
    - Recommendations
    - Suggested free courses with certificates

    Resume:
    {resume_text}
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error in AI analysis: {e}"

# Function to extract job role from resume using AI
def extract_job_role(resume_text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    You are an AI HR expert. Based on the resume provided, extract the most relevant job title that best fits the candidate.
    
    Resume:
    {resume_text}
    
    Provide only the job title (e.g., 'Software Engineer', 'Data Analyst', 'Marketing Manager') and nothing else.
    """
    try:
        response = model.generate_content(prompt)
        job_title = response.text.strip()
        return job_title if job_title else "General Job Search"
    except Exception as e:
        return f"Error extracting job role: {e}"

# Function to generate job search links for multiple platforms
def generate_job_search_urls(job_role):
    job_role_encoded = job_role.replace(" ", "%20")  # URL Encoding

    job_platforms = {
        "LinkedIn": f"https://www.linkedin.com/jobs/search/?keywords={job_role_encoded}",
        "Internshala": f"https://internshala.com/jobs/{job_role_encoded}-jobs",
        "Wellfound (AngelList)": f"https://angel.co/jobs?query={job_role_encoded}",
        "Naukri": f"https://www.naukri.com/{job_role_encoded}-jobs",
        "Indeed": f"https://www.indeed.com/jobs?q={job_role_encoded}",
        "Glassdoor": f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={job_role_encoded}",
    }
    
    return job_platforms



# Function to get free course links based on extracted skills
def get_free_courses(skills):
    all_courses = {
        "Agile development": "https://www.coursera.org/learn/agile-development",
        "A/B Testing": "https://www.udacity.com/course/ab-testing--ud257",
        "Babel": "https://www.udemy.com/course/babel-javascript-compiler/",
        "Bootstrap": "https://www.udemy.com/course/bootstrap-4-from-scratch-with-5-projects/",
        "Business Intelligence": "https://www.coursera.org/specializations/business-intelligence",
        "Cloud Computing": "https://www.udemy.com/course/aws-certified-cloud-practitioner/",
        "Cloudinary": "https://cloudinary.com/documentation/cloudinary_training",
        "Cybersecurity": "https://www.coursera.org/specializations/ibm-cybersecurity-analyst",
        "Data Analysis": "https://www.coursera.org/specializations/data-analysis",
        "Data Cleaning": "https://www.coursera.org/learn/data-cleaning",
        "Data Modeling": "https://www.datacamp.com/courses/data-modeling-for-beginners",
        "Data Science": "https://www.edx.org/course/data-science",
        "Data Visualization": "https://www.coursera.org/learn/datavisualization",
        "ETL": "https://www.udemy.com/course/etl-testing-training/",
        "Excel": "https://www.coursera.org/learn/excel-data-analysis",
        "Express.js": "https://www.udemy.com/course/express-js/",
        "Fullstack development": "https://www.coursera.org/specializations/full-stack-react/",
        "Git": "https://www.udemy.com/course/git-and-github-crash-course/",
        "GraphQL": "https://www.udemy.com/course/graphql-by-example/",
        "HTML/CSS": "https://www.coursera.org/learn/html-css-javascript-for-web-developers",
        "JavaScript": "https://www.udemy.com/course/the-complete-javascript-course/",
        "JWT": "https://www.udemy.com/course/json-web-token/",
        "Leaflet": "https://leafletjs.com/",
        "Machine Learning": "https://www.coursera.org/learn/machine-learning",
        "Marketing": "https://learndigital.withgoogle.com/digitalgarage/course/digital-marketing",
        "MaterialUI": "https://mui.com/",
        "MERN stack": "https://www.udemy.com/course/mern-stack-front-to-back/",
        "MongoDB": "https://www.mongodb.com/developer/courses/introduction/",
        "Next.js": "https://nextjs.org/learn",
        "Node.js": "https://www.udemy.com/course/nodejs-the-complete-guide/",
        "NPM": "https://www.udemy.com/course/npm-the-complete-guide/",
        "Power BI": "https://www.coursera.org/learn/microsoft-power-bi",
        "Python": "https://www.coursera.org/learn/python",
        "Python (Pandas, NumPy)": "https://www.coursera.org/learn/data-analysis-with-python",
        "React.js": "https://www.udemy.com/course/react-redux/",
        "Redux": "https://www.udemy.com/course/redux-and-react/",
        "RESTful APIs": "https://www.udemy.com/course/rest-api-design/",
        "SQL": "https://www.datacamp.com/courses/introduction-to-sql",
        "Statistical Analysis": "https://www.coursera.org/learn/statistical-analysis-in-python",
        "Tailwind CSS": "https://tailwindcss.com/docs/installation",
        "TypeScript": "https://www.udemy.com/course/typescript/",
        "Web Development": "https://www.freecodecamp.org/learn",
        "Webpack": "https://www.udemy.com/course/webpack-5-course/",
    }
    suggested_courses = {skill: all_courses.get(skill) for skill in skills if skill in all_courses}
    return suggested_courses

# Function to calculate resume score
def calculate_resume_score(resume_text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    You are an AI HR expert. Evaluate the given resume based on:
    - Clarity and structure
    - Relevance of skills and experience
    - Industry fit
    - Overall presentation
    
    Provide a resume score between 0 and 100, followed by a brief reason.

    Resume:
    {resume_text}
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error calculating resume score: {e}"

# Function to generate a career roadmap based on skills
def generate_career_roadmap(skills):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    You are an AI career advisor. Based on the following key skills, generate a structured career roadmap, including:
    - Recommended roles
    - Next steps for skill improvement
    - Certifications that can boost credibility
    - Industry trends to watch
    
    Skills: {', '.join(skills)}
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "⚠️ Error generating career roadmap."



# Sidebar Navigation
with st.sidebar:
    st.title("📌 AI Resume Analyzer")
    st.markdown("### Navigate:")
    page = st.radio("Go to:", ["🏠 Home", "📄 Resume Analysis", "🎓 Career Roadmap & Courses", "🔗 Job Opportunities" , "✍️ Resume Improvement"])

# Home Page
if page == "🏠 Home":
    st.title("🚀 Welcome to AI Resume & Job Matcher")
    st.write("📤 Upload your resume, get AI-powered insights, and explore job opportunities!")
    st.image("AI.webp",  width=300)
    st.markdown("### Features:")
    st.write("✅ AI-powered resume analysis")
    st.write("✅ Career roadmap & free courses based on your skills")
    st.write("✅ Find the best job matches on Multiple platforms")
    st.write("✅ Improvements in resume")

# Resume Analysis Page
elif page == "📄 Resume Analysis":
    st.title("📂 Upload Resume for Analysis")
    uploaded_file = st.file_uploader("📤 Upload your resume (PDF)", type=["pdf"])

    if uploaded_file:
        st.success("✅ Resume uploaded successfully!")
        with open("uploaded_resume.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        resume_text = extract_text_from_pdf("uploaded_resume.pdf")
        if st.button("🔍 Analyze Resume"):
            with st.spinner("Processing... ⏳"):
                analysis = analyze_resume(resume_text)
                st.subheader("📌 Resume Analysis")
                st.write(analysis)
                
                # Display Resume Score
                st.subheader("📊 Resume Score")
                resume_score = calculate_resume_score(resume_text)
                st.write(resume_score)

# Career Roadmap & Free Courses Page
if page == "🎓 Career Roadmap & Courses":
    st.title("🎓 Career Roadmap & Free Courses")
    uploaded_file = st.file_uploader("📤 Upload your resume (PDF)", type=["pdf"])
    
    if uploaded_file:
        st.success("✅ Resume uploaded successfully!")
        with open("uploaded_resume.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        resume_text = extract_text_from_pdf("uploaded_resume.pdf")
        skills = extract_skills(resume_text)
        
        if skills:
            st.subheader("📌 Career Roadmap")
            career_roadmap = generate_career_roadmap(skills)
            st.write(career_roadmap)
            
            st.subheader("📚 Suggested Free Courses with Certificates")
            courses = get_free_courses(skills)
            for skill, course in sorted(courses.items()):
                st.markdown(f"✅ **{skill}**: [Enroll Here]({course})")
        else:
            st.warning("⚠️ No skills detected in the resume. Please try another file.")

# Job Search Page with Multiple Platforms
if page == "🔗 Job Opportunities":
    st.title("🔍 Find Jobs on Multiple Platforms")
    uploaded_file = st.file_uploader("📤 Upload your resume (PDF)", type=["pdf"])

    if uploaded_file:
        st.success("✅ Resume uploaded successfully!")
        with open("uploaded_resume.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        resume_text = extract_text_from_pdf("uploaded_resume.pdf")
        job_role = extract_job_role(resume_text)
        
        st.subheader("🎯 Best Matched Job Role")
        st.write(f"🔹 **{job_role}**")

        # Generate job links for multiple platforms
        job_urls = generate_job_search_urls(job_role)

        st.subheader("🌍 Explore Job Opportunities")
        for platform, url in job_urls.items():
            st.markdown(f"✅ [{platform} Jobs]({url})")


        # Section for All Job Platforms (Always Visible)
        st.subheader("📌 Explore More Job Platforms")
        st.markdown("""
    - [Monster Jobs](https://www.monster.com/jobs/)
    - [Turing Jobs](https://www.turing.com/jobs)
    - [FlexJobs](https://www.flexjobs.com/)
    - [Remotive](https://remotive.io/)
    - [We Work Remotely](https://weworkremotely.com/)
    - [Jobspresso](https://jobspresso.co/)
    - [Hired](https://hired.com/)
    - [Outsourcely](https://www.outsourcely.com/)
    - [Dice Jobs](https://www.dice.com/)
""")


# Resume Improvement Page
if page == "✍️ Resume Improvement":
    st.title("📝 Improve Your Resume")

    uploaded_file = st.file_uploader("📤 Upload your resume (PDF)", type=["pdf"])
    
    if uploaded_file:
        with open("uploaded_resume.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success("✅ Resume uploaded successfully!")
        resume_text = extract_text_from_pdf("uploaded_resume.pdf")
        
        if resume_text and "⚠️" not in resume_text:
            improved_resume_text = improve_resume(resume_text)
            output_pdf_path = "improved_resume.pdf"
            save_resume_as_pdf(improved_resume_text, output_pdf_path)
            
            st.subheader("📄 Your Improved Resume is Ready!")
            st.download_button(
                label="📥 Download Improved Resume",
                data=open(output_pdf_path, "rb"),
                file_name="Improved_Resume.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("⚠️ No text extracted from the resume. Please upload a proper resume.")