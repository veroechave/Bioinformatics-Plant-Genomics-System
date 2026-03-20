# PROJECT: INTERACTIVE DATABASE MANAGEMENT WITH PYTHON
# AUTHOR: Verónica Mar Echave-Sustaeta Hernán

#!/usr/bin/env python3

import os          # To check if the file exists in the operating system
import json        # To save and read structured data (lists, dictionaries) in text files
import re          # For name cleaning using regular expressions
import difflib     # To compare text and find similarities (correction of user typos)

# Define a constant with the Name of the file where the database will be saved
FILE = "botany_db.txt"

# Official list of provinces to validate user input
SPAIN_PROVINCES = [ 
    "Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila", "Badajoz", "Barcelona", "Burgos", "Cáceres",
    "Cádiz", "Cantabria", "Castellón", "Ciudad Real", "Córdoba", "Cuenca", "Gerona", "Granada", "Guadalajara",
    "Guipúzcoa", "Huelva", "Huesca", "Islas Baleares", "Jaén", "La Coruña", "La Rioja", "Las Palmas", "León",
    "Lérida", "Lugo", "Madrid", "Málaga", "Murcia", "Navarra", "Orense", "Palencia", "Pontevedra", "Salamanca",
    "Santa Cruz de Tenerife", "Segovia", "Sevilla", "Soria", "Tarragona", "Teruel", "Toledo", "Valencia",
    "Valladolid", "Vizcaya", "Zamora", "Zaragoza", "Ceuta", "Melilla" 
]

# FUNCTIONS TO LOAD AND SAVE THE DATABASE

def load_db(file_name):
    # Loads the database from the file, if it exists, when starting the program
    if os.path.exists(file_name):
        try:
            # If it exists, we open the file in read mode ('r') using UTF-8 for accents and ñ
            with open(file_name, "r", encoding="utf-8") as f:
                return json.load(f) # Load JSON content into a python dictionary and return it
        except (json.JSONDecodeError, IOError):
            # If the file exists but is corrupt or empty, we catch the error so the program doesn't crash
            print("Reading error\n"
                  "To continue discovering botanical curiosities\n"
                  "We are going to start with an empty DB")
            return {} # Return an empty dictionary to start from scratch
    else:
        # If the file does not exist (first time running the program)
        print("Our database is currently empty\n"
              "Let's start from the beginning!")
        return {} # Return an empty dictionary

def save_db(file_name, db): # Saves the database to the text file
    try:
        # We open the file in write mode ('w'). If it doesn't exist, Python creates it
        with open(file_name, "w", encoding="utf-8") as f:
            # Dump the 'db' dictionary to file 'f'
            # indent=4 makes it saved pretty and readable
            # ensure_ascii=False allows saving accents correctly
            json.dump(db, f, indent=4, ensure_ascii=False)
        print(f"DB successfully saved in {file_name}") # Visual confirmation for the user
    except IOError:
        # If it fails (e.g., due to space or permissions), we warn the user
        print("Error saving the file")

# HELPER AND SECURITY FUNCTIONS

def clean_plant_name(): # To save correct names
# Asks for the name, removes numbers/symbols using Regex and confirms with the user
    while True:
        entry = input("Plant name (or press ENTER to return to menu): ").strip()
        if not entry: return None # Exit if ENTER is pressed without text
        
        # We delete everything that is NOT a letter
        # r'[^a-zA-ZáéíóúüÁÉÍÓÚÜñÑ\s]' means: Replace everything that is not a letter with (''), which means (nothing)
        clean_name = re.sub(r'[^a-zA-ZáéíóúüÁÉÍÓÚÜñÑ\s]', '', entry).strip().title()

        # If after cleaning nothing is left (because the user only put numbers or symbols)
        if not clean_name:
            print("The name must contain letters. Numbers or symbols are not valid")
            continue

        # We confirm with the user if it is the name of the plant they want to register
        res = ask_secure_confirmation(f"Perhaps you meant: '{clean_name}'. Is it correct? (y/n): ")

        if res is None: return None # Abort
        if res == 'y':
            return clean_name # Return the clean name
        else:
            # If they say no
            print("Understood. Please try to type the name again being more precise")
            print("   (Avoid numbers or symbols)")

def remove_accents(text): # Normalizes text by removing accents to facilitate searches
    # We define which letters with accents are changed for which without accents
    replace = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u'}
    text = text.lower() # Convert everything to lowercase first
    for with_accent, without_accent in replace.items(): # Iterate through the dictionary of replacements
        text = text.replace(with_accent, without_accent) # Substitute in the text
    return text # Return "clean" text

def ask_secure_confirmation(message):
# Prevents the user from answering weird things and allows exiting to the menu if they regret
    while True: # Infinite loop: we don't exit until we have a valid answer
        # We show the question and clean the input (remove spaces and set to lowercase)
        entry = input(message).strip().lower()
        
        # If it's a valid answer, we return it directly (using 'y' for 's')
        if entry == 'y' or entry == 'n':
            return entry
        
        # If the user has typed something that is neither 'y' nor 'n'
        print("\nInvalid character. Expected 'y' or 'n'")
        
        # We start a sub-loop to decide what to do about the error
        while True:
            print("Do you want to ABANDON this option and return to the Main Menu?")
            # We give the option to exit or retry
            decision = input("   Type 'y' to exit or press ENTER (without typing anything) to try again: ").strip().lower()
            
            if decision == 'y':
                print("Returning to main menu...")
                return None # Exit to menu
            
            elif decision == "": 
                # If ENTER was pressed without typing anything
                print("Okay, try again")
                break # Break the sub-loop and return to the main loop
            
            else:
                # If they typed anything else that is neither 'y' nor 'ENTER'
                print(f"'{decision}' is not a valid option")

def ask_positive_float(prompt):
    # Requests a positive decimal number. Rejects text, symbols, and 0
    while True: # Infinite loop that won't break until we have valid data
        # Ask the user for the number, remove side spaces and change commas for dots
        s_raw = input(prompt).strip().replace(",", ".")
        
        # Use regular expressions to filter the text
        # r'[^0-9.]' means: "Search for everything that is NOT (^) a number (0-9) or dot (.)"
        # Substitute it with '' (empty string), i.e., delete it.
        s_clean = re.sub(r'[^0-9.]', '', s_raw)
        
        # Check if there is more than one decimal point
        if s_clean.count('.') > 1:
            # If this happens, warn about the format error
            print("Incorrect numeric format (too many dots).")
            # Return to the beginning of the while loop to ask for data again
            continue

        # If the user typed only letters "by mistake... sure..."
        if not s_clean:
            # Warn that a number must be typed
            print("You must type a number (e.g., 6.9)")
            # Return to the start of the loop
            continue

        # Compare the original entry (s_raw) with the clean one (s_clean)
        # If they are different, it means the user entered strange characters (letters, symbols...)
        if s_raw != s_clean:
            # Warn that something strange was detected
            print(f"I detected non-numeric characters in '{s_raw}'")
            
            # Use our secure function to ask if they meant the clean number
            res = ask_secure_confirmation(f"      Did you mean '{s_clean}'? (y/n): ")
            
            # If the function returns None, the user chose to Exit
            if res is None: return None 
            
            # If the user says no
            if res == 'n':
                # Ask them to type it again
                print("Okay, type it again correctly (e.g., 6.9)")
                continue # Return to the start of the loop
            
            # If the user says yes, we accept the clean number
            print(f"Saved size: {s_clean}") # Confirmation message

        try:
            # Try to convert the clean string to a decimal number
            value = float(s_clean) 
            
            # Verify it is greater than 0 (a size cannot be 0 or negative)
            if value <= 0: 
                # If 0 or less, launch warning
                print("The size must be greater than 0")
            else:
                # If everything is fine (it's a number, correct structure, and >0), return it
                return value 
                
        except ValueError: 
            # Catch any other strange conversion error
            print("Unknown error interpreting the number, please try to type a valid number (e.g., 6.9)") 

def ask_habitat(): # Asks for habitat and corrects typos automatically
    # Correction dictionary: key (what we search) -> value (what we save nicely)
    options_dict = { "aquatic": "Aquatic", "terrestrial": "Terrestrial" }
    
    # List of clean keys for the comparison tool (difflib)
    clean_keys = list(options_dict.keys())

    while True: # Validation loop
        entry_raw = input("Habitat (Aquatic / Terrestrial): ").strip().lower()
        entry_clean = remove_accents(entry_raw) # Clean what the user typed
        
        # Search if what was typed looks like any valid option (cutoff=0.5 is tolerance)
        matches = difflib.get_close_matches(entry_clean, clean_keys, n=1, cutoff=0.5)
        
        if matches: # If we found something similar...
            found_key = matches[0] # Take the best match
            best_option = options_dict[found_key] # Retrieve the nice name with accents
            
            # If typed perfectly, don't bother, save directly
            if entry_clean == remove_accents(best_option).lower():
                print(f"   └─Registered as: {best_option}")
                return best_option
            
            # If there are doubts, use the secure function to confirm
            res = ask_secure_confirmation(f"Did you mean '{best_option}'? (y/n): ")
            
            if res is None: return None # If decided to abort
            if res == 'y':
                print(f"   └─Interpreted and registered as: {best_option}")
                return best_option
            else:
                print("Oh well, try again") # If said no, loop repeats
                
        else:
            # If it doesn't look like anything known
            print("I didn't understand you. Please type 'Aquatic' or 'Terrestial'")

def ask_spain_provinces(plant_name): 
# Asks for a list of provinces, validates each, and allows accumulating them
    print(f"\nCultivation provinces for '{plant_name.upper()}'") 
    
    # Create the dictionary to correct provinces
    provinces_dict = {}
    for prov in SPAIN_PROVINCES: 
        clean_key = remove_accents(prov).lower() # Simple key (albacete)
        provinces_dict[clean_key] = prov # Nice value (Albacete)
    
    list_clean_keys = list(provinces_dict.keys()) # List for the searcher
    accumulated_list = [] # Where we will save validated provinces

    while True: # Main loop to ask for provinces
        
        # If we already have provinces, ask if they want to continue
        if accumulated_list:
            print(f"    TOTAL ADDED: {', '.join(accumulated_list)}") 
            print("    " + "." * 40) 
            
            # Ask if they want to add more
            continue_asking = ask_secure_confirmation(f"    Do you want to add MORE provinces to '{plant_name}'? (y/n): ") 
            
            if continue_asking is None: return None # User wants to abort
            if continue_asking == 'n': break        # User finished, exit loop

        # Ask for provinces separated by commas
        print("\nATTENTION: Enter provinces separated by commas (,)") 
        provinces_raw = input(" ").strip() 
        
        # If ENTER is empty
        if not provinces_raw:
            if not accumulated_list: # If nothing was saved, warn
                print(f"You haven't assigned any province") 
            break # Exit loop (finish)

        # Separate what was typed by commas and remove extra spaces
        user_list = [p.strip() for p in provinces_raw.split(",") if p.strip()]
        
        print("    " + "." * 40) 
        
        # Process each province the user tried to type
        for user_entry in user_list:
            entry_clean = remove_accents(user_entry).lower() # Clean text
            # Search for reasonable similarity
            matches = difflib.get_close_matches(entry_clean, list_clean_keys, n=1, cutoff=0.5)
            
            if matches:
                found_key = matches[0]
                official_name = provinces_dict[found_key]
                
                # Avoid duplicates: if already there, move to the next
                if official_name in accumulated_list:
                    print(f"'{official_name}' was already in the list") 
                    continue

                # If exact match, in it goes
                if entry_clean == found_key:
                    accumulated_list.append(official_name)
                    print(f"ADDED: {official_name}") 
                else:
                    # If similar, ask
                    print(f"I detected '{user_entry}'...") 
                    confirm = ask_secure_confirmation(f"            Did you mean '{official_name}'? (y/n): ") 
                    
                    if confirm is None: return None # Abort mission
                    if confirm == 'y':
                        accumulated_list.append(official_name) # Save
                        print(f"└─ADDED: {official_name}") 
                    else:
                        print("Discarded.")  
            else:
                # If it doesn't look like any province on the official list
                print(f"I don't recognize '{user_entry}'. Discarded") 
        
        print("    " + "." * 40 + "\n") 

    # Final summary upon exit
    pretty_list = ", ".join(accumulated_list) if accumulated_list else "None"
    print("\n" + "=" * 60) 
    print(f"FINISHED FOR: {plant_name.upper()}") 
    print(f"Registered provinces: {pretty_list}") 
    print("=" * 60 + "\n") 
    
    return accumulated_list # Return the full list to the main function

# MAIN MENU FUNCTIONS

# OPTION 1: Add new plant
def introduce_plant(db):
    while True: # Loop to add several plants in a row
        print("\n" + " 💠"*30)
        print("\n=== 📝 NEW PLANT REGISTRATION 📝 ===")
        print()
        
        # Use the name cleaning function (helper function)
        name = clean_plant_name()
        if name is None: break # If ENTER without typing, back to menu
        
        print()
        # Ask for size (validating > 0)
        size = ask_positive_float(f"Size of '{name}' in cm: ")
        
        print()
        # Ask for habitat (validating Aquatic or Terrestrial)
        habitat = ask_habitat()
        if habitat is None: break # If user aborted, exit
        
        print()
        # Ask for provinces (validating with the official list)
        provinces = ask_spain_provinces(name) 
        if provinces is None: break # If user aborted, exit
        
        # Save everything in the main dictionary
        db[name] = {
            "cm": size,
            "habitat": habitat,
            "provinces": provinces
        }
        print(f"🔹 Plant '{name}' successfully saved")

        # Ask if they want to keep adding plants
        res = ask_secure_confirmation("\nAdd another plant? (y/n): ")
        if res is None or res == 'n': break # If no or abort, back to menu

        print("\n" + " 💠"*30)
    
    return db # Return the updated database
    
# OPTION 2: View simple list
def list_plants(db):
    if not db: # If dictionary is empty
        print("\n🍂 The database is empty")
        return
    print("\n" + " 🌿"*30)
    print("\n=== 🗃️ LABORATORY CATALOG 🗃️ ===")
    print()
    
    # Sort names alphabetically for display
    sorted_names = sorted(db.keys(), key=str.lower)
    for i, name in enumerate(sorted_names, 1):
        print(f"{i}. {name}")
    print("\n" + " 🌿"*30)
        
# OPTION 3: Detailed technical sheet
def show_plant_data(db):
    # Infinite loop to perform several searches in a row without exiting to the main menu
    while True:
        print("\n" + " 📑"*30)
        print("\n=== 🔍 PLANT DATA 🔍 ===")
        print()
        
        # Request the name and remove spaces
        entry = input("Enter the name to search (or ENTER to return to menu): ").strip()
        
        # If user presses ENTER exit the loop
        if not entry: break
        
        # Use Regular Expressions (Regex) to filter the plant name
        clean_name = re.sub(r'[^a-zA-ZáéíóúüÁÉÍÓÚÜñÑ]', '', entry).strip().capitalize() 

        # If after cleaning nothing is left (e.g., user put "1234"), warn and restart
        if not clean_name: 
            print("Invalid search. The name must contain letters") 
            continue # Return to the start of while

        # Use helper function 'ask_secure_confirmation' which handles y/n
        res = ask_secure_confirmation(f"Searching for: '{clean_name}'. Correct? (y/n): ") 
        
        if res is None: break # If user decides to exit
        if res == 'n': 
            print("Understood. Enter a name again") 
            continue # Back to start to ask name again

        # If yes, proceed with search
        searched_name = clean_name 
        final_name = None # Initialize this variable to save the final key if found
        
        # Check if the clean name exists as a key in our dictionary
        if searched_name in db:
            final_name = searched_name # Found directly
        else:
            # If no exact match:
            # Get all keys (plant names) existing in the database
            existing_names = list(db.keys()) 
            
            # difflib compares our term with the list and returns the most similar
            # n=1: we only want the best candidate. cutoff=0.6: must look at least 60% alike
            matches = difflib.get_close_matches(searched_name, existing_names, n=1, cutoff=0.6) 

            if matches: 
                # If difflib found something similar, suggest it to the user
                suggestion = matches[0] 
                print(f"I can't find exact '{searched_name}'.") 
                res = ask_secure_confirmation(f"        Perhaps you meant '{suggestion}'? (y/n): ") 

                if res == 'y': 
                    final_name = suggestion # User accepts suggestion
                else: 
                    print(f"Search cancelled.") # User rejects suggestion
            else:
                # If no exact or fuzzy match
                print(f"'{searched_name}' not found and no close matches.") 

        # If plant found or suggestion accepted
        if final_name: 
            d = db[final_name] # Extract sub-dictionary with plant data
            
            # Print technical sheet with clean format
            print("\n" + "."*30)
            print(f"\nTECHNICAL SHEET: {final_name.upper()}")
            print(f"Size: {d['cm']} cm") 
            print(f"Habitat: {d['habitat']}") 
            
            # For provinces, join list with commas. If list is empty, show "No data".
            print(f"Provinces: {', '.join(d['provincias']) if d['provincias'] else 'No data'}")
            print("\n" + "."*30)
            
        # Ask if they want to perform another search before returning to main menu
        res = ask_secure_confirmation("\nSearch for another? (y/n): ")
        if res is None or res == 'n': break # If no, exit while loop

    print("\n" + " 📑"*30) # Final separator when exiting function
     
# OPTION 4: Filter by size (CORRECTED AND COMMENTED)
def search_by_size(db):
    # Start infinite loop to allow user to repeat search several times without exiting to main menu
    while True:
        print("\n" + " 📏"*30)
        print("\n=== 🔍 SEARCH BY SIZE RANGE 🔍 ===")
        
        # Initialize min size variable as empty to know if we got a valid value later
        min_t = None
        
        # Start sub-loop just to ask and validate min size
        while True:
            # Ask user for number removing spaces
            min_in = input("Min size cm (or ENTER for Main Menu): ").strip()
            
            # If variable is empty (user pressed ENTER without typing), break loop
            if not min_in: 
                break 
            
            # Replace commas for dots
            s_norm = min_in.replace(",", ".")

            # Cleaning with regex as in function (ask_positive_float)
            s_clean = re.sub(r'[^0-9.]', '', s_norm)

            # 4. Validations of the resulting text structure:
            # Count if there is more than one decimal point. If so, format is wrong (e.g., 12.5.5)
            if s_clean.count('.') > 1 or s_clean.count('-') > 1:
                print("nvalid format (too many dots), please type a correct number (e.g., 6.9)")
                continue # Back to start of child loop to ask for data again
            
            # If user only typed letters or signs
            if not s_clean:
                print("You must type a number (e.g., 6.9)")
                continue # Back to ask for data.

            # Compare what the user typed with what is clean
            if s_norm != s_clean:
                # If different, warn user about strange characters
                print(f"I detected strange characters in '{min_in}'")
                
                # Ask if meant the clean number using our secure y/n function
                res = ask_secure_confirmation(f"      Did you mean '{s_clean}'? (y/n): ")
                
                # If function returns None, user wants to abort and exit to menu
                if res is None: return 
                
                # If user says n, the clean number was not what they wanted
                if res == 'n':
                    print("Okay, type it again, try to be more precise (e.g., 6.9)")
                    continue # Back to ask for data from zero
                
                # If says y, code continues down using 's_clean' for conversion

            # Conversion and validation 
            try:
                # Try to convert clean string to decimal number
                val = float(s_clean)
                
                # Check if number is negative or zero (biologically impossible for size)
                if val <= 0:
                    print("Size cannot be negative or 0")
                else:
                    # If number is valid, positive and has correct format
                    min_t = val # Save validated value in external variable
                    break # Break sub-loop of min because we already have data
            
            # If error occurs during conversion
            except ValueError:
                print("Error: Could not interpret number")
        
        # If 'min_t' is still None, it means user pressed ENTER to exit
        if min_t is None: break # Break main loop and back to menu

        # Ask for max size with helper function 'ask_positive_float'
        print() # Aesthetic line jump
        max_t = ask_positive_float("Max size cm: ")
        
        # If helper function returned None (user aborted), exit main loop
        if max_t is None: break 
        
        try:
            # If min is greater than max, swap them
            if max_t < min_t:
                min_t, max_t = max_t, min_t 
            
            # Create empty list to save found results.
            results = []
            
            # Iterate in database
            for name, data in db.items():
                # Check if size of that plant is within range [min_t, max_t].
                if min_t <= data["cm"] <= max_t:
                    # If matches, add formatted text to results list
                    results.append(f"{name} ({data['cm']} cm)")
            
            if results:
                print("\n" + "."*30) 
                # Show found plants joined by commas
                print(f"Plants found: {', '.join(results)}")
                print("\n" + "."*30)
            else:
                # If list is empty, warn
                print("No plants in that range")
                
        # Generic error capture just in case
        except ValueError:
            print("Unknown error")

        # Ask if they want another range search
        res = ask_secure_confirmation("\nNew range search? (y/n): ")
        
        # If returns None or no, break loop
        if res is None or res == 'n': break
    
    print("\n" + " 📏"*30)

# OPTION 5: Filter by habitat
def search_by_habitat(db):
    while True: # Infinite loop
        print("\n" + "🍃"*30)
        print("\n=== 🔍 SEARCH BY HABITAT 🔍 ===")
        print()

        # Define valid options and keys to compare
        options_map = { "aquatic": "Aquatic", "terrestrial": "Terrestrial" } 
        valid_keys = list(options_map.keys()) # List of valid keys
        selected_habitat = None # Variable to save final habitat

        # Validation loop to understand what the user is searching for
        while True: # Internal loop
            entry = input("Habitat to filter (Aquatic/Terrestrial) or ENTER for Main Menu: ").strip() ## 
            if not entry: break # If ENTER, back to main menu

            clean_entry = remove_accents(entry) # Normalize
            
            # Use difflib for similarity search
            matches = difflib.get_close_matches(clean_entry, valid_keys, n=1, cutoff=0.5) 

            if matches: # If something similar found
                match = matches[0] 
                nice_name = options_map[match] # Format name correctly

                # If exact, take as good
                if clean_entry == match:
                    selected_habitat = match
                    break # Break internal loop, habitat obtained
                else:
                    # If similar, ask
                    res = ask_secure_confirmation(f"    Did you mean '{nice_name}'? (y/n): ") 
                    if res == 'y': # If confirms
                        selected_habitat = match # Assign suggested habitat
                        break # Break internal loop
                    else: # If rejects
                        print("Okay, try again.") 
            else:
                # If typed something totally different
                print("I didn't understand you. Try ('Aquatic' or 'Terrestrial')") 

        # If loop exited and no habitat selected (because ENTER pressed)
        # Break loop and back to menu
        if not selected_habitat: break 

        # Perform search
        print(f"\nSearching for plants of type: {options_map[selected_habitat].upper()}...") 
        results = [] # List for names of found plants
        for name, data in db.items():
            # Compare habitat of each plant (normalized) with selected habitat
            if remove_accents(data["habitat"]) == selected_habitat:
                results.append(name) # If matches, add name to results list
        
        if results:
            print("\n" + "."*30)
            # Show found plant names joined by commas
            print(f"\nPlants found: {', '.join(results)}")
            print("\n" + "."*30)
        else:
            # If no plant found with that habitat
            print("No plants registered in that habitat")
        
        # Ask if they want another search
        res = ask_secure_confirmation("\nSearch other habitat? (y/n): ")
        if res is None or res == 'n': break

    print("\n" + "🍃"*30)
    
# OPTION 6: Filter by province
def search_by_province(db):
    while True:
        print("\n" + " 📌" *25)
        print("\n=== 🔍 SEARCH BY PROVINCE 🔍 ===")
        print()
        
        searched_prov = input("Province to search (or ENTER to exit): ").strip()
        if not searched_prov: break
        
        # Try to guess which province the user meant
        matches = difflib.get_close_matches(searched_prov.title(), SPAIN_PROVINCES, n=1, cutoff=0.6) 
        normalized_prov = remove_accents(searched_prov)
        
        # If reasonable suggestion, propose it
        if matches and searched_prov.lower() != matches[0].lower():
            suggestion = matches[0]
            print(f"Searching for plants in '{suggestion}'?")
            
            res = ask_secure_confirmation("   (y/n): ")
            if res is None: break # Abort
            
            if res == 'y':
                normalized_prov = remove_accents(suggestion)
                searched_prov = suggestion 
        
        results = []
        # Deep search: look inside the province list of each plant
        for name, data in db.items():
            for plant_province in data.get("provincias", []):
                # If searched province found in this plant's list
                if remove_accents(plant_province) == normalized_prov:
                    results.append(name)
                    break # stop searching this plant and move to next
        
        print()
        if results:
            print("\n" + "."*30)
            print(f"\nPlants cultivable in {searched_prov.title()}: {', '.join(results)}")
            print("\n" + "."*30)
        else:
            print(f"No plants registered for '{searched_prov}'.")
            
        res = ask_secure_confirmation("\nSearch other province? (y/n): ")
        if res is None or res == 'n': break
        
    print("\n" + " 📌" *25) 

# ===========================
# 🚀 PROGRAM EXECUTION
# ===========================

def main():
    """Main function controlling program flow."""
    # Load data from file at start (if it exists)
    db = load_db(FILE)

    while True: # Infinite loop for main menu
        # Show available options
        print("""
=== 🌸🏵️🌼 BOTANY DATABASE MAIN MENU 🌸🏵️🌼 ===

🌱 1 Introduce new plant
🌱 2 List all plants
🌱 3 Show plant data
🌱 4 Search plants by size range
🌱 5 Search plants by habitat
🌱 6 Search plants by province
🌱 0 Save and exit

        """)

        option = input("Select an option: ").strip()  # Request option from user

        # Depending on option, call the corresponding function
        if option == "1": introduce_plant(db)
        elif option == "2": list_plants(db)
        elif option == "3": show_plant_data(db)
        elif option == "4": search_by_size(db)
        elif option == "5": search_by_habitat(db)
        elif option == "6": search_by_province(db)
        elif option == "0":
            # Save everything before closing to not lose data
            save_db(FILE, db) 
            print("👋 Exiting program... See you next time!")
            break # Break infinite loop and program ends
        else:
            print("Invalid option ❌ REMINDER: Enter a number from 0 to 6")
            
# Standard Python entry point.
# If running this file directly, main() is called.
if __name__ == "__main__":
    main()
