import time
from encounter_generator.encounter_logic import generate_all_encounters
from encounter_generator.generator import generate_divine_blessing

def print_encounter(encounter, number):
    print(f"\n--- Generating Encounter {number} ---")
    time.sleep(0.1)
    
    if encounter.get("type") == "Shop Encounter":
        print(f"Type: Shop Encounter")
        print(f"Rarity Distribution: {encounter['rarity_mix']}\n")
        time.sleep(0.1)
        for category, items in encounter["items_by_category"].items():
            print(f"{category}:")
            for item in items:
                print(f" - {item}")
                time.sleep(0.1)
            print()
    else:
        for key, value in encounter.items():
            print(f"{key.capitalize()}: ", end="")
            time.sleep(0.1)
            
            if isinstance(value, list):
                print()
                for item in value:
                    print(f" - {item}")
                    time.sleep(0.1)
            else:
                print(value)
            time.sleep(0.1)

if __name__ == "__main__":
    divine_blessing_for_run = generate_divine_blessing()
    print("\n=== Divine Blessing For This Run ===")
    print(f" {divine_blessing_for_run}")
    print("=======================================\n")
    encounters = generate_all_encounters(39)
    for i, encounter in enumerate(encounters, start=1):
        print_encounter(encounter, i)
        time.sleep(0.1)