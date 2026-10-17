from pathlib import Path

import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
AFFILIATION = (
    "Amrita School of Computing, Amrita Vishwa Vidyapeetham, Coimbatore"
)
MEMBERS = [
    {
        "name": "Mosa Sumanthraj",
        "roll_number": "CB.SC.U4CSE23227",
        "email": "cb.sc.u4cse23227@cb.amrita.edu",
        "photo": ROOT / "Images" / "227.png",
    },
    {
        "name": "Kasibhotla Yogananda Sarma",
        "roll_number": "CB.SC.U4CSE23221",
        "email": "cb.sc.u4cse23221@cb.students.amrita.edu",
        "photo": ROOT / "Images" / "221.jpg",
    },
    {
        "name": "Kudirella Sai Tejash",
        "roll_number": "CB.SC.U4CSE23331",
        "email": "cb.sc.u4cse23331@cb.students.amrita.edu",
        "photo": ROOT / "Images" / "331.PNG",
    },
]


st.set_page_config(page_title="Team Members", page_icon="👥", layout="wide")
st.title("Meet Team 8")
st.caption("Influencer Campaign Intelligence")
st.markdown("[📊 Back to project dashboard](/)")
st.markdown(f"**Affiliation:** {AFFILIATION}")

st.markdown(
    """
    <style>
    [data-testid="stImage"] img {
        width: 180px;
        height: 180px;
        object-fit: cover;
        border-radius: 50%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

columns = st.columns(len(MEMBERS), gap="large")
for column, member in zip(columns, MEMBERS):
    with column:
        if not member["photo"].is_file():
            st.error(f"Photo not found: {member['photo'].name}")
            continue
        st.image(str(member["photo"]), caption=member["name"], width=180)
        st.subheader(member["name"])
        st.caption(member["roll_number"])
        st.markdown(f"[{member['email']}](mailto:{member['email']})")
        st.caption(AFFILIATION)
