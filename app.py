"""
CodeMentor - Using Google Gemini (Free!)
"""

import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import warnings
import logging

# Suppress warnings and logging
warnings.filterwarnings('ignore')
logging.getLogger('absl').setLevel(logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

load_dotenv()

st.set_page_config(
    page_title="CodeMentor AI", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Animated gradient background */
    .stApp {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Main content card */
    .main .block-container {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 2.5rem 3.5rem;
        margin: 2rem auto;
        max-width: 1400px;
        box-shadow: 0 25px 80px rgba(0, 0, 0, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1e 100%);
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent;
        padding: 2rem 1.5rem;
    }
    
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p {
        color: #ffffff !important;
    }
    
    section[data-testid="stSidebar"] h2 {
        font-size: 1.4rem;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    /* Title with gradient animation */
    h1 {
        background: linear-gradient(120deg, #667eea, #764ba2, #f093fb);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shimmer 3s linear infinite;
        font-weight: 800;
        text-align: center;
        font-size: 3.5rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -1px;
    }
    
    @keyframes shimmer {
        to { background-position: 200% center; }
    }
    
    /* Section headers */
    h2 {
        color: #2d3748;
        font-weight: 700;
        font-size: 2rem;
        margin: 1.5rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    h3 {
        color: #4a5568;
        font-weight: 600;
        font-size: 1.5rem;
        margin: 1.5rem 0 1rem 0;
    }
    
    /* Input fields */
    .stTextArea textarea,
    .stTextInput input {
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 14px !important;
        font-size: 15px !important;
        transition: all 0.3s ease !important;
        background: #f8fafc !important;
    }
    
    .stTextArea textarea:focus,
    .stTextInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15) !important;
        background: white !important;
    }
    
    /* Beautiful buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 0.9rem 2.5rem !important;
        font-weight: 600 !important;
        font-size: 17px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
        width: 100%;
        letter-spacing: 0.5px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover:before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div,
    .stSelectbox [data-baseweb="select"] {
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        background: #f8fafc !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox [data-baseweb="select"]:hover {
        border-color: #667eea !important;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: rgba(102, 126, 234, 0.05);
        padding: 1rem;
        border-radius: 12px;
    }
    
    .stRadio [role="radiogroup"] label {
        padding: 0.75rem 1rem;
        border-radius: 8px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stRadio [role="radiogroup"] label:hover {
        background: rgba(102, 126, 234, 0.1);
    }
    
    /* Info/Alert boxes */
    .stAlert {
        border-radius: 12px !important;
        border-left: 5px solid #667eea !important;
        background: rgba(102, 126, 234, 0.08) !important;
        padding: 1rem 1.5rem !important;
    }
    
    /* Warning messages */
    .stWarning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%) !important;
        color: #92400e !important;
        border-radius: 12px !important;
        border-left: 5px solid #f59e0b !important;
        padding: 1rem 1.5rem !important;
        font-weight: 500;
    }
    
    /* Success messages */
    .stSuccess {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%) !important;
        color: #065f46 !important;
        border-radius: 12px !important;
        border-left: 5px solid #10b981 !important;
    }
    
    /* Code blocks */
    code {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
        color: #e11d48 !important;
        padding: 3px 8px !important;
        border-radius: 6px !important;
        font-size: 0.9em !important;
        font-weight: 500 !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    pre {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        border: 1px solid #334155 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
    }
    
    pre code {
        background: transparent !important;
        color: #e2e8f0 !important;
        border: none !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
        border-right-color: #764ba2 !important;
    }
    
    /* Dividers */
    hr {
        margin: 2.5rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent);
        opacity: 0.5;
    }
    
    /* Markdown content styling */
    .stMarkdown {
        color: #1e293b;
        line-height: 1.7;
    }
    
    .stMarkdown ul, .stMarkdown ol {
        padding-left: 1.5rem;
    }
    
    .stMarkdown li {
        margin-bottom: 0.5rem;
    }
    
    /* Slider */
    .stSlider [data-baseweb="slider"] {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1.5rem !important;
        }
        
        h1 {
            font-size: 2.5rem !important;
        }
        
        h2 {
            font-size: 1.5rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Configure Gemini with proper error handling
try:
    GOOGLE_API_KEY = os.getenv('OPENAI_API_KEY')  # Your key is here
    if not GOOGLE_API_KEY:
        st.error("❌ API Key not found! Please check your .env file.")
        st.stop()
    
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error(f"❌ Configuration error: {str(e)}")
    st.stop()

@st.cache_resource
def get_model():
    """Initialize Gemini model - using the latest free model"""
    try:
        # gemini-2.0-flash-exp is the latest free model as of Oct 2024
        return genai.GenerativeModel('gemini-2.0-flash-exp')
    except:
        # Fallback to stable version
        return genai.GenerativeModel('gemini-2.0-flash')

def generate_response(prompt):
    """Generate AI response with error handling"""
    try:
        model = get_model()
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.95,
                top_k=40,
                max_output_tokens=2048,
            )
        )
        return response.text
    except Exception as e:
        error_msg = str(e)
        if "API key" in error_msg:
            return "❌ **API Key Error:** Your API key seems invalid. Please check your .env file."
        elif "quota" in error_msg.lower():
            return "❌ **Quota Exceeded:** You've reached your API limit. Try again later."
        elif "not found" in error_msg.lower():
            return f"❌ **Model Error:** The model couldn't be found. Error: {error_msg}"
        else:
            return f"❌ **Error:** {error_msg}\n\n💡 Try refreshing the page or checking your internet connection."

# Header
st.title("🎓 CodeMentor AI")
st.markdown("""
<div style='text-align: center; margin-top: -1rem; margin-bottom: 2rem;'>
    <p style='color: #64748b; font-size: 1.15rem; font-weight: 500;'>
        Your Intelligent Programming Companion 🚀
    </p>
    <p style='color: #94a3b8; font-size: 0.95rem;'>
        Powered by Google Gemini 2.0 Flash ⚡
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    user_level = st.selectbox(
        "📊 Your Skill Level",
        ["Beginner", "Intermediate", "Advanced"],
        index=1,
        help="Choose your programming experience level"
    )
    
    language = st.selectbox(
        "💻 Programming Language",
        ["Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust", "PHP", "Swift"],
        index=0,
        help="Select the language you want help with"
    )
    
    st.markdown("---")
    st.markdown("## 🎯 Choose Feature")
    
    feature = st.radio(
        "Select what you need:",
        ["💬 Ask Questions", "🔍 Code Review", "📝 Practice Exercise", "🐛 Debug Help"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 💡 Pro Tips")
    st.info("""
    ✓ **Be specific** with questions
    
    ✓ **Include context** in code
    
    ✓ **Mention errors** you're seeing
    
    ✓ **Describe expected** behavior
    """)
    
    st.markdown("---")
    st.markdown("### 📊 About")
    st.markdown("""
    <div style='font-size: 0.85rem; line-height: 1.6;'>
        <p>✨ AI-powered tutoring</p>
        <p>🎯 Personalized learning</p>
        <p>⚡ Instant feedback</p>
        <p>🔒 100% free to use</p>
    </div>
    """, unsafe_allow_html=True)

# Main Content Area
if feature == "💬 Ask Questions":
    st.markdown("## 💬 Ask Programming Questions")
    st.markdown("Get detailed explanations with code examples and best practices.")
    
    question = st.text_area(
        "✍️ What would you like to know?",
        height=170,
        placeholder="Example: How do Python decorators work? Can you show me practical examples?",
        help="Be specific for better answers"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Get Answer", use_container_width=True):
            if question.strip():
                with st.spinner("🤔 Analyzing your question..."):
                    prompt = f"""You are an expert {language} programming tutor teaching a {user_level} level student.

**Student's Question:** {question}

Please provide a comprehensive answer that includes:

1. **Clear Explanation**: Explain the concept in simple, understandable terms
2. **Code Examples**: Provide practical, well-commented code examples
3. **Key Concepts**: Highlight the most important points to remember
4. **Common Pitfalls**: Mention mistakes beginners often make
5. **Best Practices**: Share industry-standard approaches

Format your response with proper markdown for excellent readability. Use code blocks with syntax highlighting."""

                    answer = generate_response(prompt)
                    
                    st.markdown("---")
                    st.markdown("### 📚 Your Answer")
                    st.markdown(answer)
                    
                    # Feedback buttons
                    col_a, col_b, col_c = st.columns([1, 1, 2])
                    with col_a:
                        if st.button("👍 Helpful"):
                            st.success("Thanks for the feedback!")
                    with col_b:
                        if st.button("👎 Not helpful"):
                            st.info("We'll try to improve!")
            else:
                st.warning("⚠️ Please enter your question first!")

elif feature == "🔍 Code Review":
    st.markdown("## 🔍 Professional Code Review")
    st.markdown("Get expert feedback on code quality, performance, and best practices.")
    
    code = st.text_area(
        "📋 Paste your code here:",
        height=380,
        placeholder="# Paste your code here...\n\ndef example_function():\n    # Your code\n    pass",
        help="Include complete, runnable code for best results"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔍 Review My Code", use_container_width=True):
            if code.strip():
                with st.spinner("🔍 Analyzing your code thoroughly..."):
                    prompt = f"""You are a senior {language} developer reviewing code from a {user_level} programmer.

**Code to Review:**
```{language.lower()}
{code}
```

Please provide a comprehensive code review with:

1. ✅ **Strengths**: What's well-implemented
2. ⚠️ **Issues**: Bugs, errors, or problems found
3. 💡 **Improvements**: Suggestions for better code
4. 🚀 **Performance**: Optimization opportunities
5. 📖 **Best Practices**: Industry standards to follow
6. 🔒 **Security**: Any security concerns (if applicable)

Be constructive, educational, and provide specific examples. Use proper markdown formatting."""

                    review = generate_response(prompt)
                    
                    st.markdown("---")
                    st.markdown("### 📋 Code Review Results")
                    st.markdown(review)
            else:
                st.warning("⚠️ Please paste your code first!")

elif feature == "📝 Practice Exercise":
    st.markdown("## 📝 Generate Practice Exercise")
    st.markdown("Create custom coding challenges tailored to your skill level.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        topic = st.text_input(
            "🎯 Topic or Concept:",
            placeholder="e.g., recursion, binary search, object-oriented programming",
            help="Enter the topic you want to practice"
        )
    with col2:
        difficulty = st.select_slider(
            "📊 Difficulty Level:",
            options=["Easy", "Medium", "Hard", "Expert"],
            value="Medium"
        )
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        if st.button("🎯 Generate Exercise", use_container_width=True):
            if topic.strip():
                with st.spinner("✨ Creating your personalized exercise..."):
                    prompt = f"""Create a {difficulty} level {language} coding exercise about "{topic}" for a {user_level} programmer.

Structure the exercise as follows:

1. 📋 **Problem Statement**: Clear, concise description of the task
2. 📥 **Input/Output Examples**: Provide 2-3 test cases with expected results
3. 💡 **Hints**: Helpful tips without revealing the solution
4. ✅ **Solution**: Complete, well-commented code solution
5. 🎓 **Explanation**: Step-by-step breakdown of how the solution works
6. 🚀 **Extensions**: Optional challenges to take it further

Make it educational, engaging, and appropriately challenging. Use proper markdown formatting with code blocks."""

                    exercise = generate_response(prompt)
                    
                    st.markdown("---")
                    st.markdown("### 🎯 Your Coding Exercise")
                    st.markdown(exercise)
                    
                    st.markdown("---")
                    st.info("💡 **Tip:** Try solving it yourself first before looking at the solution!")
            else:
                st.warning("⚠️ Please enter a topic first!")

elif feature == "🐛 Debug Help":
    st.markdown("## 🐛 Debug Your Code")
    st.markdown("Let AI help you identify and fix bugs in your code.")
    
    buggy_code = st.text_area(
        "📋 Your buggy code:",
        height=280,
        placeholder="# Paste the code that's not working...\n\ndef broken_function():\n    # Your buggy code here\n    pass",
        help="Include the complete code that's causing issues"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        error_msg = st.text_area(
            "❌ Error message (if any):",
            height=120,
            placeholder="Paste the complete error message here...",
            help="Include stack traces and error details"
        )
    with col2:
        description = st.text_area(
            "✨ Expected behavior:",
            height=120,
            placeholder="Describe what should happen...",
            help="Explain what you want the code to do"
        )
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        if st.button("🔧 Debug My Code", use_container_width=True):
            if buggy_code.strip():
                with st.spinner("🔍 Debugging your code..."):
                    prompt = f"""You are a debugging expert helping a {user_level} {language} programmer.

**Buggy Code:**
```{language.lower()}
{buggy_code}
```

**Error Message:** {error_msg if error_msg.strip() else "Not provided"}

**Expected Behavior:** {description if description.strip() else "Not specified"}

Please provide detailed debugging help:

1. 🐛 **Problem Identification**: Explain exactly what's wrong
2. 🔧 **Fixed Code**: Provide the corrected, working code
3. 💡 **Explanation**: Explain why it failed and how the fix works
4. 📚 **Learning Points**: Key concepts to remember
5. 🛡️ **Prevention**: Tips to avoid this error in the future
6. 🧪 **Testing**: Suggest test cases to verify the fix

Be clear, educational, and thorough. Use proper markdown formatting with code blocks."""

                    debug_help = generate_response(prompt)
                    
                    st.markdown("---")
                    st.markdown("### 🔧 Debug Analysis & Solution")
                    st.markdown(debug_help)
            else:
                st.warning("⚠️ Please paste your buggy code first!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem 0 1rem 0;'>
    <p style='font-size: 1rem; color: #64748b; font-weight: 500; margin-bottom: 0.5rem;'>
        💡 <strong>Pro Tip:</strong> The more context you provide, the better the AI can help you!
    </p>
    <p style='font-size: 0.85rem; color: #94a3b8; margin-top: 1rem;'>
        Made with ❤️ using Streamlit & Google Gemini 2.0 Flash
    </p>
    <p style='font-size: 0.75rem; color: #cbd5e1; margin-top: 0.5rem;'>
        © 2024 CodeMentor AI • Free Educational Tool
    </p>
</div>
""", unsafe_allow_html=True)