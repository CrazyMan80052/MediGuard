# This controls and manpulates the data for the Flask app

# data structures:
# we will get some kinda json from the API. need to store in a map
# {"Drug Name" or Product/Serial no : {"Drug Name" : name, "Dosage" : dosage ...}}

# Key Names: "Drug Name", "Expiration Date", "Time Interval", "Dosage", "Drug Facts", 
# "Side Affects", "Drug Interactions", "Allergens", "Ingredients", "Warnings"

# patient information: name, date, patient id, doctor id, prescription numbers/list, OTC list
# drug history, times taken each drug(whether they taking or not), allergies
# Each drug in the patients drug list includes: date assigned, doctor note, doctor id, 
# dosage, time interval other drug facts
# Doctor information: name, doctor id, patient id list, 
# doctor enters drug name/id, dosage, time interval, any other important notes
# patient enters OTC drugs with information above(dosage...) 

# getting data from html form rn then maybe read prescription labels and drug facts using OCR
# use a simple table to display data for now for both the client and doctor
# each drug has its own map with key being name or id and values being the drug information
# each doctor has a map with key = doctor id and value is stuff above
# each patient has a map with key = patient id and value is stuff above