
import streamlit as st
import pandas as pd
import re

# Function to calculate transparency score
def calculate_transparency_score(text):
    base_score = 100
    text = text.lower()

    emotional_triggers = [
        "threat", "crisis", "danger", "emergency", "now", "must", "freedom", 
        "destroy", "war", "chaos", "out of control", "take back", "only", "save"
    ]
    emotional_hits = sum(1 for word in emotional_triggers if word in text)
    base_score -= emotional_hits * 3

    vague_buzzwords = ["real americans", "common sense", "woke", "patriot", "truth", "agenda"]
    buzzword_hits = sum(1 for word in vague_buzzwords if word in text)
    base_score -= buzzword_hits * 2

    if re.search(r"\bus\b.*\bthem\b", text) or re.search(r"\bagainst\b.*\bus\b", text):
        base_score -= 10

    if "source" not in text and "report" not in text and "data" not in text:
        base_score -= 10

    return max(0, min(100, base_score))

# Title and description
st.title("Selective Mind Analyzer")
st.subheader("Decode media, speeches, or posts using the 5F Framework")

# User input
user_input = st.text_area("Paste the text you want to analyze here:", height=200)

# When user clicks 'Analyze'
if st.button("Run Analysis"):
    transparency_score = calculate_transparency_score(user_input)

    data = {
        "Framework Component": [
            "Follow the Money",
            "Feel the Emotion",
            "Find the Gaps",
            "Filter the Language",
            "Frame the System"
        ],
        "Analysis": [
            "Identifies who profits or gains from the message.",
            "Detects emotional triggers and their purpose.",
            "Reveals missing perspectives or cherry-picked facts.",
            "Uncovers manipulative phrases and slogans.",
            "Links the message to bigger institutional systems."
        ],
        "Example Insight": [
            "Possible political or corporate interest influencing the message.",
            "Message triggers fear and urgency to push action.",
            "No counterarguments or broader context offered.",
            "Uses binary framing like 'us vs. them' or 'real Americans'.",
            "Reflects systemic patterns tied to privatization or nationalism."
        ]
    }

    df = pd.DataFrame(data)

    st.write("### Transparency Score")
    st.metric(label="Score (0 = least transparent, 100 = most transparent)", value=transparency_score)

    st.write("### Analysis Output")
    st.dataframe(df)
