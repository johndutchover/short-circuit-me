#!/bin/sh
python slackbolt_csv.py &
streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
