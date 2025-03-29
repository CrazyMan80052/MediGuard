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

    warnings = ""
    if 'warnings' in label:
        warnings = label['warnings'][0]
    elif 'warnings_and_cautions' in label:
        warnings = label['warnings_and_cautions'][0]
    elif 'boxed_warning' in label:
        warnings = label['boxed_warning'][0]
        
    active_ingredients = []
    if 'openfda' in label:
        active_ingredients = label['openfda']['substance_name']
        print(active_ingredients)

    bad_interactions = []
    # now need to get the stop use
    for active_ingredient in active_ingredients:
        res = get_interactions(active_ingredient)
        if res is None:
            break
        interactions = res['results'][0]

        drug_interactions = interactions.get('drug_interactions', [])
        for drug in patient_drugs:
            if 'active_ingredients' in drug:
                for ing in drug['active_ingredients']:
                    print(ing)
                    if (len(drug_interactions) > 0 and ing.lower() in drug_interactions[0].lower()) or ing.lower() in warnings.lower():
                        print(f"Warning: {drug['drug']} interacts with {drug_name}")
                        bad_interactions.append(drug['drug'])

    drug_info = {
        "drug": drug_name,
        "warnings": warnings,
        "active_ingredients": active_ingredients,
    }

    if 'do_not_use' in label:
        drug_info["do_not_use"] = label['do_not_use'][0]
    if 'indications_and_usage' in label:
        drug_info["indications_and_usage"] = label['indications_and_usage'][0]
    if 'effective_time' in label:
        drug_info["effective_time"] = label['effective_time'][0]

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
# drug, bad = get_drug_info("Warfarin", sample_data, 'substance_name')
# print('ibuprofen' in drug['warnings'])
# print(bad)