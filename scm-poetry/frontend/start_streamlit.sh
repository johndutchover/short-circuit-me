#!/bin/sh
# streamlit run pages/1_app.py --server.port=8501 --server.address=0.0.0.0
streamlit run pages/1_app.py --server.port=8501 --server.address=$MY_IP_ADDRESS
