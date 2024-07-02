import pandas as pd

user_appliances_df = pd.read_csv("uploads/user_upload.csv")
predefined_appliances_df = pd.read_csv("./appliances.csv")

def match_appliances(user_appliances, predefined_appliances):
    matched_appliances = pd.DataFrame(columns=['User Appliance', 'Matched Appliance', 'Match Found'])
    matched_list = []

    for index, user_appliance in user_appliances.iterrows():
        potential_matches = predefined_appliances[predefined_appliances['tag'] == user_appliance['tag']]
        
        if user_appliance['name'] == "Ideal Logic2 C35 35kW Combination Boiler Natural Gas ErP":
            specific_match = potential_matches[potential_matches['name'].str.contains("tepeo", case=False)]
            if not specific_match.empty:
                matched_list.append({
                    'User Appliance': user_appliance['name'],
                    'Matched Appliance': specific_match['name'].iloc[0],
                    'Match Found': True
                })
            else:
                matched_list.append({
                    'User Appliance': user_appliance['name'],
                    'Matched Appliance': None,
                    'Match Found': False
                })
        else:
            if not potential_matches.empty:
                matched_list.append({
                    'User Appliance': user_appliance['name'],
                    'Matched Appliance': potential_matches['name'].iloc[0],  
                    'Match Found': True
                })
            else:
                matched_list.append({
                    'User Appliance': user_appliance['name'],
                    'Matched Appliance': None,
                    'Match Found': False
                })

    matched_appliances = pd.concat([matched_appliances, pd.DataFrame(matched_list)], ignore_index=True)
    return matched_appliances

matched_appliances_df = match_appliances(user_appliances_df, predefined_appliances_df)
print(matched_appliances_df['User Appliance'])
print(matched_appliances_df['Matched Appliance'])