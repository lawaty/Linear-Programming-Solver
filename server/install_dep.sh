python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install flask flask-restful flask-cors numpy scipy
pip freeze > requirements.txt