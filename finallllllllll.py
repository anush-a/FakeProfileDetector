import streamlit as st
import requests
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Function to train the model
def train_model():
    # Your existing function to train the model
    fake_users = pd.read_csv(r"C:\Users\shekh\OneDrive\Desktop\final\instafakefinal.csv")
    genuine_users = pd.read_csv(r"C:\Users\shekh\OneDrive\Desktop\final\instarealfinal.csv")
    x = pd.concat([fake_users, genuine_users])
    y = len(fake_users) * [0] + len(genuine_users) * [1]

    feature_columns_to_use = ['Profile Pic', 'Nums/Length Username', 'Full Name Words', 'Bio Length', 'External Url',
                              'Verified', 'Business', '#Posts', '#Followers', '#Following', 'Last Post Recent',
                              '%Post Single Day', 'Index of Activity', 'Average of Likes']

    x = x.loc[:, feature_columns_to_use]

    clf = RandomForestClassifier(n_estimators=40, oob_score=True)
    clf.fit(x, y)

    # Returning trained model
    return clf, feature_columns_to_use

# Function to get user details from Instagram API using UserID
def get_instagram_user_info(user_id):
    url = f"https://instagram-api-20231.p.rapidapi.com/api/get_user_info/{user_id}"

    headers = {
        "X-RapidAPI-Key": 'add8ccd381msh3efd1280b36ee31p108fc9jsn0f6d8f79ff6a',  # Replace with your actual RapidAPI key
        "X-RapidAPI-Host": "instagram-api-20231.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        return user_info
    else:
        st.error(f"Error accessing Instagram API: {response.status_code}")
        return None

# Function to extract relevant features from the API response for testing
def get_features_for_testing_from_user_info(user_info):
    if user_info and 'data' in user_info:
        data = user_info['data']
        features = [
            data.get('has_profile_picture', 0),
            len(data.get('username', '')) / len(data.get('full_name', '')) if len(data.get('full_name', '')) > 0 else 0,
            len(data.get('full_name', '').split()),
            len(data.get('biography', '')),
            int(bool(data.get('external_url'))),
            int(bool(data.get('is_verified'))),
            int(bool(data.get('is_business'))),
            data.get('media_count', 0),
            data.get('follower_count', 0),
            data.get('following_count', 0),
            int(data.get('latest_reel_media', 0) > 0),
            0,  # Adjust this value if more data is available
            0,  # Adjust this value if more data is available
            data.get('average_likes', 0),
        ]

        return features
    else:
        return None

# Streamlit app
def main():
    st.title("Fake/Genuine User Classifier")

    # Train the model when the app starts
    clf, feature_columns_to_use = train_model()

    # User input form for UserID
    st.sidebar.header("User Input")
    user_id = st.sidebar.text_input("Enter Instagram UserID:")

    if user_id:
        # Fetch user info from Instagram API using UserID
        user_info = get_instagram_user_info(user_id)

        if user_info:
            # Display fetched user info from API
            st.subheader("Fetched User Info from Instagram API:")
            st.write(user_info)

            # Test UserID button
            if st.sidebar.button("Test UserID"):
                # Extract relevant features from API response for testing
                features = get_features_for_testing_from_user_info(user_info)

                if features is not None:
                    # Display the extracted features
                    st.subheader("Features Extracted from UserID")
                    for feature_name, value in zip(feature_columns_to_use, features):
                        st.write(f"{feature_name}: {value}")

                    # Make prediction and get probability scores
                    features_df = pd.DataFrame([features], columns=feature_columns_to_use)
                    prediction_proba = clf.predict_proba(features_df)

                    # Display the result with percentage likelihood
                    fake_prob = prediction_proba[0][0] * 100
                    genuine_prob = prediction_proba[0][1] * 100
                    st.write(f"Probability of UserID {user_id} being FAKE: {fake_prob:.2f}%")
                    st.write(f"Probability of UserID {user_id} being GENUINE: {genuine_prob:.2f}%")

                    # Final prediction based on threshold (e.g., 50%)
                    if fake_prob > genuine_prob:
                        st.write(f"Based on the threshold, UserID {user_id}: FAKE user")
                    else:
                        st.write(f"Based on the threshold, UserID {user_id}: GENUINE user")


if __name__ == "__main__":
    main()
