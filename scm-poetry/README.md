
Frontend

#### Docker container
Build frontend image: `docker build -t frontend .`
Run the frontend container: `docker run -p 8501:8501 frontend`
View your Streamlit app in your browser
- URL: http://0.0.0.0:8501

#### Python poetry
`poetry shell`
`streamlit run short_circuit_me.py`
'''To run this file:
        - from VSCode, use "Run Python File" instead of "Run Code" (properly activates venv)
        - from PyCharm...set Python interpreter to .venv/bin/python
        - from external terminal, use "poetry shell" followed by:
            streamlit run short_circuit_me.py
'''