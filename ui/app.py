import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import streamlit as st
from streamlit_option_menu import option_menu

from ai_engine.llm_client import PydanticAILLMClient
from ai_engine.test_generator import TestGenerator

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Powered Test Automation for IRCTC",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CUSTOM CSS (Railway Style + Glassmorphism)
# ---------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Main Background */

[data-testid="stAppViewContainer"]{
    background:
    linear-gradient(
        135deg,
        #140606 0%,
        #2B0C0C 35%,
        #451111 70%,
        #1A0F0F 100%
    );
    color:white;
}

/* Sidebar */

section[data-testid="stSidebar"]{
    background:
    linear-gradient(
        180deg,
        #090909 0%,
        #121212 100%
    );
    border-right:1px solid rgba(255,255,255,0.08);
}

/* Hide Streamlit Header */

header[data-testid="stHeader"]{
    background:transparent;
}

/* Main Hero Section */

.hero-section{

    text-align:center;

    padding:50px 40px;

    border-radius:28px;

    background:
    linear-gradient(
        135deg,
        rgba(255,140,66,0.18),
        rgba(150,40,20,0.18)
    );

    backdrop-filter:blur(25px);

    border:1px solid rgba(255,255,255,0.08);

    margin-bottom:30px;
}

.hero-section h1{

    font-size:72px;

    font-weight:800;

    color:white;

    line-height:1.1;

    margin-bottom:10px;

    letter-spacing:-2px;
}

.hero-section h3{

    font-size:28px;

    color:#FFA347;

    font-weight:600;

    margin-bottom:20px;
}

.hero-section p{

    font-size:20px;

    color:#E2E8F0;

    max-width:900px;

    margin:auto;
}

/* Tatkal Notice */

.notice-card{

    padding:18px;

    border-radius:18px;

    background:
    linear-gradient(
        135deg,
        rgba(255,140,66,0.15),
        rgba(255,77,77,0.10)
    );

    border:1px solid rgba(255,140,66,0.25);

    margin-bottom:25px;
}

.notice-text{

    color:#FFD166;

    font-size:15px;

    font-weight:500;
}

.main-title{
    font-size:72px !important;
    font-weight:800 !important;
    text-align:center;
    color:white;
    margin-bottom:10px;
    line-height:1.1;
}

.sub-heading{
    font-size:26px !important;
    text-align:center;
    color:#FF9E45;
    margin-bottom:15px;
}

.hero-desc{
    font-size:18px;
    text-align:center;
    color:#E2E8F0;
}

/* Metric Cards */

.metric-card{

    background:
    rgba(255,255,255,0.04);

    backdrop-filter:blur(20px);

    border:1px solid rgba(255,255,255,0.08);

    border-radius:22px;

    padding:25px;

    text-align:center;

    transition:0.3s;
}

.metric-card:hover{

    transform:translateY(-4px);

    border:1px solid #FF8C42;
}

.metric-title{

    color:#CBD5E1;

    font-size:15px;

    margin-bottom:10px;
}

.metric-value{

    color:#FF9E45;

    font-size:42px;

    font-weight:700;
}

/* Dashboard Section */

.section-title{

    font-size:40px;

    font-weight:700;

    color:white;

    margin-bottom:15px;
}

/* Glass Cards */

.glass-card{

    background:
    rgba(255,255,255,0.05);

    backdrop-filter:blur(18px);

    border:1px solid rgba(255,255,255,0.08);

    border-radius:20px;

    padding:25px;
}

/* Buttons */

.stButton > button{

    background:
    linear-gradient(
        135deg,
        #FF8C42,
        #FF5F1F
    );

    color:white;

    border:none;

    border-radius:12px;

    font-weight:600;

    padding:12px 25px;

    width:100%;
}

.stButton > button:hover{

    background:
    linear-gradient(
        135deg,
        #FFA94D,
        #FF6B35
    );
}

/* Selectbox */

.stSelectbox div[data-baseweb="select"]{

    background:#1E1E1E;
}

/* Footer */

.footer{

    margin-top:50px;

    padding:25px;

    border-top:1px solid rgba(255,255,255,0.08);

    text-align:center;

    color:#CBD5E1;
}

.footer a{

    color:#FF9E45;

    text-decoration:none;
}

/* Scrollbar */

::-webkit-scrollbar{
    width:8px;
}

::-webkit-scrollbar-track{
    background:#1A1A1A;
}

::-webkit-scrollbar-thumb{
    background:#FF8C42;
    border-radius:20px;
}

</style>
""", unsafe_allow_html=True)
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.markdown("""
    <div style="text-align:center;padding:10px;">

    <h1 style="
    color:#FF9E45;
    font-size:32px;
    font-weight:800;
    margin-bottom:0px;
    ">
    🚆 IRCTC AI
    </h1>

    <p style="
    color:#CBD5E1;
    font-size:14px;
    ">
    Automation Command Center
    </p>

    </div>
    """, unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=[
            "Dashboard",
            "Generate Test",
            "Execute Test",
            "Reports",
            "Logs",
            "Screenshots"
        ],
        icons=[
            "house",
            "robot",
            "play-circle",
            "bar-chart",
            "file-text",
            "image"
        ],
        default_index=0
    )

    st.markdown("---")

    st.info(
        """
🚦 Quick Start

• Open IRCTC

• Login with your account

• Generate AI Test

• Execute Test

• View Reports

• Analyze Results
"""
    )

    st.markdown("---")

    st.warning(
        """
⚠️ Tatkal Notice

Automation may be restricted between

10:00 AM - 1:00 PM IST

due to IRCTC Tatkal traffic.
"""
    )

    st.markdown("---")

    st.success(
        """
✅ Sample Scenarios

• Search MAS → YPR

• Verify Login

• Check PNR Status

• Check Chart Vacancy

• Verify Station Suggestions

• Train Availability Search
"""
    )

    st.markdown("---")

    st.markdown("""
    <div style='text-align:center;'>

    <h4 style='color:#FF9E45'>
    👨‍💻 Dhirajkumar M
    </h4>

    AI Powered Test Automation for IRCTC
    <br>
    <a href="https://www.linkedin.com/in/dhirajkumar-/" target="_blank">
    LinkedIn
    </a>
    <br>
  

    <a href="https://github.com/dhirajmanavalan/AI-Powered-Test-Automation-for-IRCTC" target="_blank">
    GitHub Repository
    </a>

    

    Version 1.0.0
    </div>
    """, unsafe_allow_html=True)
# ---------------------------------------------------
# GLOBAL HERO SECTION
# ---------------------------------------------------

st.markdown("""
<div class="hero-section">

<h1 class="main-title">
🚆 AI Powered Test Automation
<br>
for IRCTC
</h1>

<h3 class="sub-heading">
Generate • Execute • Analyze • Report
</h3>

<p class="hero-desc">
AI-driven Playwright Automation Platform powered by
Mistral AI, Pydantic AI and PyTest.
</p>

</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TATKAL NOTICE
# ---------------------------------------------------

st.markdown("""
<div class="notice-card">

<div class="notice-text">

⚠️ IRCTC Tatkal Notice


This automation platform may experience limited
functionality between 10:00 AM and 1:00 PM IST
due to Tatkal booking traffic and IRCTC restrictions.

</div>

</div>
""", unsafe_allow_html=True)


# Dashboard
if selected == "Dashboard":

    generated_tests = len(
        list(Path("tests/generated").glob("test_*.py"))
    )

    reports_count = len(
        list(Path("reports/html").glob("*.html"))
    )

    screenshots_count = len(
        list(Path("reports/screenshots").glob("*.png"))
    ) if Path("reports/screenshots").exists() else 0

    logs_exist = Path(
        "reports/logs/execution.log"
    ).exists()



    st.markdown("## 📊 Dashboard Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">
                Generated Scripts
            </div>
            <div class="metric-value">
                {generated_tests}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">
                Executions
            </div>
            <div class="metric-value">
                {reports_count}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">
                Reports
            </div>
            <div class="metric-value">
                {reports_count}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">
                Screenshots
            </div>
            <div class="metric-value">
                {screenshots_count}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    left, right = st.columns([2, 1])

    with left:

        st.markdown("## 👨‍💻 Project Overview")

        st.markdown("""
        AI Powered Test Automation for IRCTC converts
        plain English user stories into executable
        Playwright + PyTest automation.

        ### Core Capabilities

        - 🤖 AI Test Generation
        - 🎭 Playwright Execution
        - 📸 Screenshot Capture
        - 📄 HTML Reports
        - 📊 Allure Reports
        - 🔍 Failure Analysis
        - ☁️ Railway Deployment Ready
        """)

    with right:

        st.info("""
### 🧠 AI Engine

**Model:** Mistral AI

**Framework:** Pydantic AI

**Test Framework:** Playwright + PyTest
        """)

    st.markdown("---")

    st.markdown("## ⚙️ Architecture Flow")

    st.code("""
User Story
    ↓
Mistral AI
    ↓
Pydantic AI Agent
    ↓
Playwright Test Generation
    ↓
Test File Creation
    ↓
Execution Engine
    ↓
PyTest Execution
    ↓
HTML Reports
    ↓
Screenshots
    ↓
Logs & Analytics
""")

    st.markdown("---")

    st.markdown("## ⚡ Platform Status")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success("AI Generator Online")

    with col2:
        st.success("Execution Engine Online")

    with col3:
        st.success("Reporting Service Online")



# Generate Test
elif selected == "Generate Test":

    st.markdown("""
    <div class="hero-section">
        <h1>🤖 AI Test Generator</h1>
        <p>
        Convert plain English scenarios into production-ready
        Playwright + PyTest automation scripts.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        """
        💡 Example:

        Verify train search from Chennai to Bangalore
        and validate train availability.
        """
    )

    scenario = st.text_area(
        "📝 Enter Test Scenario",
        height=250,
        placeholder="""
Example:

Verify train search from CBE to ED

1. Open IRCTC website
2. Enter source station CBE
3. Enter destination station ED
4. Search trains
5. Verify train results are displayed
        """,
        key="generate_test_scenario"
    )

    col1, col2 = st.columns([1, 5])

    with col1:

        generate_clicked = st.button(
            "🚀 Generate",
            use_container_width=True
        )

    if generate_clicked:

        if not scenario.strip():

            st.warning(
                "Please enter a valid test scenario."
            )

        else:

            try:

                with st.spinner(
                    "Generating Playwright automation..."
                ):

                    llm_client = PydanticAILLMClient()

                    generator = TestGenerator(
                        llm_client
                    )

                    generated_file = (
                        generator.generate_and_save_test(
                            scenario
                        )
                    )

                    generated_code = (
                        generated_file.read_text(
                            encoding="utf-8"
                        )
                    )

                st.success(
                    f"✅ Test generated successfully: {generated_file.name}"
                )

                st.markdown("---")

                st.markdown(
                    "### 📄 Generated Automation Script"
                )

                st.code(
                    generated_code,
                    language="python"
                )

                with open(
                    generated_file,
                    "rb"
                ) as file:

                    st.download_button(
                        label="📥 Download Generated Test",
                        data=file,
                        file_name=generated_file.name,
                        mime="text/plain"
                    )

            except Exception as error:

                st.error(
                    f"Generation failed: {error}"
                )

    st.markdown("---")

    st.markdown("### ⚡ AI Generation Workflow")

    st.markdown("""
    ✅ User enters test scenario

    ✅ Mistral AI analyzes requirements

    ✅ Pydantic AI structures test steps

    ✅ Playwright script generated

    ✅ Test saved under tests/generated

    ✅ Ready for execution
    """)


# Execute Test
elif selected == "Execute Test":

    st.markdown("""
    <div class="hero-section">
        <h1>▶️ Test Execution Center</h1>
        <p>
        Execute AI Generated Playwright Tests and Analyze Results
        </p>
    </div>
    """, unsafe_allow_html=True)

    from execution_engine.cloud_executor import CloudExecutor

    generated_tests_dir = Path(
        "tests/generated"
    )

    test_files = sorted(
        generated_tests_dir.glob(
            "test_*.py"
        )
    )

    if not test_files:

        st.warning(
            "No generated test files found."
        )

    else:

        left, right = st.columns(
            [2, 1]
        )

        with left:

            selected_test = st.selectbox(
                "📄 Select Test Script",
                test_files,
                format_func=lambda x: x.name
            )

        with right:

            st.markdown("<br>", unsafe_allow_html=True)

            run_clicked = st.button(
                "🚀 Run Test",
                use_container_width=True
            )

        st.info(
            f"Selected Test: {selected_test.name}"
        )

        if run_clicked:

            try:

                with st.spinner(
                    "Executing Playwright Automation..."
                ):

                    executor = CloudExecutor(
                        report_dir="reports",
                        headed=not bool(
                            os.getenv("RAILWAY_ENVIRONMENT")
                        )
                    )

                    result = executor.run_tests(
                        [selected_test]
                    )

                st.markdown("---")

                if result["return_code"] == 0:

                    st.success(
                        "✅ Test Execution Passed"
                    )

                else:

                    st.error(
                        "❌ Test Execution Failed"
                    )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Status",
                        "PASS"
                        if result["return_code"] == 0
                        else "FAIL"
                    )

                with col2:
                    st.metric(
                        "Test File",
                        selected_test.name
                    )

                with col3:
                    st.metric(
                        "Report",
                        "Generated"
                    )

                st.markdown("---")

                st.subheader(
                    "🖥 Execution Console"
                )

                st.code(
                    result["stdout"],
                    language="bash"
                )

                if result["stderr"]:

                    st.subheader(
                        "⚠ Error Output"
                    )

                    st.code(
                        result["stderr"],
                        language="bash"
                    )

                st.markdown("---")

                st.subheader(
                    "📊 Generated Report"
                )

                report_path = Path(
                    result["report_path"]
                )

                if report_path.exists():

                    with open(
                        report_path,
                        "rb"
                    ) as report:

                        st.download_button(
                            label="📥 Download HTML Report",
                            data=report,
                            file_name=report_path.name,
                            mime="text/html"
                        )

                screenshots_dir = Path(
                    "reports/screenshots"
                )

                if screenshots_dir.exists():

                    screenshots = sorted(
                        screenshots_dir.glob(
                            "*.png"
                        ),
                        reverse=True
                    )

                    if screenshots:

                        st.markdown("---")

                        st.subheader(
                            "📸 Latest Failure Screenshot"
                        )

                        st.image(
                            str(screenshots[0]),
                            use_container_width=True
                        )

            except Exception as error:

                st.error(
                    f"Execution failed: {error}"
                )

    st.markdown("---")

    st.markdown(
        "### 📜 Recent Execution Summary"
    )

    report_dir = Path(
        "reports/html"
    )

    recent_reports = sorted(
        report_dir.glob("*.html"),
        reverse=True
    )[:5]

    if recent_reports:

        history = []

        for report in recent_reports:

            history.append(
                {
                    "Report": report.name,
                    "Generated": report.stat().st_mtime
                }
            )

        st.dataframe(
            history,
            use_container_width=True
        )

    else:

        st.info(
            "No execution history available."
        )
# Reports
elif selected == "Reports":

    st.markdown("""
    <div class="hero-section">
        <h1>📊 Report Center</h1>
        <p>
        View, Download and Analyze Test Execution Reports
        </p>
    </div>
    """, unsafe_allow_html=True)

    report_dir = Path(
        "reports/html"
    )

    html_reports = sorted(
        report_dir.glob("*.html"),
        reverse=True
    )

    if not html_reports:

        st.warning(
            "No reports found."
        )

    else:

        st.success(
            f"{len(html_reports)} Reports Available"
        )

        selected_report = st.selectbox(
            "📄 Select Report",
            html_reports,
            format_func=lambda x: x.name
        )

        report_size = round(
            selected_report.stat().st_size / 1024,
            2
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Selected Report",
                "1"
            )

        with col2:
            st.metric(
                "Size (KB)",
                report_size
            )

        with col3:
            st.metric(
                "Total Reports",
                len(html_reports)
            )

        st.markdown("---")

        st.info(
            f"📄 {selected_report.name}"
        )

        with open(
            selected_report,
            "rb"
        ) as file:

            st.download_button(
                label="📥 Download Report",
                data=file,
                file_name=selected_report.name,
                mime="text/html"
            )

        st.markdown("---")

        st.subheader(
            "📚 Report History"
        )

        report_history = []

        for report in html_reports:

            report_history.append(
                {
                    "Report Name": report.name,
                    "Size (KB)": round(
                        report.stat().st_size / 1024,
                        2
                    )
                }
            )

        st.dataframe(
            report_history,
            use_container_width=True
        )

        st.markdown("---")

        st.subheader(
            "📈 Reporting Features"
        )

        st.markdown("""
        ✅ HTML Test Reports

        ✅ Execution Summary

        ✅ Pass / Fail Analysis

        ✅ Error Tracebacks

        ✅ Screenshot Attachments

        ✅ Downloadable Artifacts

        ✅ Historical Report Tracking
        """)
# Logs
elif selected == "Logs":

    st.markdown("""
    <div class="hero-section">
        <h1>📄 System Logs</h1>
        <p>
        Monitor Execution Logs, Errors and Runtime Events
        </p>
    </div>
    """, unsafe_allow_html=True)

    log_file = Path(
        "reports/logs/execution.log"
    )

    if not log_file.exists():

        st.warning(
            """
            No execution logs found.

            Run at least one test execution
            to generate logs.
            """
        )

    else:

        log_content = log_file.read_text(
            encoding="utf-8"
        )

        lines = log_content.splitlines()

        total_lines = len(lines)

        error_count = sum(
            1 for line in lines
            if "ERROR" in line.upper()
        )

        warning_count = sum(
            1 for line in lines
            if "WARNING" in line.upper()
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Log Entries",
                total_lines
            )

        with col2:
            st.metric(
                "Warnings",
                warning_count
            )

        with col3:
            st.metric(
                "Errors",
                error_count
            )

        st.markdown("---")

        st.subheader(
            "📜 Log Console"
        )

        st.code(
            log_content,
            language="bash"
        )

        st.markdown("---")

        st.subheader(
            "📋 Latest Entries"
        )

        latest_logs = lines[-20:]

        for line in latest_logs:

            if "ERROR" in line.upper():

                st.error(line)

            elif "WARNING" in line.upper():

                st.warning(line)

            elif "SUCCESS" in line.upper():

                st.success(line)

            else:

                st.info(line)

        st.markdown("---")

        st.subheader(
            "📊 Log Health Status"
        )

        if error_count == 0:

            st.success(
                "System Health: Excellent"
            )

        elif error_count < 5:

            st.warning(
                "System Health: Monitor"
            )

        else:

            st.error(
                "System Health: Critical"
            )

        with open(
            log_file,
            "rb"
        ) as file:

            st.download_button(
                label="📥 Download Log File",
                data=file,
                file_name="execution.log",
                mime="text/plain"
            )
# Screenshots
elif selected == "Screenshots":

    st.markdown("""
    <div class="hero-section">
        <h1>📸 Evidence Gallery</h1>
        <p>
        View Failure Screenshots and Execution Evidence
        </p>
    </div>
    """, unsafe_allow_html=True)

    screenshots_dir = Path(
        "reports/screenshots"
    )

    if not screenshots_dir.exists():

        st.warning(
            """
            Screenshots directory not found.

            Failure screenshots will automatically
            appear here after failed test executions.
            """
        )

    else:

        screenshots = []

        screenshots.extend(
            screenshots_dir.glob("*.png")
        )

        screenshots.extend(
            screenshots_dir.glob("*.jpg")
        )

        screenshots.extend(
            screenshots_dir.glob("*.jpeg")
        )

        screenshots = sorted(
            screenshots,
            reverse=True
        )

        if not screenshots:

            st.success(
                """
                🎉 Great News!

                No failure screenshots available.

                All executed tests have passed successfully.
                """
            )

        else:

            st.success(
                f"{len(screenshots)} Screenshot(s) Available"
            )

            st.markdown("---")

            cols = st.columns(3)

            for index, image in enumerate(screenshots):

                with cols[index % 3]:

                    st.image(
                        str(image),
                        use_container_width=True
                    )

                    st.caption(
                        image.name
                    )

                    with open(
                        image,
                        "rb"
                    ) as file:

                        st.download_button(
                            label=f"📥 Download",
                            data=file,
                            file_name=image.name,
                            mime="image/png",
                            key=f"download_{index}"
                        )

            st.markdown("---")

            st.subheader(
                "📋 Screenshot Details"
            )

            screenshot_data = []

            for image in screenshots:

                screenshot_data.append(
                    {
                        "Screenshot": image.name,
                        "Size (KB)": round(
                            image.stat().st_size / 1024,
                            2
                        )
                    }
                )

            st.dataframe(
                screenshot_data,
                use_container_width=True
            )

            st.markdown("---")

            st.info(
                """
                Screenshot evidence is automatically
                captured whenever a Playwright test fails.

                These screenshots help identify:

                • Locator Issues
                • Assertion Failures
                • UI Changes
                • Network Issues
                • Unexpected Popups
                """
            )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")

st.markdown("""
<div style="
text-align:center;
padding:20px;
border-radius:10px;
background-color:#1E293B;
color:white;
">

<h4>🚀 Developed By</h4>

<h3>DHIRAJKUMAR M</h3>

<p>
Software Developer | AI & Data Science Graduate
</p>

<p>
🔗 GitHub:
<a href="https://github.com/dhirajmanavalan/AI-Powered-Test-Automation-for-IRCTC" target="_blank">
IRCTC Automation using Playwright
</a>
</p>

<p>
💼 LinkedIn:
<a href="https://www.linkedin.com/in/dhirajkumar-/" target="_blank">
Dhirajkumar
</a>
</p>

</div>
""", unsafe_allow_html=True)

st.info(
    "This application uses for demonstration purposes only."
)

st.markdown("---")

st.caption(
    "Playwright IRCTC Automation • Multi-Agent AI Platform • Version 1.0"
)