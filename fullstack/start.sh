#!/bin/sh
python slackbolt_csv.py &
streamlit run pages/1_app.py --server.port=8501 --server.address=0.0.0.0
