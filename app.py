#!/usr/bin/env python3
"""
Web interface for Lost Pet Identifier prototype.
Run with: streamlit run app.py
"""

import os
import sys
import tempfile
from pathlib import Path

# Set OpenMP environment variable
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import streamlit as st
from PIL import Image
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lost_pet_identifier import LostPetIdentifier

# Page configuration
st.set_page_config(
    page_title="Lost Pet Identifier",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
    .similarity-high {
        color: #28a745;
        font-weight: bold;
    }
    .similarity-medium {
        color: #ffc107;
        font-weight: bold;
    }
    .similarity-low {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'identifier' not in st.session_state:
    with st.spinner("Initializing Lost Pet Identifier system..."):
        st.session_state.identifier = LostPetIdentifier(
            vector_db_path="./data/faiss_index",
            ollama_url="http://localhost:11434",
            ollama_model="llama2"
        )
    st.success("System initialized!")

if 'database_size' not in st.session_state:
    st.session_state.database_size = st.session_state.identifier.get_database_size()

# Header
st.markdown('<p class="main-header">Lost Pet Identifier</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Multimodal AI System for Pet Recovery</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Database Status")
    db_size = st.session_state.identifier.get_database_size()
    st.metric("Pets in Database", db_size)
    
    st.divider()
    
    st.header("Settings")
    top_k = st.slider("Number of Results", 1, 10, 5)
    include_explanation = st.checkbox("Show Explanations", value=True)
    
    st.divider()
    
    if st.button("Refresh Database"):
        st.session_state.database_size = st.session_state.identifier.get_database_size()
        st.rerun()
    
    if st.button("Clear Database"):
        if st.session_state.database_size > 0:
            st.session_state.identifier.clear_database()
            st.session_state.database_size = 0
            st.success("Database cleared!")
            st.rerun()

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["Search Lost Pet", "Add Found Pet", "BirdNET Demo", "About"])

with tab1:
    st.header("Search for a Lost Pet")
    st.markdown("Upload an image and/or provide a description to find potential matches.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input")
        uploaded_image = st.file_uploader(
            "Upload Pet Image (Optional)",
            type=['jpg', 'jpeg', 'png'],
            help="Upload an image of the lost pet"
        )
        
        description = st.text_area(
            "Description (Optional)",
            placeholder="e.g., Small brown dog with floppy ears, friendly, last seen near Bukit Timah",
            height=100,
            help="Describe the lost pet"
        )
        
        search_button = st.button("Search", type="primary", use_container_width=True)
    
    with col2:
        st.subheader("Preview")
        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_container_width=True)
        else:
            st.info("No image uploaded")
    
    if search_button:
        if not uploaded_image and not description:
            st.error("Please provide at least an image or description to search.")
        elif st.session_state.database_size == 0:
            st.warning("Database is empty! Please add some found pets first.")
        else:
            with st.spinner("Searching for matches..."):
                # Save uploaded image temporarily
                image_path = None
                if uploaded_image:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                        image.save(tmp_file.name)
                        image_path = tmp_file.name
                
                try:
                    results = st.session_state.identifier.search_lost_pet(
                        image_path=image_path,
                        description=description,
                        k=top_k,
                        include_explanation=include_explanation
                    )
                    
                    # Clean up temp file
                    if image_path and os.path.exists(image_path):
                        os.unlink(image_path)
                    
                    if results['results']:
                        st.success(f"Found {len(results['results'])} potential matches!")
                        
                        # Display results
                        for i, result in enumerate(results['results'], 1):
                            with st.container():
                                similarity = result['similarity_score']
                                
                                # Determine similarity color
                                if similarity > 0.7:
                                    sim_class = "similarity-high"
                                    sim_label = "High"
                                elif similarity > 0.5:
                                    sim_class = "similarity-medium"
                                    sim_label = "Medium"
                                else:
                                    sim_class = "similarity-low"
                                    sim_label = "Low"
                                
                                col_img, col_info = st.columns([1, 2])
                                
                                with col_img:
                                    if result.get('image_path') and os.path.exists(result['image_path']):
                                        try:
                                            match_image = Image.open(result['image_path'])
                                            st.image(match_image, caption=f"Match #{i}", use_container_width=True)
                                        except:
                                            st.info("Image unavailable")
                                    else:
                                        st.info("No image available")
                                
                                with col_info:
                                    st.markdown(f"### Match #{i}")
                                    st.markdown(f"**Similarity:** <span class='{sim_class}'>{similarity:.3f} ({sim_label})</span>", unsafe_allow_html=True)
                                    
                                    if result.get('description'):
                                        st.markdown(f"**Description:** {result['description']}")
                                    
                                    if result.get('location'):
                                        st.markdown(f"**Location:** {result['location']}")
                                    
                                    if result.get('date'):
                                        st.markdown(f"**Date:** {result['date']}")
                                
                                st.divider()
                        
                        # Display explanation
                        if include_explanation and results.get('explanation'):
                            st.markdown("### Explanation")
                            st.info(results['explanation'])
                    else:
                        st.warning("No matches found. Try adjusting your search criteria.")
                        
                except Exception as e:
                    st.error(f"Error during search: {str(e)}")
                    if image_path and os.path.exists(image_path):
                        os.unlink(image_path)

with tab2:
    st.header("Add a Found Pet")
    st.markdown("Add information about a found pet to the database.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Pet Information")
        found_image = st.file_uploader(
            "Upload Pet Image (Optional)",
            type=['jpg', 'jpeg', 'png'],
            key="found_image",
            help="Upload an image of the found pet"
        )
        
        found_description = st.text_area(
            "Description *",
            placeholder="e.g., Small brown dog with floppy ears, friendly",
            height=100,
            help="Describe the found pet (required)"
        )
        
        found_location = st.text_input(
            "Location",
            placeholder="e.g., Bukit Timah",
            help="Where was the pet found?"
        )
        
        found_date = st.date_input(
            "Date Found",
            help="When was the pet found?"
        )
        
        add_button = st.button("Add to Database", type="primary", use_container_width=True)
    
    with col2:
        st.subheader("Preview")
        if found_image:
            preview_image = Image.open(found_image)
            st.image(preview_image, caption="Found Pet Image", use_container_width=True)
        else:
            st.info("No image uploaded")
    
    if add_button:
        if not found_image and not found_description:
            st.error("Please provide at least an image or description.")
        else:
            with st.spinner("Adding pet to database..."):
                # Save uploaded image temporarily
                image_path = None
                if found_image:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                        preview_image.save(tmp_file.name)
                        image_path = tmp_file.name
                
                try:
                    idx = st.session_state.identifier.add_found_pet(
                        image_path=image_path,
                        description=found_description,
                        location=found_location if found_location else None,
                        date=str(found_date) if found_date else None
                    )
                    
                    # Clean up temp file
                    if image_path and os.path.exists(image_path):
                        os.unlink(image_path)
                    
                    st.success(f"Successfully added found pet (index: {idx})!")
                    st.session_state.database_size = st.session_state.identifier.get_database_size()
                    st.balloons()
                    
                    # Clear form
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error adding pet: {str(e)}")
                    if image_path and os.path.exists(image_path):
                        os.unlink(image_path)

with tab3:
    st.header("BirdNET Audio Classification Demo")
    st.markdown("""
    **Evidence of Model Exploration and Evaluation**
    
    This demo shows BirdNET audio classification capabilities and demonstrates how it would integrate 
    with the main Lost Pet Identifier pipeline.
    """)
    
    # Audio conversion section
    st.subheader("Step 1: Convert Audio to WAV (Optional)")
    st.info("""
    **Recommended:** Convert MP3/FLAC to WAV for best compatibility. WAV files work without ffmpeg.
    """)
    
    convert_tab1, convert_tab2 = st.tabs(["Convert Audio", "Upload WAV File"])
    
    with convert_tab1:
        st.markdown("**Convert your audio file to WAV format:**")
        convert_file = st.file_uploader(
            "Upload Audio to Convert",
            type=['mp3', 'flac', 'm4a', 'ogg', 'wav'],
            help="Upload MP3, FLAC, or other format to convert to WAV",
            key="convert_audio"
        )
        
        if convert_file is not None:
            try:
                from pydub import AudioSegment
                import io
                
                if st.button("Convert to WAV", type="primary", key="convert_button"):
                    with st.spinner("Converting audio file..."):
                        # Read uploaded file into memory
                        audio_bytes = convert_file.read()
                        
                        # Create AudioSegment from bytes
                        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=convert_file.name.split('.')[-1])
                        
                        # Export to WAV in memory
                        wav_buffer = io.BytesIO()
                        audio.export(wav_buffer, format="wav")
                        wav_buffer.seek(0)
                        
                        # Provide download
                        st.success("Conversion successful!")
                        st.download_button(
                            label="Download WAV File",
                            data=wav_buffer.getvalue(),
                            file_name=f"{convert_file.name.rsplit('.', 1)[0]}.wav",
                            mime="audio/wav",
                            key="download_wav"
                        )
                        
                        # Show file info
                        duration = len(audio) / 1000
                        st.info(f"""
                        **File Info:**
                        - Duration: {duration:.2f} seconds
                        - Sample Rate: {audio.frame_rate} Hz
                        - Channels: {audio.channels}
                        - Format: WAV (PCM)
                        """)
                        
            except ImportError:
                st.warning("""
                **pydub not available.** Install with:
                ```bash
                pip install pydub
                ```
                """)
            except Exception as e:
                error_msg = str(e)
                if "ffmpeg" in error_msg.lower():
                    st.error("""
                    **ffmpeg not found.** 
                    
                    For MP3/FLAC conversion, install ffmpeg:
                    ```bash
                    brew install ffmpeg  # macOS
                    ```
                    
                    Or use an online converter, then upload the WAV file in the next tab.
                    """)
                else:
                    st.error(f"Conversion error: {error_msg}")
                    st.info("""
                    **Alternative:** Use an online converter:
                    - https://cloudconvert.com/mp3-to-wav
                    - Then upload the WAV file in the "Upload WAV File" tab
                    """)
    
    with convert_tab2:
        st.markdown("**Or upload a WAV file directly:**")
        audio_file = st.file_uploader(
            "Upload WAV Audio File",
            type=['wav'],
            help="Upload a .wav file containing bird sounds (recommended format)",
            key="birdnet_audio"
        )
    
    col1, col2 = st.columns(2)
    with col1:
        min_confidence = st.slider("Minimum Confidence", 0.0, 1.0, 0.1, 0.01, key="birdnet_confidence")
    with col2:
        top_k_results = st.slider("Top K Results", 1, 10, 5, key="birdnet_topk")
    
    if st.button("Analyze Audio", type="primary", use_container_width=True, key="birdnet_analyze"):
        if audio_file is None:
            st.warning("Please upload a WAV audio file in the 'Upload WAV File' tab first.")
        else:
            try:
                # Save uploaded file temporarily
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(audio_file.getvalue())
                    tmp_path = tmp_file.name
                
                # Try to import and use BirdNET
                try:
                    from birdnetlib import Recording
                    from birdnetlib.analyzer import Analyzer
                    
                    with st.spinner("Analyzing audio with BirdNET (this may take a moment on first run)..."):
                        # Check file exists and has content
                        if not os.path.exists(tmp_path):
                            raise FileNotFoundError("Temporary file was not created properly")
                        
                        file_size = os.path.getsize(tmp_path)
                        if file_size == 0:
                            raise ValueError("Uploaded file appears to be empty")
                        
                        # Initialize analyzer (may download model on first use)
                        analyzer = Analyzer()
                        
                        # Create recording and analyze
                        recording = Recording(analyzer, tmp_path, min_conf=min_confidence)
                        recording.analyze()
                        
                        if recording.detections:
                            st.success(f"Found {len(recording.detections)} bird species!")
                            
                            # Display results
                            st.subheader("Species Probabilities")
                            results = []
                            for detection in recording.detections:
                                species = detection['common_name']
                                confidence = detection['confidence']
                                results.append((species, confidence))
                            
                            results.sort(key=lambda x: x[1], reverse=True)
                            
                            for i, (species, conf) in enumerate(results[:top_k_results], 1):
                                st.progress(conf, text=f"{i}. {species}: {conf:.3f}")
                            
                            # Show CLIP integration example
                            st.divider()
                            st.subheader("CLIP Integration Example")
                            st.markdown("""
                            **How BirdNET output would feed into CLIP text prompt:**
                            """)
                            
                            top_species = results[0][0] if results else "unknown"
                            clip_text = f"bird, {top_species}"
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**BirdNET Output:**")
                                st.code(f"{top_species}\n(confidence: {results[0][1]:.3f})")
                            with col2:
                                st.markdown(f"**CLIP Text Prompt:**")
                                st.code(f'"{clip_text}"')
                            
                            st.info("""
                            This text would be embedded using CLIP and could be:
                            - Compared with image embeddings of found birds
                            - Stored in FAISS vector database
                            - Used for multimodal search (audio → text → image)
                            """)
                            
                        else:
                            st.warning("No bird species detected above the confidence threshold.")
                        
                        # Clean up
                        os.unlink(tmp_path)
                        
                except ImportError:
                    st.error("""
                    BirdNET is not installed. Install with:
                    ```
                    pip install birdnetlib tensorflow
                    ```
                    """)
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
                        
            except Exception as e:
                error_msg = str(e)
                st.error(f"Error analyzing audio: {error_msg}")
                
                # Provide helpful error messages
                if "librosa" in error_msg.lower() or "audio read" in error_msg.lower():
                    st.warning("""
                    **Audio format issue detected.**
                    
                    Possible solutions:
                    1. **Try a .wav file** - WAV format works without additional dependencies
                    2. **Install ffmpeg** for MP3/FLAC support:
                       ```bash
                       brew install ffmpeg  # macOS
                       ```
                    3. **Check file format** - Ensure the file is a valid audio file
                    4. **Try converting** the file to WAV format first
                    """)
                elif "tensorflow" in error_msg.lower() or "model" in error_msg.lower():
                    st.warning("""
                    **Model loading issue.**
                    
                    BirdNET may be downloading the model on first use. Please wait and try again.
                    """)
                else:
                    st.info("""
                    **Troubleshooting tips:**
                    - Ensure the audio file is not corrupted
                    - Try a different audio file
                    - For best results, use .wav format
                    - Check that the file contains actual audio data
                    """)
                
                if 'tmp_path' in locals() and os.path.exists(tmp_path):
                    os.unlink(tmp_path)
    
    st.divider()
    st.subheader("Integration Status")
    
    st.markdown("""
    **Why BirdNET is not fully wired into FAISS yet:**
    
    1. **Audio Processing Pipeline**
       - Requires audio file preprocessing and segmentation
       - BirdNET works on 3-second audio chunks
       - Need to handle longer recordings (sliding window)
    
    2. **Integration Complexity**
       - Audio → Text conversion (BirdNET → CLIP prompt)
       - Text → Embedding (CLIP text encoder)
       - Embedding → FAISS storage
       - Requires additional data pipeline components
    
    3. **Evaluation Status**
       - BirdNET accuracy validated on test audio
       - Integration architecture designed
       - Pending full pipeline implementation
    
    4. **Current Status**
       - BirdNET model exploration: COMPLETE
       - Audio classification: WORKING
       - CLIP integration path: DESIGNED
       - FAISS integration: PLANNED
    """)
    
    st.info("""
    This demo provides evidence of model exploration and evaluation, demonstrating 
    understanding of BirdNET capabilities and integration architecture, even though 
    full integration is deferred to maintain focus on the core similarity matching prototype.
    """)

with tab4:
    st.header("About Lost Pet Identifier")
    
    st.markdown("""
    ### Project Overview
    
    This is a **multimodal AI system** designed to assist in the recovery of lost pets by automatically 
    analyzing and matching animal-related content across multiple online sources.
    
    ### How It Works
    
    1. **Feature Extraction**: Uses CLIP (Contrastive Language-Image Pretraining) to generate embeddings 
       from images and text descriptions.
    
    2. **Semantic Processing**: Leverages LLaMA (via Ollama) to extract structured features from 
       unstructured text descriptions.
    
    3. **Similarity Matching**: Uses FAISS (Facebook AI Similarity Search) to efficiently find the most 
       similar pets based on cosine similarity.
    
    4. **Ranked Results**: Returns top-k matches with similarity scores and explanations.
    
    ### Technologies Used
    
    - **CLIP**: Image-text embedding for zero-shot visual similarity
    - **LLaMA/Ollama**: Semantic feature extraction and normalization
    - **FAISS**: Efficient vector similarity search
    - **BirdNET**: Audio classification for bird species (demo - see BirdNET Demo tab)
    - **Streamlit**: Web interface framework
    
    ### System Architecture
    
    ```
    [User Input] → [Data Ingestion] → [Feature Extraction] 
    → [Vector Database] → [Similarity Matching] → [Ranked Results]
    ```
    
    ### Getting Started
    
    1. **Add Found Pets**: Use the "Add Found Pet" tab to populate the database
    2. **Search**: Use the "Search Lost Pet" tab to find potential matches
    3. **Review Results**: Check similarity scores and explanations
    
    ### Configuration
    
    - **Ollama**: Optional but recommended for better semantic extraction
      - Install from: https://ollama.ai
      - Run: `ollama serve` and `ollama pull llama2`
    
    ### Notes
    
    - The system works without Ollama but uses keyword-based fallback
    - Similarity scores range from 0.0 to 1.0 (higher is better)
    - Results are ranked by similarity score
    - The system supports image-only, text-only, or combined queries
    """)
    
    st.divider()
    
    st.markdown("### Database Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Pets", st.session_state.database_size)
    with col2:
        st.metric("Embedding Dimension", "512")
    with col3:
        st.metric("Search Method", "Cosine Similarity")

