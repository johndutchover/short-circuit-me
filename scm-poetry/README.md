# short-circuit-me

## project structure
```text
├── .streamlit/
│ └── secrets.toml
├── scm-poetry/
├── .gitignore
├── .python-version
├── Makefile
```

### Poetry project: scm-poetry/

```text
├── backend
│ └── .env
│ └── __init__.py
│ └── atlas_motor_conn.py
│ └── Dockerfile
│ └── message_counts.csv (primary)
│ └── poetry.lock
│ └── pyproject.toml
│ └── slackbolt_app.py [MongoDB]
│ └── slackbolt_csv.py [csv]
├── data
│ └── message_counts.csv (copy)
├── frontend
│ └── .env
│ └── __init__.py
│ └── Dockerfile
│ └── entrypoint.sh
│ └── message_counts.csv (copy)
│ └── poetry.lock
│ └── pyproject.toml
│ └── streamlit_app.py [MongoDB]
│ └── streamlit_csv.py [csv]
├── scm_poetry
│ └── __init__.py
└── tests
    ├── __init__.py
├── .python-version
├── .message_counts.csv
├── poetry.lock
├── pyproject.toml
├── README.md
```

### Developer notes

To run this file using poetry:

```text
poetry shell
streamlit run streamlit_csv.py
```

To run this file:

- from VSCode, use "Run Python File" instead of "Run Code" (properly activates venv)
- from PyCharm...set Python interpreter to .venv/bin/python
- from external terminal, use `poetry shell` followed by:
    `streamlit run streamlit_csv.py`
