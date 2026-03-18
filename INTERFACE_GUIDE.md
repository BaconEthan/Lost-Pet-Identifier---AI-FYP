# Web Interface Guide - Lost Pet Identifier

## Quick Start

### Option 1: Using the Run Script (Easiest)

```bash
./run_interface.sh
```

### Option 2: Manual Start

```bash
# Activate virtual environment
source venv/bin/activate

# Set environment variable (macOS)
export KMP_DUPLICATE_LIB_OK=TRUE

# Install Streamlit if needed
pip install streamlit

# Run the app
streamlit run app.py
```

The interface will automatically open in your browser at `http://localhost:8501`

## Interface Features

### Main Tabs

1. **Search Lost Pet**
   - Upload an image of the lost pet
   - Enter a text description
   - View ranked matches with similarity scores
   - See explanations for why matches were found

2. **Add Found Pet**
   - Upload an image (optional)
   - Enter description, location, and date
   - Add pets to the database

3. **About**
   - System overview and documentation
   - Technology stack information
   - Database statistics

### Sidebar Features

- **Database Status**: Shows current number of pets in database
- **Settings**: Adjust number of results and explanation display
- **Refresh**: Update database statistics
- **Clear**: Remove all pets from database

## Demonstration Tips

### For Presentations/Demos:

1. **Start with Empty Database**
   - Show the "Add Found Pet" tab
   - Add 3-5 sample pets with descriptions
   - Explain the multimodal input (image + text)

2. **Demonstrate Search**
   - Use the "Search Lost Pet" tab
   - Show image-only search
   - Show text-only search
   - Show combined search
   - Highlight similarity scores and explanations

3. **Show Features**
   - Point out the similarity score colors (green/yellow/red)
   - Show how results are ranked
   - Demonstrate the explanation feature

### Sample Demo Flow:

```
1. Add Found Pet #1:
   - Description: "Small brown dog with floppy ears, friendly"
   - Location: "Bukit Timah"
   
2. Add Found Pet #2:
   - Description: "Black and white cat, medium size, shy"
   - Location: "Orchard Road"
   
3. Search for Lost Pet:
   - Description: "Brown dog, friendly, last seen near Bukit Timah"
   - Show how it matches Found Pet #1 with high similarity
   
4. Show Explanation:
   - Point out the AI-generated explanation
   - Explain how the system reasons about matches
```

## Troubleshooting

### Port Already in Use
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

### Interface Not Loading
- Check that all dependencies are installed: `pip install streamlit`
- Ensure virtual environment is activated
- Check browser console for errors

### Images Not Displaying
- Ensure image files are in supported formats (JPG, PNG)
- Check file permissions
- Try refreshing the page

## Screenshots for Documentation

The interface includes:
- Clean, modern design
- Color-coded similarity scores
- Image previews
- Real-time database statistics
- Responsive layout

## Sharing Your Prototype

### Local Network Access
```bash
# Allow access from other devices on your network
streamlit run app.py --server.address 0.0.0.0
```

### For Remote Access
Consider deploying to:
- Streamlit Cloud (free)
- Heroku
- AWS/GCP/Azure
- Docker container

## Notes

- The interface persists data in `./data/faiss_index`
- Images are temporarily stored during upload
- The system works offline (except Ollama features)
- All processing happens locally for privacy

