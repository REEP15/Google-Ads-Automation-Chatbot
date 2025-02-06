import streamlit as st
import streamlit.components.v1 as components
from langchain_community.chat_models import ChatOpenAI
from google.ads.googleads.client import GoogleAdsClient 
import openai

# Set up OpenAI API key
openai.api_key = "secret_key"

# Google Ads API setup
def create_google_ads_campaign(client, customer_id, ad_copy):
    """Creates a Google Ads campaign with the given ad copy."""
    # Initialize API services
    campaign_service = client.get_service("CampaignService")
    ad_group_service = client.get_service("AdGroupService")
    ad_service = client.get_service("AdGroupAdService")
    
    # Create campaign
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.create
    # Set campaign details
    campaign.name = "AI Generated Campaign"
    campaign.status = client.enums.CampaignStatusEnum.PAUSED
    campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
    
    campaign_service.mutate_campaigns(customer_id=customer_id, operations=[campaign_operation])
    
    # Create ad group
    ad_group_operation = client.get_type("AdGroupOperation")
    ad_group = ad_group_operation.create
    ad_group.name = "AI Ad Group"
    ad_group.campaign = campaign.resource_name
    ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
    
    ad_group_service.mutate_ad_groups(customer_id=customer_id, operations=[ad_group_operation])
    
    # Create ad
    ad_operation = client.get_type("AdGroupAdOperation")
    ad = ad_operation.create
    ad.ad.expanded_text_ad.headline_part1 = ad_copy["headline"]
    ad.ad.expanded_text_ad.description = ad_copy["description"]
    ad.ad_group = ad_group.resource_name
    ad.status = client.enums.AdGroupAdStatusEnum.PAUSED
    
    ad_service.mutate_ad_group_ads(customer_id=customer_id, operations=[ad_operation])
    
    return "Campaign created successfully!"

# Function to generate ad copy using OpenAI
def generate_ad_copy(business_name, business_type, target_audience, goal):
    """Generates ad copy using OpenAI based on user input."""
    prompt = f"""
    Generate a Google Ads headline and description for a {business_type} business named {business_name}.
    The target audience is {target_audience}, and the marketing goal is {goal}.
    Provide a single best-fit option following Google Ads character limits (30 chars for headline, 90 chars for description).
    """
    
    response = openai.completions.create(  # Updated API method
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert Google Ads copywriter."},
                  {"role": "user", "content": prompt}]
    )
    generated_text = response["choices"][0]["message"]["content"].strip()
    
    # Extract headline and description
    parts = generated_text.split("\n")
    return {"headline": parts[0], "description": parts[1] if len(parts) > 1 else ""}

# Streamlit UI
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Streamlit with External Script</title>
    <!-- External JavaScript file -->
    <script src="https://accounts.google.com/gsi/client" async></script> 
    <script>
        // Function to handle login response
        function handleLogin(response) {
            localStorage.setItem("token", response.credential);  // Logs the response to the console
            alert("Login successful! Check console for response.");
        }
    </script>

    <div id="g_id_onload"
     data-client_id="client_id_from_google_cloud"
     data-context="signin"
     data-ux_mode="popup"
     data-callback="handleLogin"
     data-auto_select="true"
     data-itp_support="true">
    </div>

    <div class="g_id_signin"
     data-type="standard"
     data-shape="rectangular"
     data-theme="outline"
     data-text="signin_with"
     data-size="large"
     data-logo_alignment="left">
    </div>
</head>
<body>
    <!-- You can include other HTML content here as needed -->
</body>
</html>
"""

def main():
    """Main function to handle Streamlit UI and user interactions."""
    
    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Inject external script (this line doesn't change your app's core logic)
    components.html(html_code, height=0)  # height=0 if you don't want to display extra content
    
    st.title("AI-Powered Google Ads Campaign Generator - Chatbot")
    
    # Display chat history
    for message in st.session_state.messages:
        st.write(message["role"] + ": " + message["content"])
    
    # User input
    user_input = st.text_input("Your Response:")
    
    if st.button("Send"):
        if user_input:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Ask next question based on the current state of the conversation
            if len(st.session_state.messages) == 1:
                question = "What is the name of your business?"
            elif len(st.session_state.messages) == 2:
                question = "What type of business is it?"
            elif len(st.session_state.messages) == 3:
                question = "Who is your target audience?"
            elif len(st.session_state.messages) == 4:
                question = "What is your marketing goal?"
            elif len(st.session_state.messages) == 5:
                question = "What is your budget?"
            elif len(st.session_state.messages) == 6:
                question = "What is your Google Ads customer ID?"
                # After gathering all info, generate the ad
                business_name = st.session_state.messages[1]["content"]
                business_type = st.session_state.messages[2]["content"]
                target_audience = st.session_state.messages[3]["content"]
                goal = st.session_state.messages[4]["content"]
                budget = st.session_state.messages[5]["content"]
                customer_id = st.session_state.messages[6]["content"]
                
                ad_copy = generate_ad_copy(business_name, business_type, target_audience, goal)
                st.session_state.messages.append({"role": "system", "content": f"Generated Ad: {ad_copy['headline']} - {ad_copy['description']}"})
                
                # Call Google Ads API here
                client = GoogleAdsClient.load_from_storage("google-ads.yaml")
                result = create_google_ads_campaign(client, customer_id, ad_copy)
                st.session_state.messages.append({"role": "system", "content": result})
                
                st.experimental_rerun()
            else:
                question = "Thank you for your responses! We are generating your campaign."
            
            # Add bot message to chat history (question)
            st.session_state.messages.append({"role": "system", "content": question})
    
if __name__ == "__main__":
    main()
