# Influencer Campaign Intelligence

An academic Streamlit demo for campaign analytics and LSTM, GRU, and BiLSTM
evaluation. Purchase, revenue, and ROI outcomes include synthetic estimates;
the prototype results are not validated real-world forecasts.

## Run locally

```powershell
python -m pip install -r requirements.txt
python -m streamlit run streamlit_dashboard.py
```

The team page is available through the **Meet the team** link in the app.

## Free online deployment

This app is prepared for [Streamlit Community Cloud](https://share.streamlit.io/).
To publish it:

1. Push the app files, `requirements.txt`, `pages/`, `Images/`, the enriched
   campaign CSV, and the two evaluation CSVs to a public GitHub repository.
2. Sign in to Streamlit Community Cloud with the GitHub account that can access
   the repository.
3. Choose **Create app**, select the repository and branch, and set
   `streamlit_dashboard.py` as the main file.
4. After deployment, copy the public app URL into `DEPLOYMENT_URL` in
   `streamlit_dashboard.py` and push the update. The dashboard will then show
   the live link and deployment status.

Do not publish the `Document Submissions/`, `models/`, or `.venv/` folders.
The deployment only needs the dashboard artifacts listed in step 1. Member
photos and email addresses on the Team page are public when the app is public.
