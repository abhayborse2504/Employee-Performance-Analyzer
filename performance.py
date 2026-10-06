import streamlit as st
import pandas as pd
import plotly.express as px
from textblob import TextBlob


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Employee Performance Review Analyzer",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: bold;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    color: #777777;
    margin-bottom: 25px;
}

.metric-card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f5f5f5;
    text-align: center;
}

.warning-box {
    padding: 15px;
    border-radius: 10px;
    background-color: #fff3cd;
    border: 1px solid #ffecb5;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">🤖 Employee Performance Review Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered sentiment analysis to identify potential inconsistencies '
    'and bias signals in employee performance reviews.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SAMPLE DATA
# ============================================================

sample_data = {
    "Employee": [
        "Aarav Sharma",
        "Priya Patel",
        "Rahul Mehta",
        "Sneha Shah",
        "Vikram Joshi",
        "Neha Desai",
        "Rohan Kumar",
        "Ananya Singh",
        "Karan Shah",
        "Meera Patel",
        "Arjun Mehta",
        "Diya Joshi"
    ],

    "Reviewer": [
        "Manager A",
        "Manager B",
        "Manager A",
        "Manager C",
        "Manager B",
        "Manager C",
        "Manager A",
        "Manager B",
        "Manager C",
        "Manager A",
        "Manager B",
        "Manager C"
    ],

    "Feedback": [
        "Excellent performance. Aarav consistently delivers high quality work and helps the team.",
        "Priya completes her tasks but needs to improve communication and teamwork.",
        "Rahul has shown outstanding leadership and has exceeded all expectations.",
        "Sneha often misses deadlines and her work requires significant improvement.",
        "Vikram is highly motivated, creative and consistently produces excellent results.",
        "Neha has struggled with several assignments and needs better attention to detail.",
        "Rohan is reliable and demonstrates strong technical skills.",
        "Ananya's performance has been inconsistent and she needs to improve productivity.",
        "Karan is exceptional, proactive and one of the strongest members of the team.",
        "Meera does not communicate effectively and frequently misses important requirements.",
        "Arjun consistently performs well and provides valuable support to colleagues.",
        "Diya's work quality is poor and several tasks required correction."
    ],

    "Score": [
        5,
        3,
        2,
        2,
        5,
        4,
        4,
        2,
        5,
        1,
        4,
        5
    ]
}

df = pd.DataFrame(sample_data)


# ============================================================
# SENTIMENT ANALYSIS FUNCTION
# ============================================================

def analyze_sentiment(text):

    polarity = TextBlob(str(text)).sentiment.polarity

    if polarity > 0.10:
        sentiment = "Positive"
    elif polarity < -0.10:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return polarity, sentiment


# ============================================================
# APPLY SENTIMENT ANALYSIS
# ============================================================

results = df["Feedback"].apply(analyze_sentiment)

df["Sentiment Score"] = results.apply(lambda x: round(x[0], 3))
df["Sentiment"] = results.apply(lambda x: x[1])


# ============================================================
# POTENTIAL BIAS DETECTION
# ============================================================

def detect_bias(row):

    sentiment = row["Sentiment"]
    score = row["Score"]

    # Strong negative feedback but high performance score
    if sentiment == "Negative" and score >= 4:
        return "Potential Bias"

    # Strong positive feedback but very low performance score
    if sentiment == "Positive" and score <= 2:
        return "Potential Bias"

    return "Normal"


df["Bias Status"] = df.apply(detect_bias, axis=1)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ Dashboard Controls")

st.sidebar.markdown("### Filter Reviews")

selected_sentiment = st.sidebar.multiselect(
    "Sentiment",
    options=["Positive", "Neutral", "Negative"],
    default=["Positive", "Neutral", "Negative"]
)

selected_bias = st.sidebar.multiselect(
    "Review Status",
    options=["Normal", "Potential Bias"],
    default=["Normal", "Potential Bias"]
)


# Apply filters

filtered_df = df[
    (df["Sentiment"].isin(selected_sentiment)) &
    (df["Bias Status"].isin(selected_bias))
]


# ============================================================
# KPI SECTION
# ============================================================

total_reviews = len(filtered_df)

positive_reviews = len(
    filtered_df[filtered_df["Sentiment"] == "Positive"]
)

neutral_reviews = len(
    filtered_df[filtered_df["Sentiment"] == "Neutral"]
)

negative_reviews = len(
    filtered_df[filtered_df["Sentiment"] == "Negative"]
)

bias_reviews = len(
    filtered_df[filtered_df["Bias Status"] == "Potential Bias"]
)

average_score = (
    filtered_df["Score"].mean()
    if len(filtered_df) > 0
    else 0
)


col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "👥 Total Reviews",
        total_reviews
    )

with col2:
    st.metric(
        "😊 Positive",
        positive_reviews
    )

with col3:
    st.metric(
        "😞 Negative",
        negative_reviews
    )

with col4:
    st.metric(
        "🚨 Potential Bias",
        bias_reviews
    )

with col5:
    st.metric(
        "⭐ Avg Score",
        round(average_score, 2)
    )


st.divider()


# ============================================================
# DASHBOARD CHARTS
# ============================================================

col1, col2 = st.columns(2)    


# ---------------- SENTIMENT DISTRIBUTION ----------------

with col1:

    st.subheader("📊 Sentiment Distribution")

    sentiment_counts = (
        filtered_df["Sentiment"]
        .value_counts()
        .reset_index()
    )

    sentiment_counts.columns = ["Sentiment", "Count"]

    fig_sentiment = px.pie(
        sentiment_counts,
        names="Sentiment",
        values="Count",
        title="Employee Review Sentiment"
    )

    st.plotly_chart(
        fig_sentiment,
        use_container_width=True
    )


# ---------------- SCORE DISTRIBUTION ----------------

with col2:

    st.subheader("⭐ Performance Score Distribution")

    score_counts = (
        filtered_df["Score"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    score_counts.columns = ["Score", "Count"]

    fig_score = px.bar(
        score_counts,
        x="Score",
        y="Count",
        title="Performance Scores"
    )

    st.plotly_chart(
        fig_score,
        use_container_width=True
    )


# ============================================================
# SENTIMENT VS PERFORMANCE SCORE
# ============================================================

st.subheader("🔍 Sentiment vs Performance Score")

fig_scatter = px.scatter(
    filtered_df,
    x="Sentiment Score",
    y="Score",
    color="Bias Status",
    hover_data=[
        "Employee",
        "Reviewer",
        "Sentiment",
        "Feedback"
    ],
    size="Score",
    title="AI Sentiment Score vs Performance Score"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)


# ============================================================
# BIAS DETECTION SECTION
# ============================================================

st.subheader("🚨 Potential Bias Detection")

bias_df = filtered_df[
    filtered_df["Bias Status"] == "Potential Bias"
]


if len(bias_df) > 0:

    st.warning(
        f"AI detected {len(bias_df)} review(s) that may require human review."
    )

    st.dataframe(
        bias_df[
            [
                "Employee",
                "Reviewer",
                "Feedback",
                "Score",
                "Sentiment",
                "Sentiment Score",
                "Bias Status"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "No potential bias signals detected in the selected reviews."
    )


# ============================================================
# COMPLETE REVIEW DATA
# ============================================================

st.subheader("📋 Complete Review Analysis")

display_df = filtered_df[
    [
        "Employee",
        "Reviewer",
        "Feedback",
        "Score",
        "Sentiment",
        "Sentiment Score",
        "Bias Status"
    ]
]

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# INDIVIDUAL REVIEW ANALYZER
# ============================================================

st.divider()

st.subheader("🤖 Analyze New Employee Feedback")

feedback_input = st.text_area(
    "Enter peer feedback below:",
    placeholder="Example: The employee consistently delivers excellent work and supports the team."
)

performance_score = st.slider(
    "Performance Score",
    min_value=1,
    max_value=5,
    value=3
)


if st.button("🔎 Analyze Feedback"):

    if feedback_input.strip() == "":

        st.error("Please enter employee feedback.")

    else:

        polarity, sentiment = analyze_sentiment(feedback_input)

        temp_row = {
            "Sentiment": sentiment,
            "Score": performance_score
        }

        temp_df = pd.DataFrame([temp_row])

        bias_status = detect_bias(temp_df.iloc[0])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Sentiment",
                sentiment
            )

        with col2:
            st.metric(
                "Sentiment Score",
                round(polarity, 3)
            )

        with col3:
            st.metric(
                "Performance Score",
                performance_score
            )

        if bias_status == "Potential Bias":

            st.error(
                "🚨 Potential inconsistency detected. "
                "The feedback sentiment and performance score do not appear "
                "to align. Human review is recommended."
            )

        else:

            st.success(
                "✅ No obvious sentiment/score inconsistency detected."
            )


# ============================================================
# PROJECT INFORMATION
# ============================================================

st.divider()

st.subheader("ℹ️ About This AI Dashboard")

st.write("""
This dashboard uses Natural Language Processing (NLP) sentiment analysis
to evaluate employee peer feedback.

The system compares the sentiment expressed in written feedback with the
numerical performance score.

Potential bias signals are highlighted when:

• Negative feedback is combined with a high performance score.

• Positive feedback is combined with a very low performance score.

These signals do not prove that bias exists. They are intended to help
HR teams identify reviews that may deserve additional human evaluation.
""")


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Employee Performance Review Analyzer | AI + NLP + Streamlit"
)