# Video Demo Script - Lost Pet Identifier AI Orchestration Prototype

**Duration: 2-3 minutes**

---

## [SCENE 1: Introduction] (0:00 - 0:20)

**[Screen: Project title slide]**

**Narrator:**
"Today I'm demonstrating my AI orchestration prototype: a multimodal Lost Pet Identifier system. This project orchestrates multiple pre-trained AI models to solve a real-world problem - helping pet owners find their lost animals more efficiently."

**[Screen: Show web interface]**

**Narrator:**
"The system combines CLIP for visual-text similarity, LLaMA for semantic understanding, and BirdNET for audio classification, all orchestrated through a unified pipeline."

---

## [SCENE 2: Problem Statement] (0:20 - 0:35)

**[Screen: Show empty database]**

**Narrator:**
"Currently, pet owners must manually search through hundreds of social media posts and community forums. This is time-consuming, emotionally taxing, and prone to error."

**[Screen: Show interface]**

**Narrator:**
"Our system automates this process by using AI to match lost and found pet posts based on visual, textual, and audio similarity."

---

## [SCENE 3: Core Feature - Adding Found Pets] (0:35 - 0:55)

**[Screen: "Add Found Pet" tab]**

**Narrator:**
"Let me demonstrate by adding some found pets to the database."

**[Action: Add 2-3 found pets with descriptions]**

**Narrator:**
"Notice how the system uses LLaMA to extract structured features from unstructured text descriptions. This semantic normalization is crucial for accurate matching."

**[Screen: Show database stats updating]**

**Narrator:**
"Each pet is processed through CLIP to generate embeddings, which are stored in a FAISS vector database for efficient similarity search."

---

## [SCENE 4: Core Feature - Searching] (0:55 - 1:25)

**[Screen: "Search Lost Pet" tab]**

**Narrator:**
"Now let's search for a lost pet. I'll use both an image and a text description."

**[Action: Upload image and enter description, then search]**

**Narrator:**
"The system generates embeddings for the query using CLIP, then searches the FAISS database using cosine similarity."

**[Screen: Show results with similarity scores]**

**Narrator:**
"Results are ranked by similarity score, with the most likely matches appearing first. The system also generates natural language explanations using LLaMA, explaining why certain matches were ranked highly."

**[Screen: Highlight explanation]**

**Narrator:**
"This explainability feature improves user trust, especially important in emotionally sensitive contexts like lost pets."

---

## [SCENE 5: BirdNET Audio Demo] (1:25 - 1:55)

**[Screen: "BirdNET Demo" tab]**

**Narrator:**
"As evidence of model exploration, I've integrated BirdNET for audio classification. This demonstrates how the system could handle audio queries in the future."

**[Action: Upload audio file and analyze]**

**Narrator:**
"BirdNET processes the audio and returns species probabilities. The output is formatted as text that would feed into CLIP for embedding generation."

**[Screen: Show CLIP integration example]**

**Narrator:**
"While not fully integrated into the FAISS pipeline yet, this demonstrates the integration architecture and validates BirdNET's capabilities for the domain."

---

## [SCENE 6: Technical Architecture] (1:55 - 2:20)

**[Screen: Architecture diagram or code view]**

**Narrator:**
"The system orchestrates multiple models: CLIP handles multimodal embeddings, LLaMA provides semantic reasoning, and FAISS enables efficient vector search."

**[Screen: Show pipeline flow]**

**Narrator:**
"Each component operates on different data modalities, and the orchestration layer combines their outputs to produce ranked, explainable results."

---

## [SCENE 7: Conclusion] (2:20 - 2:35)

**[Screen: Summary view]**

**Narrator:**
"This prototype successfully demonstrates that orchestrating multiple pre-trained AI models can solve real-world problems effectively."

**[Screen: Key achievements]**

**Narrator:**
"The system provides evidence of model exploration, technical feasibility, and thoughtful architecture design. Future work includes full BirdNET integration, location filtering, and user-based evaluation."

**[Screen: Final slide]**

**Narrator:**
"Thank you for watching. This demonstrates how AI orchestration can create practical, explainable solutions for complex, multimodal problems."

---

## Production Notes

### Key Points to Emphasize:
1. **Orchestration** - Multiple models working together
2. **Multimodal** - Image, text, and audio support
3. **Explainability** - LLaMA-generated explanations
4. **Real-world application** - Practical problem solving
5. **Model exploration** - BirdNET integration evidence

### Visual Elements:
- Clear screen recordings of interface
- Highlight similarity scores and explanations
- Show architecture diagram
- Smooth transitions between features

### Timing:
- Keep each scene concise
- Allow time for actions to complete on screen
- Pause briefly after key demonstrations

### Tips:
- Practice the flow before recording
- Have sample data ready (found pets, test images)
- Ensure audio file is ready for BirdNET demo
- Test all features work before recording

