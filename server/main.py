from flask import Flask, redirect, request, url_for, jsonify, render_template
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import pickle

# Inicializando a aplicação Flask
app = Flask(__name__, template_folder='templates')
 
# Caminho para o arquivo de credenciais
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Diretório raiz do projeto
CREDENTIALS_FILE = os.path.join(BASE_DIR, 'config', 'credentials.json')  # Caminho correto para o arquivo de credenciais
TOKEN_PICKLE = os.path.join(BASE_DIR, 'token.pickle')  # Caminho para salvar o token de acesso

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# Configurando a URL de redirecionamento
REDIRECT_URI = 'http://localhost:8000/oauth2callback'

@app.route('/')
def index():
    return redirect(url_for('html'))

@app.route('/html')
def html():
    return render_template('index.html')

@app.route('/login')
def login():
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=["https://www.googleapis.com/auth/drive.readonly"],
        redirect_uri=REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=["https://www.googleapis.com/auth/drive.readonly"],
        redirect_uri=REDIRECT_URI
    )
    flow.fetch_token(authorization_response=request.url)

    # Salvar as credenciais
    credentials = flow.credentials
    with open(TOKEN_PICKLE, 'wb') as token:
        pickle.dump(credentials, token)

    return redirect(url_for('files_list'))

@app.route('/files')
def files_list():
    # Verificar se o token está salvo
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    # Conectar à API do Google Drive com as credenciais
    drive_service = build('drive', 'v3', credentials=credentials)

    # Listar os arquivos
    results = drive_service.files().list(
        pageSize=10, fields="files(id, name)"
    ).execute()
    
    files = results.get('files', [])
    
    return jsonify(files)  # Retornar a lista de arquivos como JSON


if __name__ == "__main__":
    app.run(debug=True, port=8000)
