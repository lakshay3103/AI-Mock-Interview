from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Alex Developer', 0, 1, 'C')
        self.set_font('Arial', '', 12)
        self.cell(0, 10, 'Junior AI/ML Engineer | Python Expert', 0, 1, 'C')
        self.ln(5)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 5, body)
        self.ln()

# Create PDF
pdf = PDF()
pdf.add_page()

# 1. Summary (Heavily Keyword Optimized)
pdf.chapter_title("Professional Summary")
pdf.chapter_body(
    "Passionate Junior AI Engineer with strong proficiency in Python and Machine Learning. "
    "Experience building RAG pipelines using LangChain and Pinecone. "
    "Skilled in deploying models with FastAPI and Docker. "
    "Eager to join NexusFlow Tech to build FinTech AI solutions."
)

# 2. Technical Skills
pdf.chapter_title("Technical Skills")
pdf.chapter_body(
    "- Languages: Python (Advanced), SQL, C++\n"
    "- Machine Learning: TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy\n"
    "- GenAI & LLMs: LangChain, OpenAI API, Gemini, RAG, Pinecone, Prompt Engineering\n"
    "- Deployment: Docker, Git, GitHub, FastAPI, Flask, AWS Basics"
)

# 3. Projects (Matching the JD Responsibilities)
pdf.chapter_title("Projects")
pdf.chapter_body(
    "1. AI Financial Chatbot (RAG & LangChain)\n"
    "   - Built a chatbot to answer customer queries using LangChain and OpenAI.\n"
    "   - Implemented RAG (Retrieval Augmented Generation) with Pinecone vector DB.\n"
    "   - Deployed backend using FastAPI and Docker.\n\n"
    "2. Customer Churn Prediction Model\n"
    "   - Preprocessed large datasets using Pandas and NumPy.\n"
    "   - Trained Random Forest and Logistic Regression models (Scikit-learn).\n"
    "   - Achieved 85% accuracy in predicting customer drop-offs."
)

# 4. Education
pdf.chapter_title("Education")
pdf.chapter_body(
    "B.Tech in Computer Science\n"
    "XYZ Institute of Technology (2022 - 2026)\n"
    "CGPA: 8.5/10"
)

# Output
pdf.output("perfect_resume.pdf")
print("✅ Success! 'perfect_resume.pdf' has been created in your folder.")