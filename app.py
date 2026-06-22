import os
import json
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# =========================================
# LOAD ENV VARIABLES
# =========================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not found in .env file")
    st.stop()

# =========================================
# GROQ CLIENT
# =========================================

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="AI Code Companion",
    page_icon="🤖",
    layout="wide"
)

# =========================================
# SESSION STATE
# =========================================

if "reply" not in st.session_state:
    st.session_state.reply = ""

if "history" not in st.session_state:
    st.session_state.history = []

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None

# =========================================
# MODERN CSS
# =========================================

st.markdown("""
<style>

.stApp{
background:
linear-gradient(135deg,#050816,#0B1023,#111827);
color:white;
font-family:sans-serif;
}

/* HERO */

.hero{
padding:30px;
border-radius:25px;
background:
linear-gradient(
135deg,
rgba(79,70,229,0.25),
rgba(168,85,247,0.20),
rgba(236,72,153,0.15)
);
border:1px solid rgba(255,255,255,0.08);
margin-bottom:25px;
}

.hero h1{
font-size:48px;
margin-bottom:10px;
}

.hero p{
font-size:18px;
color:#CBD5E1;
}

/* INPUT */

.stTextArea textarea{
background:#0F172A !important;
color:white !important;
border-radius:18px !important;
border:1px solid rgba(255,255,255,0.08) !important;
font-size:15px !important;
padding:15px !important;
}

/* BUTTON */

.stButton button{
width:100%;
height:52px;
border:none;
border-radius:14px;
font-size:17px;
font-weight:700;
background:linear-gradient(90deg,#4F46E5,#9333EA,#DB2777);
color:white;
transition:0.2s;
}

.stButton button:hover{
transform:scale(1.01);
}

/* OUTPUT */

.output-box{
padding:25px;
border-radius:22px;
background:#0F172A;
border:1px solid rgba(255,255,255,0.08);
margin-top:15px;
line-height:1.8;
overflow-x:auto;
}

/* HISTORY */

.history-card{
padding:14px;
border-radius:14px;
background:#0F172A;
border:1px solid rgba(255,255,255,0.08);
margin-bottom:10px;
font-size:14px;
}

/* QUIZ */

.quiz-question{
padding:20px;
border-radius:18px;
background:#0F172A;
border:1px solid rgba(255,255,255,0.08);
margin-bottom:20px;
}

/* SIDEBAR */

section[data-testid="stSidebar"]{
background:#081120;
}

/* RADIO BUTTONS */

div[role="radiogroup"] > label{
margin-bottom:12px !important;
display:block !important;
}

/* SCROLLBAR */

::-webkit-scrollbar{
width:8px;
height:8px;
}

::-webkit-scrollbar-thumb{
background:#4F46E5;
border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# HEADER
# =========================================

st.markdown("""
<div class="hero">
<h1>🤖 AI Code Companion</h1>
<p>Explain • Convert • Learn • Quiz • Debug • Optimize</p>
</div>
""", unsafe_allow_html=True)

# =========================================
# SIDEBAR
# =========================================

with st.sidebar:

    st.title("⚙️ Settings")

    language = st.selectbox(
        "Programming Language",
        [
            "Python",
            "Java",
            "C",
            "C++",
            "JavaScript",
            "Go",
            "Rust"
        ]
    )

    action = st.selectbox(
        "Choose Feature",
        [
            "Explain Code",
            "Convert Code",
            "Detect Concepts",
            "Smart Learning Mode",
            "Debug Code",
            "Optimize Code",
            "Generate Quiz"
        ]
    )

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

# =========================================
# CODE INPUT
# =========================================

st.subheader("💻 Enter Code")

code = st.text_area(
    "",
    height=350,
    placeholder="Paste your code here..."
)

target_language = ""

if action == "Convert Code":

    target_language = st.selectbox(
        "Convert To",
        [
            "Python",
            "Java",
            "C",
            "C++",
            "JavaScript",
            "Go",
            "Rust"
        ]
    )

# =========================================
# RUN BUTTON
# =========================================

run = st.button("🚀 Run AI")

# =========================================
# PROMPT CREATION
# =========================================

def create_prompt():

    if action == "Explain Code":

        return f"""
Explain this {language} code for a {difficulty} level programmer.

Difficulty Rules:

Beginner:
- very simple English
- explain line by line
- explain basic concepts

Intermediate:
- moderate technical explanation
- explain logic clearly

Advanced:
- detailed technical explanation
- include optimization discussion
- include best practices
- include time complexity if possible

Code:
{code}
"""

    elif action == "Convert Code":

        return f"""
Convert this {language} code into {target_language}.

Maintain proper syntax and best practices.

Code:
{code}
"""

    elif action == "Detect Concepts":

        return f"""
Detect all programming concepts used in this code.

Explain concepts for a {difficulty} learner.

Difficulty Rules:

Beginner:
- simple explanation

Intermediate:
- explain logic and usage

Advanced:
- explain technical details and implementation

Code:
{code}
"""

    elif action == "Smart Learning Mode":

        return f"""
Teach concepts from this code for a {difficulty} learner.

Beginner:
- simple explanation
- real-life analogy
- easy mini examples

Intermediate:
- moderate examples
- logic explanation
- practical understanding

Advanced:
- deep technical explanation
- optimization discussion
- advanced examples

Include:
- explanations
- examples
- practice challenge

Code:
{code}
"""

    elif action == "Debug Code":

        return f"""
Debug this {language} code for a {difficulty} programmer.

Beginner:
- explain errors simply

Intermediate:
- explain logical mistakes

Advanced:
- explain optimization issues
- explain best practices
- explain edge cases

Find:
- bugs
- errors
- improvements

Provide corrected code.

Code:
{code}
"""

    elif action == "Optimize Code":

        return f"""
Optimize this {language} code for a {difficulty} programmer.

Beginner:
- improve readability

Intermediate:
- improve structure and efficiency

Advanced:
- improve performance
- reduce complexity
- apply advanced best practices

Provide optimized code.

Code:
{code}
"""

    elif action == "Generate Quiz":

        return f"""
Generate exactly 5 {difficulty} level multiple choice quiz questions from the given code.

Difficulty Rules:

Beginner:
- basic syntax questions
- easy output questions

Intermediate:
- logic-based questions
- function behavior questions

Advanced:
- tricky logic
- optimization questions
- time complexity questions

STRICT RULES:
- Return ONLY pure JSON
- Do NOT use markdown
- Each question must have 4 options

JSON FORMAT:

{{
  "title":"Programming Quiz",
  "questions":[
    {{
      "question":"Question here",
      "options":[
        "Option 1",
        "Option 2",
        "Option 3",
        "Option 4"
      ],
      "answer":"Correct Option",
      "explanation":"Short explanation"
    }}
  ]
}}

Code:
{code}
"""

# =========================================
# QUIZ PARSER
# =========================================

def parse_quiz(text):

    try:

        text = text.strip()

        text = text.replace("```json", "")
        text = text.replace("```", "")

        start = text.find("{")
        end = text.rfind("}") + 1

        if start == -1 or end == 0:
            return None

        clean_json = text[start:end]

        data = json.loads(clean_json)

        if "questions" not in data:
            return None

        for q in data["questions"]:

            if "question" not in q:
                return None

            if "options" not in q:
                return None

            if "answer" not in q:
                return None

            if "explanation" not in q:
                return None

        return data

    except Exception as e:

        st.error(f"Quiz Parse Error: {e}")

        return None

# =========================================
# RUN AI
# =========================================

if run:

    if code.strip() == "":
        st.warning("Please enter code")

    else:

        prompt = create_prompt()

        try:

            with st.spinner("AI is thinking..."):

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role":"system",
                            "content":"You are an expert coding tutor."
                        },
                        {
                            "role":"user",
                            "content":prompt
                        }
                    ],
                    temperature=0.2
                )

                result = response.choices[0].message.content

                if action == "Generate Quiz":

                    parsed_quiz = parse_quiz(result)

                    if parsed_quiz:

                        st.session_state.quiz_data = parsed_quiz
                        st.session_state.reply = ""

                    else:

                        st.session_state.quiz_data = None

                        st.session_state.reply = """
Quiz generation failed.
Please try again with different code.
"""

                else:

                    st.session_state.reply = result
                    st.session_state.quiz_data = None

                topic_line = code.split("\n")[0][:80]

                history_text = f"{action} • {language} • {topic_line}"

                st.session_state.history.insert(0, history_text)

        except Exception as e:

            st.error(f"Error: {e}")

# =========================================
# AI OUTPUT
# =========================================

if action != "Generate Quiz":

    st.subheader("🤖 AI Reply")

    if st.session_state.reply != "":

        with st.container():

            st.markdown(
                '<div class="output-box">',
                unsafe_allow_html=True
            )

            st.markdown(st.session_state.reply)

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

    else:

        st.info("AI reply will appear here")

# =========================================
# QUIZ SECTION
# =========================================

if action == "Generate Quiz":

    st.subheader("🧠 Interactive Quiz")

    if st.session_state.quiz_data:

        quiz = st.session_state.quiz_data

        for i, q in enumerate(quiz["questions"]):

            st.markdown(
                f"""
                <div class="quiz-question">
                <h4>Q{i+1}. {q["question"]}</h4>
                </div>
                """,
                unsafe_allow_html=True
            )

            selected = st.radio(
                f"Choose Answer {i+1}",
                q["options"],
                key=f"quiz_{i}"
            )

            if st.button(
                f"Submit Answer {i+1}",
                key=f"submit_{i}"
            ):

                if selected == q["answer"]:

                    st.success("✅ Correct Answer")

                else:

                    st.error("❌ Wrong Answer")

                    st.write(
                        f"Correct Answer: {q['answer']}"
                    )

                st.info(
                    f"Explanation: {q['explanation']}"
                )

            st.divider()

    else:

        st.info("Generate quiz to see interactive quiz")

# =========================================
# HISTORY
# =========================================

st.subheader("🕘 History")

if len(st.session_state.history) == 0:

    st.info("No history available")

else:

    for item in st.session_state.history:

        st.markdown(
            f"""
            <div class="history-card">
            {item}
            </div>
            """,
            unsafe_allow_html=True
        )