from flask import Flask
from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient
import os

app = Flask(__name__)

@app.route('/')
def get_secret_value():
    response = """
    <html>
        <head>
            <title>Azure Managed Identity Access Token</title>
            <style>
                body { font-family: Arial, sans-serif; }
                h1 { color: #2c3e50; }
                p { font-size: 14px; line-height: 1.6; }
                .error { color: red; }
                .token { color: green; word-wrap: break-word; }
            </style>
        </head>
        <body>
            <h1>Azure Managed Identity Access Token by Fustok v.5a</h1>
    """

    managed_identity_client_id = os.getenv("UAMI_CLIENT_ID") #"UAMI Guid"
    keyvault_url = "https://<az keyvault>.vault.azure.net/"
    secret_name = "sec01test"

    try:
        credential = ManagedIdentityCredential(client_id=managed_identity_client_id)

        # Obtain an access token for the keyvault
        kvaccesstoken = credential.get_token(keyvault_url)

        # Create a SecretClient using the credential
        secret_client = SecretClient(vault_url=keyvault_url, credential=credential)

        # Retrieve the secret value
        secret = secret_client.get_secret(secret_name)

        #display returned values
        response += f"<p><strong>UAMI_CLIENT_ID:</strong> <span class='token'>{managed_identity_client_id}</span></p>"
        response += f"<p><strong>Access Token:</strong> <span class='token'>{kvaccesstoken.token}</span></p>"
        response += f"<p><strong>Secret '{secret_name}':</strong> <span class='token'>{secret.value}</span></p>"

    except Exception as ex:
        response += f"<p class='error'><strong>An error occurred:</strong> {ex}</p>"

    response += """
        </body>
    </html>
    """
    return response

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8000)
