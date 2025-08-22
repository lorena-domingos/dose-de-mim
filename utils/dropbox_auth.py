import dropbox
import os

APP_KEY = os.environ['APP_KEY']
APP_SECRET = os.environ['APP_SECRET']

def get_key():
    auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET, token_access_type='offline')

    authorize_url = auth_flow.start()
    print("1. Vá para:", authorize_url)
    print("2. Clique em 'Permitir' e copie o código de autorização.")

    auth_code = input("Cole o código aqui: ").strip()
    oauth_result = auth_flow.finish(auth_code)

    print("Access token:", oauth_result.access_token)
    print("Refresh token:", oauth_result.refresh_token)


