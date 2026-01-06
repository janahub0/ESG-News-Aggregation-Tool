import streamlit as st
import feedparser
import pandas as pd
import re

st.set_page_config(page_title="ESG News Dashboard", layout="wide")
st.title("ESG News Dashboard")
st.write(
    "Browse ESG-related news from Google News. "
    "You can search by keyword, filter by source, choose a time range, and download results."
)

# --------- Controls ---------
sources_list = [
    "Reuters",
    "ESG Today",
    "PR Newswire",
    "ESG News",
    "The Guardian",
    "CNBC",
]

col_top1, col_top2, col_top3 = st.columns([2, 2, 1])

with col_top1:
    query = st.text_input("Keyword/topic (optional):", "")

with col_top2:
    selected_sources = st.multiselect("Filter by sources (optional):", sources_list)

with col_top3:
    time_range_label = st.selectbox(
        "Time range",
        ["Last 24 hours", "Last 3 days", "Last 7 days", "All available"],
        index=1,  # "a 2" → default to 2nd option ("Last 3 days")
    )

reload_clicked = st.button("🔄 Reload latest news")

num_articles = st.slider("Max number of articles to display:", 5, 50, 20)

# --------- Decide effective query ---------
# If nothing is typed and no source is picked, default to "ESG"
if not query and not selected_sources:
    effective_query = "ESG"
else:
    effective_query = query if query else "ESG"

# Map time range → days
if time_range_label == "Last 24 hours":
    max_days = 1
elif time_range_label == "Last 3 days":
    max_days = 3
elif time_range_label == "Last 7 days":
    max_days = 7
else:
    max_days = None  # no filter

# --------- Fetch & process RSS ---------
# This runs every time the page reruns (including when Reload is clicked)
search_term = effective_query
rss_url = f"https://news.google.com/rss/search?q={search_term.replace(' ', '+')}"

feed = feedparser.parse(rss_url)

articles = []
for entry in feed.entries:
    source = entry.source.title if hasattr(entry, "source") else "N/A"
    published = getattr(entry, "published", "")

    # Try getting a summary/snippet if available
    summary = getattr(entry, "summary", "")
    if summary:
        # strip basic HTML tags so it's not clickable/ugly
        summary = re.sub(r"<.*?>", "", summary)

    articles.append(
        {
            "Title": entry.title,
            "URL": entry.link,       # keep raw URL for CSV
            "Link": entry.link,      # will turn into clickable word in display table
            "Published": published,
            "Source": source,
            "Summary": summary,
        }
    )

if not articles:
    st.warning("No articles found from Google News. Try changing the keyword or time range.")
else:
    df = pd.DataFrame(articles)

    # Parse dates and sort newest → oldest
    df["Published_dt"] = pd.to_datetime(df["Published"], errors="coerce", utc=True)
    df = df.sort_values("Published_dt", ascending=False)

    # Filter by time range (if not 'All available')
    if max_days is not None:
        now = pd.Timestamp.utcnow()
        cutoff = now - pd.Timedelta(days=max_days)
        df = df[df["Published_dt"] >= cutoff]

    # Filter by selected sources (optional)
    if selected_sources:
        df = df[df["Source"].isin(selected_sources)]

    # Limit number of rows
    df = df.head(num_articles)

    if df.empty:
        st.warning("No articles match the selected filters (time, sources, keyword). Try relaxing them.")
    else:
        # Format Published nicely
        df["Published (UTC)"] = df["Published_dt"].dt.strftime("%Y-%m-%d %H:%M").fillna("")

        # Build display table:
        # - Title: plain text
        # - Link: clickable word "Link"
        # - Summary: plain text
        display_df = df[["Title", "Source", "Published (UTC)", "Summary", "Link"]].copy()

        # Make the Link column a clickable word
        display_df["Link"] = display_df["Link"].apply(
            lambda url: f'<a href="{url}" target="_blank">Link</a>'
        )

        # Show as HTML table so links work, but keep it compact
        st.markdown("### Results")
        st.write(
            display_df.to_html(escape=False, index=False),
            unsafe_allow_html=True,
        )

        # Prepare CSV with REAL URL (not the HTML)
        csv_df = df[["Title", "Source", "Published", "Summary", "URL"]]
        csv = csv_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download CSV",
            csv,
            "ESG_news.csv",
            "text/csv",
        )
