# Quick Start Guide

## Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed and running (for LLM features)
   - Download from: https://ollama.ai
   - After installation, pull a model:
     ```bash
     ollama pull llama2
     # or
     ollama pull llama3
     ```

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd BirdNet
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set OpenMP environment variable (macOS only, prevents FAISS conflicts):**
   ```bash
   export KMP_DUPLICATE_LIB_OK=TRUE
   ```
   
   Or add to your `~/.bashrc` or `~/.zshrc`:
   ```bash
   echo 'export KMP_DUPLICATE_LIB_OK=TRUE' >> ~/.zshrc
   ```

   Note: If you have CUDA, you can use `faiss-gpu` instead of `faiss-cpu`:
   ```bash
   pip install faiss-gpu
   ```

## Basic Usage

### 1. Start Ollama (if not already running)

```bash
ollama serve
```

In another terminal, verify it's working:
```bash
ollama list
```

### 2. Add Found Pets to Database

```bash
# With image and description
python main.py add-found \
    --image path/to/found_pet.jpg \
    --description "Small brown dog with floppy ears, friendly" \
    --location "Bukit Timah" \
    --date "2024-01-15"

# With description only
python main.py add-found \
    --description "Black and white cat, medium size, shy" \
    --location "Orchard Road"
```

### 3. Search for Lost Pet

```bash
# With image and description
python main.py search \
    --image path/to/lost_pet.jpg \
    --description "Brown dog, friendly, last seen near Bukit Timah" \
    --top-k 5

# Image only
python main.py search --image path/to/lost_pet.jpg

# Text only
python main.py search --description "small brown dog with floppy ears"
```

### 4. Check Database Status

```bash
python main.py stats
```

## Python API Usage

```python
from lost_pet_identifier import LostPetIdentifier

# Initialize
identifier = LostPetIdentifier(
    vector_db_path="./data/faiss_index",
    ollama_url="http://localhost:11434",
    ollama_model="llama2"
)

# Add found pet
identifier.add_found_pet(
    image_path="found_dog.jpg",
    description="Small brown dog with floppy ears",
    location="Bukit Timah",
    date="2024-01-15"
)

# Search
results = identifier.search_lost_pet(
    image_path="lost_dog.jpg",
    description="Brown dog, friendly",
    k=5
)

# View results
for result in results['results']:
    print(f"Similarity: {result['similarity_score']:.3f}")
    print(f"Description: {result['description']}")
```

## Troubleshooting

### CLIP Installation Issues

If you encounter issues installing CLIP, try:
```bash
pip install git+https://github.com/openai/CLIP.git
```

### Ollama Connection Issues

- Ensure Ollama is running: `ollama serve`
- Check the URL: default is `http://localhost:11434`
- Verify model is pulled: `ollama list`

### CUDA/GPU Issues

- For CPU-only: use `faiss-cpu` (already in requirements.txt)
- For GPU: install `faiss-gpu` and ensure PyTorch with CUDA is installed

### Empty Database

If you get "Database is empty" errors:
1. Add some found pets first using `add-found` command
2. Check database with `python main.py stats`

## Next Steps

1. **Add more found pets** to build a comprehensive database
2. **Test with real images** to see similarity matching in action
3. **Experiment with different descriptions** to see how text affects results
4. **Review the code** in `lost_pet_identifier/` to understand the architecture

## Project Structure

```
BirdNet/
├── lost_pet_identifier/    # Main package
│   ├── ingestion.py        # Data ingestion
│   ├── embeddings.py       # CLIP embeddings
│   ├── llm_extractor.py    # LLaMA feature extraction
│   ├── vector_db.py        # FAISS vector database
│   ├── matcher.py          # Similarity matching
│   ├── explainer.py        # Result explanations
│   └── pipeline.py         # Main orchestrator
├── main.py                 # CLI interface
├── example_usage.py        # Example code
├── tests/                  # Test scripts
└── data/                   # Database storage (auto-created)
```

## Testing

Run basic tests:
```bash
python tests/test_basic.py
```

## Support

For issues or questions, refer to the main README.md or the project documentation.

