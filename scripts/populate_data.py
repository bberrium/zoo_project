import requests
import random

API_URL = "http://localhost:8000"

families = ["Felines", "Canines", "Ursines", "Primates", "Reptiles", "Birds"]
habitats = ["Savannah", "Taiga", "Tropical", "Mountains", "Aquatic", "Desert"]

complex_names = ["North Wing", "South Wing", "Safari Zone", "Aquarium", "Reptile House"]

def generate_data():
    print("--- Starting Data Population ---")

    species_ids = []
    print("Creating Species...")
    for i in range(50):
        data = {
            "name": f"Animal_{i}",
            "life_expectancy": random.randint(5, 40),
            "family": random.choice(families),
            "habitat": random.choice(habitats),
            "extra_info": {
                "diet": "carnivore" if random.random() > 0.5 else "herbivore",
                "activity": "nocturnal" if random.random() > 0.7 else "diurnal",
                "notes": f"Generated species #{i}"
            }
        }
        # POST request with json parameter automatically sets headers
        resp = requests.post(f"{API_URL}/species/", json=data)
        if resp.status_code == 200:
            species_ids.append(resp.json()['id'])
        else:
            print(f"Failed to create species {i}: {resp.text}")
    print(f"-> Created {len(species_ids)} species.")

    # 2. Enclosures
    enclosure_ids = []
    print("Creating Enclosures...")
    for i in range(20):
        data = {
            "complex_name": random.choice(complex_names),
            "room_number": 100 + i,
            "has_water": random.choice([True, False]),
            "area": round(random.uniform(20.0, 200.0), 2)
        }
        resp = requests.post(f"{API_URL}/enclosures/", json=data)
        if resp.status_code == 200:
            enclosure_ids.append(resp.json()['id'])
        else:
            print(f"Failed to create enclosure {i}: {resp.text}")
    print(f"-> Created {len(enclosure_ids)} enclosures.")

    # 3. Create Placements (Linking Species to Enclosures)
    # Strategy: Assign every species to at least one enclosure, 
    # and some species to multiple (to test Many-to-Many).
    print("Creating Placements...")
    placement_count = 0
    
    if species_ids and enclosure_ids:
        for s_id in species_ids:
            # Pick 1 to 3 random enclosures for this animal
            # random.sample picks unique items from a list
            target_enclosures = random.sample(enclosure_ids, k=random.randint(1, 3))
            
            for e_id in target_enclosures:
                data = {
                    "species_id": s_id,
                    "enclosure_id": e_id,
                    "animal_count": random.randint(1, 10)
                }
                
                resp = requests.post(f"{API_URL}/placements/", json=data)
                if resp.status_code == 200:
                    placement_count += 1
                else:
                    print(f"Failed to create placement: {resp.text}")
    
    print(f"-> Created {placement_count} placements.")
    print("--- Data Population Complete ---")

if __name__ == "__main__":
    generate_data()