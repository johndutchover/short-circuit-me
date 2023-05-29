# short-circuit-me

## project structure
```text
├── scm-poetry/
├── src/
├── requirements.txt
```

### Poetry project: scm-poetry

```text
├── backend
│ └── __init__.py
│ └── pyproject.toml
├── frontend
│ └── __init__.py
│ └── Dockerfile
│ └── pyproject.toml
│ └── streamlit_app.py
├── scm_poetry
│ └── __init__.py
└── tests
    ├── __init__.py
    └── test.py
├── .python-version
├── poetry.lock
├── pyproject.toml
├── README.md
```

#### Package: frontend


#### Package: backend


## Docker

Build frontend image:

 `cd scm-poetry/frontend && docker build -t frontend .`

Run the frontend container:

`docker run -p 8501:8501 frontend`

View your Streamlit app in your browser
<http://0.0.0.0:8501>

Build backend (slack-bolt) image:

 `cd scm-poetry/backend && docker build -t bolt .`

Run the backend container:
- tbd

## Usage

### Start Streamlit dashboard
`poetry run streamlit run frontend/streamlit_app.py`

### IDEs

To run this file:

#### terminal
- from external terminal, use `poetry shell` followed by:
  `streamlit run streamlit_app.py`

#### PyCharm
- from PyCharm...set Python interpreter to .venv/bin/python

#### VSCode
- from VSCode, use "Run Python File" instead of "Run Code" (properly activates venv)
