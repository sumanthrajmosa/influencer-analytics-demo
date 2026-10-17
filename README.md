# Influencer Campaign Intelligence

An academic Streamlit demo for campaign analytics and LSTM, GRU, and BiLSTM
evaluation. Purchase, revenue, and ROI outcomes include synthetic estimates;
the prototype results are not validated real-world forecasts.

[Open the live demo](https://influencer-analytics-demo-tbbuqs3hutzadswmco2hvj.streamlit.app/)

## Run locally

```powershell
python -m pip install -r requirements.txt
python -m streamlit run streamlit_dashboard.py
```

The team page is available through the **Meet the team** link in the app.

## Free online deployment

This app is deployed on [Streamlit Community Cloud](https://share.streamlit.io/).
The public demo URL is:

https://influencer-analytics-demo-tbbuqs3hutzadswmco2hvj.streamlit.app/

For future updates:

1. Push the app files, `requirements.txt`, `pages/`, `Images/`, the enriched
   campaign CSV, and the two evaluation CSVs to a public GitHub repository.
2. Sign in to Streamlit Community Cloud with the GitHub account that can access
   the repository.
3. Push changes to the `main` branch; Streamlit Community Cloud rebuilds the
   app automatically.

Do not publish the `Document Submissions/`, `models/`, or `.venv/` folders.
The deployment only needs the dashboard artifacts listed in step 1. Member
photos and email addresses on the Team page are public when the app is public.
