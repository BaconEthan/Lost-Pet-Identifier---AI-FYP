# Getting Started - Lost Pet Identifier

## System Status

Your Lost Pet Identifier system is **fully implemented and tested**! Here's what's ready:

### Core Components
- CLIP embedding generation (images & text)
- LLM feature extraction (with Ollama fallback)
- FAISS vector database
- Similarity matching engine
- Result explanation generation
- CLI interface
- Python API

### Installation Complete
- Virtual environment created
- All dependencies installed
- Tests passing
- Demo working

## Quick Test

### Option 1: Web Interface (Best for Demo)

```bash
source venv/bin/activate
export KMP_DUPLICATE_LIB_OK=TRUE  # macOS only
streamlit run app.py
```

The web interface will open in your browser with a full UI for adding and searching pets.

### Option 2: Command Line Demo

```bash
source venv/bin/activate
export KMP_DUPLICATE_LIB_OK=TRUE  # macOS only
python3 demo.py
```

## Next Steps

### 1. Start Ollama (Optional but Recommended)

For better semantic feature extraction:

```bash
# Install Ollama from https://ollama.ai
ollama serve

# In another terminal:
ollama pull llama2
```

The system works without Ollama but uses keyword-based extraction as fallback.

### 2. Add Real Found Pets

```bash
source venv/bin/activate
export KMP_DUPLICATE_LIB_OK=TRUE

# Add a found pet with image
python3 main.py add-found \
    --image path/to/pet.jpg \
    --description "Small brown dog with floppy ears" \
    --location "Bukit Timah" \
    --date "2024-01-15"

# Or text-only
python3 main.py add-found \
    --description "Black and white cat, medium size" \
    --location "Orchard Road"
```

### 3. Search for Lost Pets

```bash
# With image and description
python3 main.py search \
    --image path/to/lost_pet.jpg \
    --description "Brown dog, friendly" \
    --top-k 5

# Text-only search
python3 main.py search \
    --description "small brown dog with floppy ears"
```

### 4. Check Database

```bash
python3 main.py stats
```

## Using the Python API

```python
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'  # macOS

from lost_pet_identifier import LostPetIdentifier

# Initialize
identifier = LostPetIdentifier()

# Add found pet
identifier.add_found_pet(
    image_path="pet.jpg",
    description="Small brown dog",
    location="Bukit Timah"
)

# Search
results = identifier.search_lost_pet(
    image_path="lost.jpg",
    description="Brown dog",
    k=5
)

# View results
for result in results['results']:
    print(f"Similarity: {result['similarity_score']:.3f}")
    print(f"Description: {result['description']}")
```

## Environment Setup

### macOS Users

Add this to your `~/.zshrc` or `~/.bashrc`:

```bash
export KMP_DUPLICATE_LIB_OK=TRUE
```

Then reload:
```bash
source ~/.zshrc
```

### Linux/Windows Users

No special environment variable needed.

## Troubleshooting

### "ModuleNotFoundError"
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### "Ollama API call failed"
- This is normal if Ollama isn't running
- System falls back to keyword-based extraction
- To enable LLM features: `ollama serve` and `ollama pull llama2`

### "OpenMP Error" (macOS)
- Set environment variable: `export KMP_DUPLICATE_LIB_OK=TRUE`
- Or add to shell config file

### "Database is empty"
- Add some found pets first using `add-found` command
- Check with `python3 main.py stats`

## Project Structure

```
BirdNet/
├── lost_pet_identifier/    # Core package
│   ├── ingestion.py       # Data loading
│   ├── embeddings.py      # CLIP embeddings
│   ├── llm_extractor.py  # LLaMA integration
│   ├── vector_db.py       # FAISS database
│   ├── matcher.py         # Similarity matching
│   ├── explainer.py       # Explanations
│   └── pipeline.py        # Main orchestrator
├── main.py                # CLI interface
├── demo.py                # Demo script
├── tests/                 # Test suite
└── data/                  # Database storage
```

## What's Working

**Multimodal Matching**: Image-only, text-only, or combined queries
**Semantic Extraction**: LLaMA extracts structured features (with fallback)
**Similarity Ranking**: Cosine similarity with top-k results
**Explanations**: Natural language explanations for matches
**CLI & API**: Both interfaces fully functional
**Persistence**: Database saves to disk automatically

## Performance Notes

- **CLIP Model**: Loads on first use (~500MB)
- **Embedding Generation**: ~100-200ms per image/text
- **Search Speed**: Very fast (<10ms for small databases)
- **Database Size**: Scales well up to thousands of pets

## Ready for Evaluation

The system is ready for prototype evaluation as described in your design document. You can:

1. Test with real pet images
2. Evaluate retrieval quality
3. Measure similarity score distributions
4. Gather user feedback
5. Extend with additional features

## Support

- See `README.md` for overview
- See `QUICKSTART.md` for detailed setup
- See `IMPLEMENTATION_SUMMARY.md` for technical details
- Run `python3 main.py --help` for CLI usage

Happy pet matching!

