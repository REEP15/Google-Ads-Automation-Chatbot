
# Google Ads Automation Chatbot

This project is an AI-powered chatbot designed to automate Google Ads campaign creation. The chatbot utilizes various libraries and tools to understand a user's business niche through minimal questioning, and automatically fills in the required campaign details for Google Ads. It integrates with Google Ads API and generates ad copies and headlines using OpenAI.

## Libraries and Tools Used

- **Streamlit**: A framework for creating the frontend user interface.
- **LangChain**: For managing conversations and interacting with APIs to fill in the campaign details automatically.
- **Google Ads API**: For programmatically managing Google Ads campaigns.
- **OpenAI**: To generate ad copies and headlines based on user input.
- **os**: For interacting with the operating system and environment variables.
- **dotenv**: For loading environment variables securely.

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/google-ads-chatbot.git
cd google-ads-chatbot
```

### 2. Install dependencies

Create a virtual environment (optional but recommended) and install the necessary libraries:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scriptsctivate
pip install -r requirements.txt
```

### 3. Set up Google Ads API

Follow the [Google Ads API documentation](https://developers.google.com/google-ads/api/docs/start) to create a project in the Google Cloud Console and obtain your `client_id`, `client_secret`, and `developer_token`. Store these credentials in a `.env` file.

### 4. Set up OpenAI API

Create an OpenAI account and obtain your API key. Store it in the `.env` file.

### 5. Set up environment variables

Create a `.env` file in the root directory of the project with the following content:

```
GOOGLE_ADS_CLIENT_ID=your_client_id
GOOGLE_ADS_CLIENT_SECRET=your_client_secret
GOOGLE_ADS_DEVELOPER_TOKEN=your_developer_token
OPENAI_API_KEY=your_openai_api_key
```

### 6. Run the chatbot

Run the chatbot via Streamlit:

```bash
streamlit run app.py
```

### 7. Interact with the chatbot

Once the app is running, visit the displayed URL (typically `http://localhost:8501`) and start interacting with the chatbot. It will guide you through setting up a Google Ads campaign and automatically fill in the details based on your responses.

## Features

- Minimal questioning to understand the business niche and campaign goals.
- Automatically generates the best-fit ad copy and headline using OpenAI's GPT model.
- Seamless integration with Google Ads API for campaign management.
- Easy-to-use UI built with Streamlit.

## License

This project is open-source under the [MIT License](LICENSE).
