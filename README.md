# Lost Pet Identifier - Multimodal AI System

A multimodal AI system to assist in the recovery of lost pets by automatically analyzing and matching animal-related content across multiple online sources.

## Project Overview

This system orchestrates multiple AI models to identify visual, textual, and audio features of animals and compare them across lost- and found-pet posts. By ranking potential matches based on similarity rather than exact identification, the system reduces search effort and improves the likelihood of timely recovery.

## Architecture

The system follows a modular pipeline architecture:

1. **Data Ingestion** - Accepts images, text, and audio
2. **Feature Extraction** - CLIP (visual/text), LLaMA (semantic), BirdNET (audio)
3. **Vector Database** - FAISS for efficient similarity search
4. **Similarity Matching** - Cosine similarity ranking
5. **User Interface** - Ranked results with explanations

## Key Technologies

- **CLIP**: Image-text embedding for zero-shot visual similarity
- **LLaMA/LLM**: Semantic feature extraction and normalization
- **FAISS**: Efficient vector similarity search
- **BirdNET**: Audio classification for bird species (demo - see `birdnet_demo.py`)
- **Ollama**: Local LLM hosting for LLaMA

## Installation

1. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set OpenMP environment variable (macOS only):
```bash
export KMP_DUPLICATE_LIB_OK=TRUE
```

4. **(Optional)** Install Ollama for full LLM features (semantic extraction + explanations):
```bash
# Install Ollama from https://ollama.ai
ollama pull llama2  # or llama3, mistral, etc.
```
   **Without Ollama:** The app still runs. Text is normalized with simple keyword matching (species, size, color), and explanations use a basic fallback. CLIP and FAISS work as usual.

5. Set up environment variables (optional):
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

### Web Interface (Recommended for Demo)

```bash
# Start the web interface
./run_interface.sh

# Or manually:
source venv/bin/activate
export KMP_DUPLICATE_LIB_OK=TRUE  # macOS only
streamlit run app.py
```

The interface will open automatically in your browser at `http://localhost:8501`

### Command Line Interface

```bash
# Add a found pet to the database
python main.py add-found --image path/to/image.jpg --description "Small brown dog with floppy ears"

# Search for a lost pet
python main.py search --image path/to/lost_pet.jpg --description "Brown dog, friendly, last seen near Bukit Timah"

# Search with image only
python main.py search --image path/to/lost_pet.jpg
```

### Python API

```python
from lost_pet_identifier import LostPetIdentifier

identifier = LostPetIdentifier()

# Add found pet
identifier.add_found_pet(
    image_path="found_dog.jpg",
    description="Small brown dog with floppy ears",
    metadata={"location": "Bukit Timah", "date": "2024-01-15"}
)

# Search for lost pet
results = identifier.search_lost_pet(
    image_path="lost_dog.jpg",
    description="Brown dog, friendly"
)

for result in results:
    print(f"Similarity: {result['score']:.3f}")
    print(f"Description: {result['description']}")
```

## Project Structure

```
BirdNet/
├── lost_pet_identifier/
│   ├── __init__.py
│   ├── ingestion.py      # Data ingestion module
│   ├── embeddings.py     # CLIP embedding generation
│   ├── llm_extractor.py  # LLaMA semantic extraction
│   ├── vector_db.py      # FAISS vector storage
│   ├── matcher.py        # Similarity matching engine
│   ├── explainer.py      # LLaMA result explanations
│   └── pipeline.py       # Main orchestrator
├── main.py               # CLI interface
├── tests/                # Test scripts
├── data/                 # Sample data and database
└── requirements.txt
```

## Development Status

This is a feature prototype demonstrating the core similarity matching functionality. Future improvements include:
- Domain-specific classifiers (BirdNET integration)
- Location-based filtering
- Expanded dataset support
- Weighted fusion of embeddings
- User-based evaluation metrics

## License

MIT License

