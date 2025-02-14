import requests
import streamlit as st

# Function to get user ID from the first API
def get_instagram_user_id(username):
    url = f"https://instagram-api-20231.p.rapidapi.com/api/get_user_id/{username}"
    headers = {
        "X-RapidAPI-Key": "92238d0a1cmsh03a01e014a74bbcp1bf74ajsn573e2494e3af",
        "X-RapidAPI-Host": "instagram-api-20231.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    st.write("Response from First API:", response.text)  # Display response

    if response.status_code == 200:
        user_id = response.json().get('data')
        return user_id
    else:
        st.error(f"Error accessing Instagram API to get user ID: {response.status_code}")
        return None

# Function to get user data using the user ID from the second API
def get_instagram_user_data(user_id):
    url = f"https://instagram-api-20231.p.rapidapi.com/api/get_user_info/{user_id}"
    headers = {
        "X-RapidAPI-Key": "92238d0a1cmsh03a01e014a74bbcp1bf74ajsn573e2494e3af",
        "X-RapidAPI-Host": "instagram-api-20231.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    st.write("Response from Second API:", response.text)  # Display response

    if response.status_code == 200:
        user_data = response.json()
        return user_data
    else:
        st.error(f"Error accessing second API to get user data: {response.status_code}")
        return None

# Streamlit app
def main():
    st.title("Instagram User Data Fetcher")

    # User input form
    st.sidebar.header("User Input")
    username = st.sidebar.text_input("Enter Instagram Username:")
    
    if username:
        # Button to fetch user ID from the first API
        if st.sidebar.button("Get User ID"):
            # Get user ID from the first API
            user_id = get_instagram_user_id(username)

            if user_id:
                st.subheader("User ID")
                st.write(user_id)

                # Button to fetch user data from the second API using the obtained user ID
                if st.sidebar.button("Get User Data"):
                    # Get user data using the user ID from the second API
                    user_data = get_instagram_user_data(user_id)

                    if user_data:
                        st.subheader("User Data")
                        st.write(user_data)
            else:
                st.error("Failed to fetch user ID.")

if __name__ == "__main__":
    main()
