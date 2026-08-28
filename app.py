# Import Streamlit to build the browser-based interface.
import streamlit as st

# Configure the browser tab and application layout.
# This must be the first Streamlit command in the file.
st.set_page_config(
    page_title="VisaPath Australia",
    page_icon="🇦🇺",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Apply the full visual design.
# st.html() prevents HTML from appearing as a code block.
st.html("""
    <style>
    /* ---------- Global appearance ---------- */

    :root {
        color-scheme: light;
    }

    html,
    body,
    .stApp,
    button,
    input,
    textarea {
        font-family: Arial, Helvetica, sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 85% 8%,
                rgba(214, 170, 73, 0.14),
                transparent 26%
            ),
            linear-gradient(
                180deg,
                #f9fbfd 0%,
                #edf3f7 100%
            );
        color: #102a43;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2.2rem;
        padding-bottom: 7rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    /* ---------- Sidebar ---------- */

    [data-testid="stSidebar"] {
        background:
            radial-gradient(
                circle at 20% 0%,
                rgba(232, 193, 102, 0.15),
                transparent 25%
            ),
            linear-gradient(
                165deg,
                #071c30 0%,
                #0b3151 62%,
                #124b71 100%
            );
        border-right: none;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.15);
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 5px 0 30px;
    }

    .sidebar-logo {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 45px;
        height: 45px;
        border-radius: 14px;
        background: linear-gradient(135deg, #f7da8d, #c9952d);
        color: #071c30;
        font-size: 21px;
        font-weight: 800;
        box-shadow: 0 9px 24px rgba(201, 149, 45, 0.30);
    }

    .sidebar-brand-name {
        color: #ffffff;
        font-size: 20px;
        font-weight: 700;
    }

    .sidebar-brand-caption {
        margin-top: 2px;
        color: #b9cedd;
        font-size: 11px;
    }

    .sidebar-feature {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 13px 0;
        color: #e2edf4;
        font-size: 13px;
    }

    .sidebar-feature-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 25px;
        height: 25px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.10);
        color: #f7da8d;
        font-size: 10px;
        font-weight: 700;
    }

    /* ---------- Main hero ---------- */

    .hero {
        position: relative;
        overflow: hidden;
        padding: 56px;
        margin-bottom: 27px;
        border-radius: 28px;
        background:
            radial-gradient(
                circle at 90% 15%,
                rgba(247, 218, 141, 0.26),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #071c30 0%,
                #0b3355 58%,
                #15567f 100%
            );
        box-shadow: 0 25px 65px rgba(7, 28, 48, 0.21);
    }

    .hero::after {
        content: "";
        position: absolute;
        right: -90px;
        bottom: -160px;
        width: 300px;
        height: 300px;
        border: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 50%;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        padding: 7px 13px;
        margin-bottom: 22px;
        border: 1px solid rgba(247, 218, 141, 0.40);
        border-radius: 999px;
        background: rgba(247, 218, 141, 0.11);
        color: #f7da8d !important;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.8px;
        text-transform: uppercase;
    }

    .hero-title {
        max-width: 780px;
        margin: 0 0 18px;
        color: #ffffff !important;
        font-size: clamp(38px, 5vw, 60px);
        font-weight: 700;
        line-height: 1.03;
        letter-spacing: -2.4px;
    }

    .hero-title span {
        color: #f7da8d !important;
    }

    /* Force the hero description to remain bright white. */
    .hero .hero-description {
        max-width: 680px;
        margin: 0;
        color: #ffffff !important;
        font-size: 17px;
        font-weight: 400;
        line-height: 1.65;
        opacity: 0.94;
    }

    .hero-status-row {
        display: flex;
        flex-wrap: wrap;
        gap: 22px;
        margin-top: 31px;
    }

    .hero .hero-status {
        display: flex;
        align-items: center;
        gap: 9px;
        color: #ffffff !important;
        font-size: 12px;
        font-weight: 500;
        opacity: 0.92;
    }

    .hero-status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #5bd3a0;
        box-shadow: 0 0 0 5px rgba(91, 211, 160, 0.14);
    }

    /* ---------- Feature cards ---------- */

    .feature-card {
        min-height: 155px;
        padding: 24px;
        border: 1px solid rgba(17, 54, 82, 0.08);
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.92);
        box-shadow: 0 12px 34px rgba(17, 54, 82, 0.07);
        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 18px 42px rgba(17, 54, 82, 0.12);
    }

    .feature-number {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        margin-bottom: 16px;
        border-radius: 12px;
        background: linear-gradient(135deg, #edf4fa, #dceaf4);
        color: #0d4770;
        font-size: 12px;
        font-weight: 800;
    }

    .feature-title {
        margin-bottom: 7px;
        color: #123653;
        font-size: 16px;
        font-weight: 700;
    }

    .feature-description {
        color: #617789;
        font-size: 13px;
        line-height: 1.6;
    }

    /* ---------- Section headings ---------- */

    .section-title {
        margin: 40px 0 7px;
        color: #123653;
        font-size: 26px;
        font-weight: 700;
        letter-spacing: -0.7px;
    }

    .section-description {
        margin-bottom: 18px;
        color: #677d8f;
        font-size: 14px;
    }

    /* ---------- Buttons ---------- */

    .stButton > button {
        min-height: 49px;
        border: 1px solid #d4e0e8;
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.94);
        color: #173e5e;
        font-weight: 600;
        box-shadow: 0 6px 18px rgba(18, 54, 83, 0.06);
        transition: all 0.2s ease;
    }

    .stButton > button p {
        color: #173e5e !important;
    }

    .stButton > button:hover {
        border-color: #c9952d;
        background: #ffffff;
        color: #8b6113;
        transform: translateY(-2px);
        box-shadow: 0 11px 28px rgba(18, 54, 83, 0.11);
    }

    [data-testid="stSidebar"] .stButton > button {
        border-color: rgba(255, 255, 255, 0.23);
        background: rgba(255, 255, 255, 0.08);
        color: #ffffff;
        box-shadow: none;
    }

    [data-testid="stSidebar"] .stButton > button p {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        border-color: #f7da8d;
        background: rgba(247, 218, 141, 0.13);
    }

    /* ---------- Conversation messages ---------- */

    [data-testid="stChatMessage"] {
        padding: 18px 20px;
        margin-bottom: 12px;
        border: 1px solid rgba(18, 54, 83, 0.08);
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.94);
        box-shadow: 0 8px 25px rgba(18, 54, 83, 0.06);
    }

    [data-testid="stChatMessage"] p {
        color: #253f55 !important;
    }

    /* ---------- Redesigned question bar ---------- */

    /* Create a gentle background behind the fixed question area. */
    [data-testid="stBottomBlockContainer"] {
        padding-top: 18px;
        padding-bottom: 18px;
        background:
            linear-gradient(
                180deg,
                rgba(237, 243, 247, 0) 0%,
                rgba(237, 243, 247, 0.96) 32%,
                #edf3f7 100%
            ) !important;
    }

    /* Style the complete question input container. */
    [data-testid="stChatInput"] {
        padding: 6px !important;
        border: 2px solid #d5e1e9 !important;
        border-radius: 20px !important;
        background: #ffffff !important;
        box-shadow: 0 6px 18px rgba(21, 86, 127, 0.07) !important;
        transition:
            border-color 0.2s ease,
            box-shadow 0.2s ease !important;
    }

    /* Add a gold highlight when the input is selected. */
    [data-testid="stChatInput"]:focus-within {
        border-color: #d0a03a !important;
        box-shadow:
        0 0 0 3px rgba(208, 160, 58, 0.13),
        0 6px 18px rgba(21, 86, 127, 0.07) !important;
    }

    /* Remove dark backgrounds from the input's inner elements. */
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] div {
        background-color: transparent !important;
    }

    /* Style the typed question. */
    [data-testid="stChatInput"] textarea {
        min-height: 44px !important;
        padding: 12px 10px !important;
        border: none !important;
        background: transparent !important;
        color: #173e5e !important;
        caret-color: #c9952d !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
    }

    /* Style the placeholder inside the question bar. */
    [data-testid="stChatInput"] textarea::placeholder {
        color: #788b9a !important;
        opacity: 1 !important;
    }

    /* Remove the default focus outline from the textarea. */
    [data-testid="stChatInput"] textarea:focus {
        outline: none !important;
        box-shadow: none !important;
    }

    /* Turn the send control into a navy button. */
    [data-testid="stChatInput"] button {
        width: 42px !important;
        height: 42px !important;
        margin: 2px !important;
        border: none !important;
        border-radius: 13px !important;
        background: linear-gradient(
            135deg,
            #0b3151,
            #15567f
        ) !important;
        color: #ffffff !important;
        box-shadow: 0 7px 17px rgba(11, 49, 81, 0.22) !important;
        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease !important;
    }

    [data-testid="stChatInput"] button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 22px rgba(11, 49, 81, 0.30) !important;
    }

    [data-testid="stChatInput"] button svg {
        color: #ffffff !important;
        fill: #ffffff !important;
    }

    /* ---------- Empty conversation ---------- */

    .empty-conversation {
        padding: 34px;
        margin: 12px 0 20px;
        border: 1px dashed #b8cad8;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.65);
        text-align: center;
    }

    .empty-icon {
        margin-bottom: 10px;
        color: #c9952d;
        font-size: 29px;
    }

    .empty-title {
        color: #173e5e;
        font-size: 16px;
        font-weight: 700;
    }

    .empty-description {
        margin-top: 6px;
        color: #6d8192;
        font-size: 13px;
    }

    /* ---------- Safety disclaimer ---------- */

    .disclaimer {
        display: flex;
        gap: 13px;
        padding: 18px 20px;
        margin-top: 29px;
        border: 1px solid #ebdaa9;
        border-radius: 17px;
        background: #fffaf0;
        color: #675328;
        font-size: 12px;
        line-height: 1.6;
    }

    .disclaimer-icon {
        display: flex;
        flex: 0 0 auto;
        align-items: center;
        justify-content: center;
        width: 27px;
        height: 27px;
        border-radius: 9px;
        background: #f6e7ba;
        color: #986b16;
        font-weight: 800;
    }

    /* ---------- Mobile layout ---------- */

    @media (max-width: 700px) {
        .block-container {
            padding-top: 1rem;
        }

        .hero {
            padding: 37px 28px;
            border-radius: 22px;
        }

        .hero-title {
            letter-spacing: -1.5px;
        }

        .hero-status-row {
            gap: 13px;
        }
    }

    /* Remove every shadow generated inside Streamlit's bottom input area. */
    div[data-testid="stBottom"],
    div[data-testid="stBottom"] *,
    div[data-testid="stBottomBlockContainer"],
    div[data-testid="stBottomBlockContainer"] * {
    border-top-color: transparent !important;
}

    div[data-testid="stBottom"],
    div[data-testid="stBottomBlockContainer"] {
        box-shadow: none !important;
        filter: none !important;
        background: #edf3f7 !important;
}
    </style>
    """)


def generate_answer(question):
    """
    Generate a temporary answer for interface testing.

    The team will later replace this function with the full RAG
    retrieval and answer-generation pipeline.

    Parameters:
        question (str): The question submitted by the user.

    Returns:
        str: A temporary assistant response.
    """

    return (
        "Your question has been received successfully. This interface "
        "currently uses a placeholder response. The RAG pipeline will "
        "later retrieve relevant official information and display a "
        "supported answer with visible source citations."
    )


def submit_question(question):
    """
    Add a question and temporary answer to the conversation.

    Parameters:
        question (str): A typed or preselected question.
    """

    # Ignore blank questions.
    if not question:
        return

    # Save the user's question.
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # Generate a temporary answer.
    answer = generate_answer(question)

    # Save the assistant's answer.
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )


# Create chat history when the application opens.
if "messages" not in st.session_state:
    st.session_state.messages = []


# Build the sidebar.
with st.sidebar:
    # Display the application branding.
    st.html("""
        <div class="sidebar-brand">
            <div class="sidebar-logo">V</div>

            <div>
                <div class="sidebar-brand-name">
                    VisaPath
                </div>

                <div class="sidebar-brand-caption">
                    Australia information assistant
                </div>
            </div>
        </div>
        """)

    st.markdown("### Explore with confidence")

    st.write(
        "Navigate Australian visa information through a clear, "
        "accessible and source-supported experience."
    )

    st.divider()

    st.markdown("#### Prototype features")

    # Display the planned features.
    st.html("""
        <div class="sidebar-feature">
            <span class="sidebar-feature-icon">01</span>
            Official information sources
        </div>

        <div class="sidebar-feature">
            <span class="sidebar-feature-icon">02</span>
            Clear source citations
        </div>

        <div class="sidebar-feature">
            <span class="sidebar-feature-icon">03</span>
            Multilingual support
        </div>

        <div class="sidebar-feature">
            <span class="sidebar-feature-icon">04</span>
            Voice accessibility
        </div>
        """)

    st.divider()

    # Clear the complete conversation.
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("Group 14 · WIL Project")


# Display the main hero area.
st.html("""
    <section class="hero">
        <div class="hero-badge">
            ✦ Australian visa information
        </div>

        <h1 class="hero-title">
            A clearer path through
            <span>visa information.</span>
        </h1>

        <p class="hero-description">
            Ask questions in everyday language and explore information
            supported by official Australian Government resources.
        </p>

        <div class="hero-status-row">
            <div class="hero-status">
                <span class="hero-status-dot"></span>
                Prototype online
            </div>

            <div class="hero-status">
                Official-source focused
            </div>

            <div class="hero-status">
                Privacy conscious
            </div>
        </div>
    </section>
    """)


# Create columns for the feature cards.
feature_one, feature_two, feature_three = st.columns(3)


# First feature card.
with feature_one:
    st.html("""
        <div class="feature-card">
            <div class="feature-number">01</div>

            <div class="feature-title">
                Ask naturally
            </div>

            <div class="feature-description">
                Use everyday language instead of searching through
                multiple complicated government webpages.
            </div>
        </div>
        """)


# Second feature card.
with feature_two:
    st.html("""
        <div class="feature-card">
            <div class="feature-number">02</div>

            <div class="feature-title">
                Check the evidence
            </div>

            <div class="feature-description">
                Future answers will include visible citations to
                the official passages supporting them.
            </div>
        </div>
        """)


# Third feature card.
with feature_three:
    st.html("""
        <div class="feature-card">
            <div class="feature-number">03</div>

            <div class="feature-title">
                Know the limits
            </div>

            <div class="feature-description">
                The assistant will decline to guess when reliable
                supporting information is unavailable.
            </div>
        </div>
        """)


# Introduce the quick-question section.
st.html("""
    <div class="section-title">
        What would you like to explore?
    </div>

    <div class="section-description">
        Choose a starting point or write your own question below.
    </div>
    """)


# Create three quick-question buttons.
quick_one, quick_two, quick_three = st.columns(3)


with quick_one:
    if st.button(
        "Student visa documents",
        use_container_width=True,
    ):
        submit_question(
            "What documents may be required for an Australian student visa?"
        )
        st.rerun()


with quick_two:
    if st.button(
        "Visa conditions",
        use_container_width=True,
    ):
        submit_question(
            "Where can I check the conditions attached to my Australian visa?"
        )
        st.rerun()


with quick_three:
    if st.button(
        "Official assistance",
        use_container_width=True,
    ):
        submit_question("Where can I find official help with an Australian visa?")
        st.rerun()


# Introduce the conversation area.
st.html("""
    <div class="section-title">
        Your conversation
    </div>

    <div class="section-description">
        Ask a question without entering sensitive personal information.
    </div>
    """)


# Show an empty state before the first question.
if not st.session_state.messages:
    st.html("""
        <div class="empty-conversation">
            <div class="empty-icon">✦</div>

            <div class="empty-title">
                Start with a visa-related question
            </div>

            <div class="empty-description">
                Please do not enter passport numbers, health details,
                visa reference numbers or other sensitive information.
            </div>
        </div>
        """)


# Display all saved conversation messages.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Create the main question input.
question = st.chat_input("Ask a question about Australian visa information...")


# Process a submitted question.
if question:
    submit_question(question)
    st.rerun()


# Display the safety disclaimer.
st.html("""
    <div class="disclaimer">
        <div class="disclaimer-icon">!</div>

        <div>
            <strong>General information only.</strong>
            This prototype does not provide immigration or legal advice,
            determine eligibility, recommend a particular visa or guarantee
            an application outcome. Always verify important information with
            the Australian Department of Home Affairs or a registered
            migration professional.
        </div>
    </div>
    """)
