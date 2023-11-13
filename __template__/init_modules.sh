#!/bin/bash
python -m venv venv
source venv/bin/activate
pip install google-auth \
  google-auth-oauthlib \
  google-auth-httplib2 \
  google-api-python-client \
  google-cloud-bigquery \
  google-cloud-storage \
  gspread \
  oauth2client \
  python-dotenv \
  pandas \
  db-dtypes \
  openpyxl

pip freeze > requirements.txt

echo 'plesase run "source venv/bin/activate" to activate virtual environment'