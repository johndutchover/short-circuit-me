# short-circuit-me

## Notification insights for Slack

### Poetry project tree

```text
├── backend
│ └── .dockerignore
│ └── __init__.py
│ └── backend.Readme.md
│ └── Dockerfile
│ └── fly.toml
│ └── poetry.lock
│ └── pyproject.toml
│ └── slackbolt_api.py
│ └── start_bolt.sh
│ └── pages
    ├── 1_app.py
    ├── __init__.py
│ └── .dockerignore
│ └── __init__.py
│ └── Dockerfile
│ └── fly.toml
│ └── frontend.Readme.md
│ └── login.py
│ └── poetry.lock
│ └── pyproject.toml
│ └── start_streamlit.sh
│ └── .dockerignore
│ └── __init__.py
│ └── Dockerfile
│ └── fly.toml
│ └── login.py
│ └── pyproject.toml
│ └── login.py
│ └── start.sh
├── short_circuit_me
│ └── __init__.py
└── tests
    ├── __init__.py
├── .dockerignore
├── .gitignore
├── .python-version
├── Makefile
├── poetry.lock
├── pyproject.toml
├── README.md
├── short-circuit-me.code-workspace
```

IDE notes:

- from VSCode, use "Run Python File" instead of "Run Code" (properly activates venv)
- from PyCharm...set Python interpreter to .venv/bin/python
- from external terminal, use `poetry shell` followed by:
    `streamlit run streamlit_csv.py`
