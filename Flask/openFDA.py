import requests
import json
import re

def get_drug_label(drug_name, fdacode):
    url = 'https://api.fda.gov/drug/label.json'
    params = {
        'search': f'openfda.{fdacode}:{drug_name}',
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

def get_drug_info(drug_name, patient_drugs, fdacode):
    label = get_drug_label(drug_name, fdacode)
    if label is None:
        return None
    label = label['results'][0]

    warnings = label['warnings'][0]
    # cleans up the active ingredient stuff 
    active_ingredients = label['openfda']['substance_name']
    print(active_ingredients)

    bad_interactions = []
    # now need to get the stop use
    for active_ingredient in active_ingredients:
        res = get_interactions(active_ingredient)
        if res is None:
            break
        interactions = res['results'][0]
        drug_interactions = interactions['drug_interactions']
        #contraindications = interactions['contraindications']
        for drug in patient_drugs:
            for ing in drug['active_ingredients']:
                print(ing)
                if ing.lower() in drug_interactions[0].lower():
                    print(f"Warning: {drug['drug']} interacts with {drug_name}")
                    bad_interactions.append(drug['drug'])
        #print(f"{active_ingredient} {contraindications}")

    drug_info = {
        "drug": drug_name,
        "warnings": warnings,
        "active_ingredients": active_ingredients,
        "do_not_use" : label['do_not_use'][0],
        "indications_and_usage" : label['indications_and_usage'][0],
        "effective_time" : label['effective_time'][0],
    }
    #print(drug_name)

    return drug_info, bad_interactions

# sample_data = [
#     {
#         "name": "Advil",
#         "active_ingredients": ["ibuprofen"],
#     }, {
#         "name": "Tylenol",
#         "active_ingredients": ["acetaminophen"],
#     }
# ]
#get_drug_info("Advil", sample_data)