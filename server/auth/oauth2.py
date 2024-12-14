import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow

# Caminho para o arquivo JSON de credenciais
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "config", "credentials.json")
print(CREDENTIALS_FILE)

# Escopos de acesso que seu app precisa
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

def authenticate():
    """
    Autentica o usuário e retorna as credenciais OAuth2.
    """
    if not os.path.exists(CREDENTIALS_FILE):
        raise FileNotFoundError(f"Arquivo de credenciais não encontrado: {CREDENTIALS_FILE}")

    # Configurando o fluxo de autenticação
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    
    # Inicia o processo de autenticação
    creds = flow.run_local_server(port=8080, prompt="consent", authorization_prompt_message="Por favor, autorize o acesso ao Google Drive.")
    return creds
