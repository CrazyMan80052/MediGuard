import requests
import json
import re

def get_drug_label(drug_name):
    url = 'https://api.fda.gov/drug/label.json'
    params = {
        'search': f'openfda.brand_name:{drug_name}',
        'limit': 1
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def get_interactions(active_ingredient):
    url = 'https://api.fda.gov/drug/label.json'
    params = {
        'search': f'drug_interactions:{active_ingredient}',
        'limit': 1
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_drug_info(drug_name, patient_drugs):
    label = get_drug_label(drug_name)
    if label is None:
        return None
    label = label['results'][0]
    #print(label.keys())
    #print(label)
    #print(label['stop_use'])
    warnings = label['warnings'][0]
    # cleans up the active ingredient stuff 
    active_ingredients = label['openfda']['substance_name']
    rxcui = label['openfda']['rxcui'][0]
    print(active_ingredients)
    # active_ingredients = re.findall(r"([A-Za-z]+(?: [A-Za-z]+)*) \d+ mg", active_ingredients)
    # for i in range(len(active_ingredients)):
    #     active_ingredients[i] = active_ingredients[i].strip().lower()
    #     if("active ingredients " in active_ingredients[i]):
    #         active_ingredients[i] = active_ingredients[i].replace("active ingredients ", "")
    #     active_ingredients[i] = active_ingredients[i].strip().lower()
    # print(active_ingredients)

    # now need to get the stop use
    for active_ingredient in active_ingredients:
        res = get_interactions(active_ingredient)
        if res is None:
            break
        interactions = res['results'][0]
        drug_interactions = interactions['drug_interactions']
        contraindications = interactions['contraindications']
        for drug in patient_drugs:
            for ing in drug['active_ingredients']:
                if ing.lower() in drug_interactions[0].lower():
                    print(f"Warning: {drug['name']} interacts with {drug_name}")
        print(f"{active_ingredient} {contraindications}")
            # 
    # for drug in patient_drugs:
    #     drug_rxcui = drug['rxcui']
    #     stop_use = get_stop_use()

sample_data = [
    {
        "name": "Advil",
        "active_ingredients": ["ibuprofen"],
        "rxcui": "1234"
    }, {
        "name": "Tylenol",
        "active_ingredients": ["acetaminophen"],
        "rxcui": "5678"
    }
]
get_drug_info("Advil", sample_data)
# api_key = ""
# with open("Flask\API_Key.txt", "r") as file:
#     api_key = file.read().strip()
# print(api_key)
# url = "https://api.fda.gov"

# url = 'https://api.fda.gov/drug/drugsfda.json'
# params = {
#     'search': 'search=openfda.generic_name:"aspirin"',
#     'limit': 1
# }

# response = requests.get(url, params=params)

# if response.status_code == 200:
#     print(response.json())  # Print response as JSON
# else:
#     print(f"Error: {response.status_code}, {response.text}")

# response = requests.get(url, auth=(api_key, ""))