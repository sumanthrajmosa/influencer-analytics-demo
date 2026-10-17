from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent
CAMPAIGNS_PATH = ROOT / "influencer_campaigns_project_ready_enriched.csv"
METRICS_PATH = ROOT / "evaluation" / "model_comparison.csv"
PREDICTIONS_PATH = ROOT / "evaluation" / "best_model_predictions.csv"
DEPLOYMENT_URL = ""

CAMPAIGN_COLUMNS = [
    "campaign_id",
    "influencer_id",
    "category",
    "platform",
    "followers",
    "views",
    "likes",
    "comments",
    "engagement_rate",
    "purchases",
    "revenue",
    "campaign_cost",
    "roi",
]
METRIC_COLUMNS = [
    "model",
    "mae",
    "rmse",
    "r2",
    "train_samples",
    "test_samples",
    "test_influencers",
]
PREDICTION_COLUMNS = [
    "campaign_id",
    "influencer_id",
    "actual_purchases",
    "predicted_purchases",
]


st.set_page_config(
    page_title="Influencer Analytics Demo",
    page_icon="📊",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    [data-testid="stMetric"] {
        background: #f5f8f7;
        border: 1px solid #e5ece9;
        padding: 1rem;
        border-radius: 0.75rem;
        color: #18302b;
    }
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        color: #18302b;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def require_columns(frame: pd.DataFrame, columns: list[str], label: str) -> bool:
    missing = sorted(set(columns) - set(frame.columns))
    if missing:
        st.error(f"{label} is missing required columns: {', '.join(missing)}")
        return False
    return True


st.title("Influencer Campaign Intelligence")
st.caption(
    "A small end-to-end demo: explore campaign performance, then compare "
    "sequence models on held-out influencers."
)
st.page_link("pages/1_Team_Members.py", label="Meet the team", icon="👥")

if DEPLOYMENT_URL:
    st.success("Deployment status: live on Streamlit Community Cloud.")
    st.link_button("Open online demo", DEPLOYMENT_URL)
else:
    st.warning(
        "Deployment status: local demo ready; the public Streamlit Community "
        "Cloud URL will appear here after publishing."
    )
    st.link_button(
        "Open free deployment portal",
        "https://share.streamlit.io/",
    )

if not CAMPAIGNS_PATH.is_file():
    st.error(f"Campaign dataset not found: {CAMPAIGNS_PATH.name}")
    st.stop()

campaigns = read_csv(CAMPAIGNS_PATH)
if not require_columns(campaigns, CAMPAIGN_COLUMNS, "Campaign dataset"):
    st.stop()

campaigns["followers"] = pd.to_numeric(campaigns["followers"], errors="coerce")
if "campaign_number" in campaigns:
    campaigns["campaign_number"] = pd.to_numeric(
        campaigns["campaign_number"], errors="coerce"
    )
for column in (
    "views",
    "likes",
    "comments",
    "engagement_rate",
    "purchases",
    "revenue",
    "campaign_cost",
    "roi",
):
    campaigns[column] = pd.to_numeric(campaigns[column], errors="coerce")

with st.sidebar:
    st.header("Explore campaigns")
    categories = ["All categories", *sorted(campaigns["category"].dropna().unique())]
    selected_category = st.selectbox("Category", categories)

    category_campaigns = campaigns
    if selected_category != "All categories":
        category_campaigns = campaigns[campaigns["category"] == selected_category]
    creators = [
        "All creators",
        *sorted(category_campaigns["influencer_id"].dropna().unique()),
    ]
    selected_creator = st.selectbox("Creator", creators)

    st.divider()
    st.markdown("**Demo flow**")
    st.markdown(
        "1. Filter the campaign dataset\n"
        "2. Compare creator and campaign performance\n"
        "3. Review LSTM, GRU and BiLSTM results"
    )

filtered = category_campaigns
if selected_creator != "All creators":
    filtered = filtered[filtered["influencer_id"] == selected_creator]

st.info(
    "**Data note:** campaign purchase, revenue and ROI outcomes include "
    "synthetic estimates. Model scores are a prototype evaluation, not "
    "evidence of real-world performance."
)

kpis = st.columns(4)
kpis[0].metric("Campaigns", f"{len(filtered):,}")
kpis[1].metric("Creators", f"{filtered['influencer_id'].nunique():,}")
kpis[2].metric("Total views", f"{filtered['views'].sum():,.0f}")
kpis[3].metric("Avg. engagement", f"{filtered['engagement_rate'].mean():.1f}%")

st.divider()
left, right = st.columns(2, gap="large")

with left:
    st.subheader("Top creators by views")
    creator_views = (
        filtered.groupby("influencer_id", as_index=False)["views"]
        .sum()
        .nlargest(10, "views")
        .sort_values("views")
        .set_index("influencer_id")
    )
    if creator_views.empty:
        st.caption("No campaign records match these filters.")
    else:
        st.bar_chart(creator_views, horizontal=True, color="#168C78")

with right:
    st.subheader("Performance by campaign sequence")
    if "campaign_number" in filtered.columns:
        sequence = (
            filtered.dropna(subset=["campaign_number"])
            .groupby("campaign_number", as_index=False)
            .agg(average_views=("views", "mean"), campaigns=("campaign_id", "count"))
            .sort_values("campaign_number")
            .set_index("campaign_number")
        )
    else:
        sequence = pd.DataFrame()
    if sequence.empty:
        st.caption("No campaign-sequence data is available for these filters.")
    else:
        st.line_chart(sequence[["average_views"]], color="#E47C45")
        st.caption("Average views grouped by each creator's campaign number.")

with st.expander("Campaign records", expanded=False):
    display_columns = [
        "campaign_id",
        "influencer_id",
        "category",
        "platform",
        "followers",
        "views",
        "engagement_rate",
        "purchases",
        "roi",
    ]
    st.dataframe(
        filtered[display_columns].sort_values("views", ascending=False),
        hide_index=True,
        width="stretch",
        column_config={
            "campaign_id": "Campaign",
            "influencer_id": "Creator",
            "engagement_rate": st.column_config.NumberColumn(
                "Engagement", format="%.2f%%"
            ),
            "roi": st.column_config.NumberColumn("ROI", format="%.1f%%"),
        },
    )

st.divider()
st.header("Sequence model evaluation")
st.caption(
    "LSTM, GRU and BiLSTM models predict purchases from chronological campaign "
    "features. Influencers—not individual campaigns—are held out for testing."
)

if not METRICS_PATH.is_file() or not PREDICTIONS_PATH.is_file():
    missing_files = [
        path.name for path in (METRICS_PATH, PREDICTIONS_PATH) if not path.is_file()
    ]
    st.error(f"Model evaluation artifact(s) not found: {', '.join(missing_files)}")
    st.stop()

metrics = read_csv(METRICS_PATH)
predictions = read_csv(PREDICTIONS_PATH)
if not require_columns(
    metrics, METRIC_COLUMNS, "Model comparison"
) or not require_columns(predictions, PREDICTION_COLUMNS, "Best-model predictions"):
    st.stop()
if metrics.empty or predictions.empty:
    st.error("Model evaluation artifacts contain no results.")
    st.stop()

best_model = metrics.loc[metrics["rmse"].idxmin()]
summary = st.columns(3)
summary[0].metric("Best held-out RMSE", f"{best_model['rmse']:.1f} purchases")
summary[1].metric("Best model", str(best_model["model"]))
summary[2].metric(
    "Test windows",
    f"{int(best_model['test_samples'])} across "
    f"{int(best_model['test_influencers'])} unseen creators",
)

model_left, model_right = st.columns([1, 1.2], gap="large")
with model_left:
    st.subheader("Model comparison")
    st.bar_chart(
        metrics.set_index("model")[["rmse"]],
        color="#4E78A0",
    )
    st.dataframe(
        metrics[
            [
                "model",
                "mae",
                "rmse",
                "r2",
                "train_samples",
                "test_samples",
                "test_influencers",
            ]
        ],
        hide_index=True,
        width="stretch",
        column_config={
            "model": "Model",
            "mae": st.column_config.NumberColumn("MAE", format="%.1f"),
            "rmse": st.column_config.NumberColumn("RMSE", format="%.1f"),
            "r2": st.column_config.NumberColumn("R²", format="%.3f"),
            "train_samples": "Train windows",
            "test_samples": "Test windows",
            "test_influencers": "Test creators",
        },
    )

with model_right:
    st.subheader(f"{best_model['model']} held-out predictions")
    st.bar_chart(
        predictions.set_index("campaign_id")[
            ["actual_purchases", "predicted_purchases"]
        ],
        color=["#168C78", "#E47C45"],
    )
    st.caption("Actual and predicted purchase estimates for test campaigns.")

st.caption(
    "Prototype limitations: the dataset is small, and several conversion and "
    "business outcome fields are simulated. Treat the metrics as a learning "
    "demonstration, not a production forecast."
)
