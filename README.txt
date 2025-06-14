Google Ads Automation Chatbot
This project is an AI-powered chatbot designed to automate the creation of Google Ads campaigns. With minimal input from the user, the chatbot understands the business niche, generates ad headlines and descriptions using OpenAI, and integrates with the Google Ads API to create and manage campaigns.

Tech Stack
Streamlit – For building the web-based user interface

LangChain – For handling AI-driven conversations and dynamic form filling

Google Ads API – For programmatic ad campaign management

OpenAI API – For generating ad copy and headlines

python-dotenv – For loading environment variables securely

os – For system-level environment handling

Setup Instructions
1. Clone the Repository

git clone https://github.com/yourusername/google-ads-chatbot.git
cd google-ads-chatbot

2. Install Dependencies
(Optional) Create a virtual environment:

python -m venv venv
Activate it:

On macOS/Linux:

source venv/bin/activate
On Windows:

venv\Scripts\activate
Install the required packages:

pip install -r requirements.txt

3. Configure Google Ads API
Follow the Google Ads API Getting Started Guide to:

Create a project in Google Cloud Console

Enable the Google Ads API

Obtain your client_id, client_secret, and developer_token

4. Configure OpenAI API
Create an account at OpenAI and get your API key.

5. Create a .env File
In the root directory of the project, create a .env file:

GOOGLE_ADS_CLIENT_ID=your_client_id
GOOGLE_ADS_CLIENT_SECRET=your_client_secret
GOOGLE_ADS_DEVELOPER_TOKEN=your_developer_token
OPENAI_API_KEY=your_openai_api_key

6. Run the App
streamlit run app.py

7. Access the Chatbot
Open the URL displayed in the terminal (usually http://localhost:8501) to interact with the chatbot. It will guide you through setting up your Google Ads campaign.

Features
Minimal questioning to identify your business and campaign goals

AI-generated headlines and descriptions using OpenAI's GPT models

Direct integration with the Google Ads API for campaign creation

Web interface built with Streamlit for ease of use

License
This project is licensed under the MIT License.
