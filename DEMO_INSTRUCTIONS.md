# Demo Instructions - Lost Pet Identifier Prototype

## Quick Start for Demonstrations

### Start the Web Interface

```bash
# Activate environment
source venv/bin/activate

# Set environment variable (macOS)
export KMP_DUPLICATE_LIB_OK=TRUE

# Start the interface
streamlit run app.py
```

The interface will automatically open at `http://localhost:8501`

## Recommended Demo Flow

### Step 1: Show Empty Database
- Open the interface
- Point out the sidebar showing "0 pets in database"
- Explain this is a fresh system

### Step 2: Add Found Pets (3-5 examples)

**Found Pet #1:**
- Description: "Small brown dog with floppy ears, friendly, found near Bukit Timah"
- Location: "Bukit Timah"
- Date: Today's date
- **Explain**: This demonstrates text-only input (no image needed)

**Found Pet #2:**
- Description: "Black and white cat, medium size, shy"
- Location: "Orchard Road"
- **Explain**: Shows how the system handles different species

**Found Pet #3:**
- Description: "Golden retriever, large, friendly"
- Location: "Marina Bay"
- **Explain**: Demonstrates size variations

**Found Pet #4:**
- Description: "Small brown dog with pointy ears, energetic"
- Location: "Sentosa"
- **Explain**: Shows similar but different from Pet #1

### Step 3: Demonstrate Search

**Search #1: Exact Match**
- Description: "Small brown dog with floppy ears, friendly"
- **Expected**: Should match Found Pet #1 with high similarity (>0.9)
- **Point out**: 
  - High similarity score (green)
  - Explanation showing why it matched
  - Location information

**Search #2: Partial Match**
- Description: "Brown dog, friendly"
- **Expected**: Should match both brown dogs with good similarity
- **Point out**:
  - Multiple matches ranked by similarity
  - How the system handles partial descriptions

**Search #3: Different Species**
- Description: "Black and white cat"
- **Expected**: Should match Found Pet #2 with high similarity
- **Point out**:
  - Cross-species matching works correctly
  - Cat matches don't appear for dog searches

**Search #4: Vague Description**
- Description: "Small dog"
- **Expected**: Should match small dogs but with lower specificity
- **Point out**:
  - System handles vague queries
  - Still provides useful results

### Step 4: Show Advanced Features

1. **Image Upload** (if you have sample images):
   - Upload an image of a pet
   - Show how visual similarity works
   - Explain multimodal matching

2. **Settings Panel**:
   - Adjust number of results (show top 3, top 5, top 10)
   - Toggle explanations on/off
   - Show database statistics

3. **Explanation Feature**:
   - Point out the AI-generated explanations
   - Explain how LLaMA provides reasoning
   - Note: Falls back to basic explanations if Ollama not running

## Talking Points

### System Architecture
- "This system orchestrates multiple AI models: CLIP for visual/text similarity, LLaMA for semantic understanding, and FAISS for efficient search."

### Multimodal Approach
- "The system accepts images, text, or both. This flexibility is crucial for real-world pet recovery scenarios where information may be incomplete."

### Similarity-Based Retrieval
- "Rather than exact matching, we use similarity scores. This is more robust for real-world data where descriptions vary."

### Human-in-the-Loop
- "The system provides ranked results, not automated decisions. Users make the final verification, ensuring accuracy and trust."

### Technical Highlights
- "CLIP embeddings enable cross-modal matching - we can compare images to text descriptions."
- "FAISS provides sub-millisecond search even with thousands of pets."
- "The system works offline and processes everything locally for privacy."

## Troubleshooting During Demo

### If Ollama Not Running
- **Say**: "The system gracefully falls back to keyword-based extraction. This demonstrates robustness."
- **Show**: The warnings are informational, not errors

### If Database Empty
- **Say**: "Let me add a few sample pets first to demonstrate the search functionality."

### If Search Takes Time
- **Say**: "The first search loads the CLIP model (~500MB). Subsequent searches are much faster."

## Key Metrics to Highlight

- **Similarity Scores**: 0.0-1.0 scale, >0.7 is high confidence
- **Search Speed**: <10ms after initial model load
- **Database Size**: Scales to thousands of pets
- **Embedding Dimension**: 512-dimensional vectors
- **Modalities**: Image, text, or combined

## Closing Points

1. **Feasibility**: "This prototype demonstrates that orchestrating multiple AI models is technically feasible and produces useful results."

2. **Real-World Application**: "The system addresses a real problem - reducing manual search effort for lost pets."

3. **Future Enhancements**: "Potential improvements include location filtering, domain-specific models like BirdNET, and weighted fusion of embeddings."

4. **Evaluation Ready**: "The system is ready for user-based evaluation and quantitative testing."

## Tips for Smooth Demo

- Have sample pet descriptions ready
- Test the interface before the demo
- Keep the database small for faster demonstration
- Use clear, descriptive pet descriptions
- Point out the color-coded similarity scores
- Show both successful matches and edge cases

## Additional Resources

- See `INTERFACE_GUIDE.md` for technical details
- See `QUICKSTART.md` for setup instructions
- See `IMPLEMENTATION_SUMMARY.md` for architecture details

