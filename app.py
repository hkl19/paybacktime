import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import numpy as np
import matplotlib.pyplot as plt


# Function to display the home page
def show_home():
    st.title("Payback Time 💰")
    st.write("Save up on appliance lifetime costs, while going green!")
    # sector = st.selectbox("Select a Sector:", ["Supermarkets","Retail Store","Offices"])
    # appliances = st.selectbox("Select an Appliance:", ["Refrigerators", "Heaters", "Lighting"])

# Upload inventory file
def upload_inventory():
    st.header('Step 1: Upload an inventory file below')
    uploaded_file = st.file_uploader("Upload an inventory file below: ", type="csv")
    if uploaded_file is not None:
        # Read the uploaded CSV file
        df = pd.read_csv(uploaded_file)
        st.write("Uploaded CSV file:")
        st.dataframe(df)
        print(df.columns)
        return df

# Slider to ask for budget constraint of end user
def ask_budget():
    st.header('Step 2: Add budget constraint')
    maximum = st.number_input("Maximum", 100000,100000000,100000,100000)

    budget = st.slider(f"Budget: ", 0, maximum)
    return budget


# Define tariff data:
def connect_tariff():
    # List of providers
    providers = [
        {"name": "Company 1", "logo": "https://via.placeholder.com/50"},
        {"name": "Company 2", "logo": "https://via.placeholder.com/50"},
        {"name": "Company 3", "logo": "https://via.placeholder.com/50"},
        {"name": "Company 4", "logo": "https://via.placeholder.com/50"},
        {"name": "Company 5", "logo": "https://via.placeholder.com/50"},
        # Add more providers as needed
    ]

    # Display header
    st.header('Step 3: Add tariff constraint')
    container = st.container(height=600)
    
    # Search input and filtering logic
    with container:
        search_term = st.text_input('Search for energy providers:')
        filtered_providers = [provider for provider in providers if search_term.lower() in provider["name"].lower()]

        for provider in filtered_providers:
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 10px;">
                    <div style="display: flex; align-items: center;">
                        <img src="{provider['logo']}" style="width: 50px; height: auto; margin-right: 10px;">
                        <span>{provider['name']}</span>
                    </div>
                    <button style="background-color: #007bff; color: white; border: none; padding: 8px 16px; border-radius: 4px;">
                        Select
                    </button>
                </div>
                """,
                unsafe_allow_html=True,
            )
    

def tariff_statement():
    st.subheader('Tariff Graph')
    chart_data = pd.DataFrame(
    {
        "24hrs": np.arange(0,24,1),
        "Tariff Cost (£)": np.random.uniform(low=0.5, high=1.3, size=24),
    }
    )

    st.line_chart(chart_data, x="24hrs", y="Tariff Cost (£)")

def submit():
    st.button('Submit',key='submit')

# def sidebar_paging():


# Main function
def main():
    if 'Submit' not in st.session_state:
        st.session_state['Submit'] = False
    if 'budget' not in st.session_state:
        st.session_state['budget'] = 0

    show_home()
    df = upload_inventory()
    st.session_state['budget'] = ask_budget()
    connect_tariff()
    tariff_statement()
    submit()
    if st.session_state['Submit'] == True:
        st.rerun()
    st.write(st.session_state['budget'])
    
if __name__ == "__main__":
    main()
