import hashlib
import os
import streamlit as st
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get the file path
_CLIENT_SECRETS_PATH = os.getenv("CLIENT_SECRETS_PATH")

_SCOPE = "https://www.googleapis.com/auth/adwords"
_SERVER = "127.0.0.1"
_PORT = 5000
_REDIRECT_URI = f"http://{_SERVER}:{_PORT}/oauth2callback"

# Initialize session state
if "authorized" not in st.session_state:
    st.session_state["authorized"] = False

if "passthrough_val" not in st.session_state:
    st.session_state["passthrough_val"] = None

# Function to start authorization flow
def authorize():
    flow = Flow.from_client_secrets_file(_CLIENT_SECRETS_PATH, scopes=_SCOPE)
    flow.redirect_uri = _REDIRECT_URI

    # Create an anti-forgery state token
    passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        state=passthrough_val,
        prompt="consent",
        include_granted_scopes="true",
    )

    return authorization_url, passthrough_val

# Function to handle OAuth2 callback
def oauth2callback(passthrough_val, state, code):
    if passthrough_val != state:
        message = "State token does not match the expected state."
        raise ValueError(message)
    flow = Flow.from_client_secrets_file(_CLIENT_SECRETS_PATH, scopes=_SCOPE)
    flow.redirect_uri = _REDIRECT_URI
    flow.fetch_token(code=code)
    refresh_token = flow.credentials.refresh_token
    return refresh_token

# Streamlit UI code
st.title("OAuth Authentication for Google Ads")

# Handle authorization button click
if not st.session_state["authorized"]:
    if st.button("Authorize Google Ads"):
        authorization_url, passthrough_val = authorize()
        st.session_state["passthrough_val"] = passthrough_val
        # Redirect to Google OAuth URL
        st.experimental_set_query_params(auth_url=authorization_url)

# Handle redirect with auth_url
query_params = st.experimental_get_query_params()
if "auth_url" in query_params:
    st.markdown(f"[Click here to authorize with Google Ads]({query_params['auth_url'][0]})")

# Handle callback and token exchange
if "code" in query_params and "state" in query_params:
    state = query_params["state"][0]
    code = query_params["code"][0]
    passthrough_val = st.session_state.get("passthrough_val")

    if passthrough_val:
        try:
            refresh_token = oauth2callback(passthrough_val, state, code)
            st.session_state["authorized"] = True
            st.success("Authorization successful!")
            st.write(f"Refresh Token: {refresh_token}")
            st.experimental_set_query_params()  # Clear query params after successful auth
        except Exception as e:
            st.error(f"Error during OAuth callback: {str(e)}")
    else:
        st.error("Session expired or unauthorized access. Please restart the authorization process.")
