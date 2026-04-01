"""
Example usage of the Lost Pet Identifier system.
"""

from lost_pet_identifier import LostPetIdentifier
from pathlib import Path

# Initialize the system
print("Initializing Lost Pet Identifier...")
identifier = LostPetIdentifier(
    vector_db_path="./data/faiss_index",
    ollama_url="http://localhost:11434",
    ollama_model="llama2"
)

# Example 1: Add found pets to the database
print("\n=== Adding Found Pets ===")

# Found pet 1
identifier.add_found_pet(
    image_path=None,  # Replace with actual image path
    audio_path=None,  # Replace with actual audio path (optional, e.g., bird calls)
    description="Small brown dog with floppy ears, friendly, found near Bukit Timah",
    location="Bukit Timah",
    date="2024-01-15"
)

# Found pet 2
identifier.add_found_pet(
    image_path=None,  # Replace with actual image path
    description="Black and white cat, medium size, shy",
    location="Orchard Road",
    date="2024-01-16"
)

print(f"Database now contains {identifier.get_database_size()} pets")

# Example 2: Search for a lost pet
print("\n=== Searching for Lost Pet ===")

results = identifier.search_lost_pet(
    image_path=None,  # Replace with actual image path
    audio_path=None,  # Replace with actual audio path (optional)
    description="Brown dog, friendly, last seen near Bukit Timah",
    k=5,
    include_explanation=True
)

print(f"\nFound {len(results['results'])} matches:")
for i, result in enumerate(results['results'], 1):
    print(f"\n{i}. Similarity: {result['similarity_score']:.3f}")
    print(f"   Description: {result['description']}")
    print(f"   Location: {result.get('location', 'N/A')}")

if results.get('explanation'):
    print(f"\nExplanation:\n{results['explanation']}")

# Example 3: Image-only search
print("\n=== Image-Only Search ===")
results = identifier.search_lost_pet(
    image_path=None,  # Replace with actual image path
    description=None,
    k=3
)

# Example 4: Text-only search
print("\n=== Text-Only Search ===")
results = identifier.search_lost_pet(
    image_path=None,
    description="Small brown dog with floppy ears",
    k=3
)

print("\nDone!")

