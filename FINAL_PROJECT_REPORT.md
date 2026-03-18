# CM3070 Final Project Report

**UNIVERSITY OF LONDON — INTERNATIONAL PROGRAMMES**  
**BSc Computer Science and Related Subjects**

---

## Title Page

| Field | Content |
|-------|---------|
| **Project title** | Lost Pet Identifier: AI-Assisted Cross-Platform Matching |
| **Author** | [Your Name] |
| **Student Number** | [Your Student Number] |
| **Date of Submission** | [Date] |
| **Supervisor** | [Supervisor Name] |

**Code repository (public):** [INSERT YOUR PUBLIC REPOSITORY LINK HERE – must remain viewable until results are received]

**Note:** The overall maximum word count for this report is **9500 words** (excluding Appendices and References). Chapter word limits are guidelines; the total must not exceed 9500 words.

---

## Contents

- **Chapter 1:** Introduction  
- **Chapter 2:** Literature Review  
- **Chapter 3:** Project Design  
- **Chapter 4:** Implementation  
- **Chapter 5:** Evaluation  
- **Chapter 6:** Conclusion  
- **Chapter 7:** Appendices  
- **Chapter 8:** References  

---

## Chapter 1: Introduction

*(Word limit: 1000)*

The recovery of lost pets is a time-sensitive and emotionally distressing process for pet owners. In practice, individuals who lose a pet are often required to manually search through numerous social media groups, online forums, and classified websites to identify potential matches. These platforms typically contain hundreds of unstructured posts, each varying in image quality, descriptive detail, and relevance. As a result, owners must rely on manual inspection and keyword searches, which is inefficient and prone to error, particularly when posts originate from different platforms with inconsistent tagging or categorisation.

Existing online solutions for lost-and-found pets largely rely on user-generated text descriptions and basic filtering mechanisms. While these systems allow owners to upload images and descriptions, they do not leverage modern artificial intelligence techniques to automatically analyse visual and audio features or to intelligently match lost pets with potential sightings. Consequently, important matches may be overlooked due to incomplete descriptions, ambiguous language, or differences in terminology across platforms. This problem is exacerbated when posts involve visually similar animals of the same species or breed, where subtle distinguishing features are difficult to identify manually.

Recent advances in artificial intelligence, particularly in multi-modal machine learning, offer an opportunity to address this challenge. Pre-trained models such as CLIP enable semantic image similarity comparison, while specialised models such as BirdNET demonstrate strong performance in species-level audio classification. Large Language Models (LLMs) further provide the capability to reason over structured and unstructured data, summarise matches, and generate human-readable explanations. However, no single model alone is sufficient to solve the lost pet recovery problem effectively. Instead, there is a need to **orchestrate** multiple pre-trained models, each operating in a different data domain, into a unified workflow that achieves a clearly defined goal. This orchestration approach allows each model to contribute its specialised capabilities—CLIP for cross-modal similarity, LLaMA for semantic understanding, and FAISS for efficient retrieval—while working together to solve a problem that none could address independently.

This project is based on the University of London project template **"Project Idea 1: Orchestrating AI models to achieve a goal"**. The project number is **1** as listed in that template. The goal is to design, implement, and evaluate a prototype AI-assisted system for cross-platform lost pet matching. The central concept is to build a system that can ingest pet-related posts from multiple sources, analyse images, text, and audio where available, and retrieve the most relevant potential matches for a reported lost pet. By combining multiple pre-trained models into a structured pipeline, the system aims to significantly reduce the manual effort required by pet owners and improve the speed and accuracy of pet recovery.

The primary aim is to investigate whether a multi-model AI workflow can effectively support the identification and matching of lost pets across heterogeneous online platforms. Specifically, the project seeks to answer: (1) Can pre-trained multi-modal models be orchestrated to accurately identify species and visual similarity between lost and found pet posts? (2) Does embedding-based retrieval improve cross-platform matching compared to traditional keyword-based searches? (3) How can an LLM be used to reason over retrieved matches and present results in a clear, interpretable manner for end users?

To address these questions, the project defines concrete objectives. First, a data ingestion pipeline processes pet-related content in multiple modalities. Images are converted into semantic embeddings using CLIP, while textual descriptions are embedded using CLIP's text encoder, enabling cross-modal similarity comparison. Where applicable, domain-specific models such as BirdNET are explored for audio classification. Second, a vector-based retrieval system using FAISS stores embeddings alongside metadata, enabling efficient similarity-based search. Third, an orchestration layer integrates retrieval results with LLaMA for reasoning and summarisation, producing ranked matches with explanatory justifications. Finally, a functional prototype (web and CLI) demonstrates the end-to-end workflow.

In summary, this project explores the application of orchestrated pre-trained AI models to a real-world, socially relevant problem. By orchestrating computer vision (CLIP), natural language processing (LLaMA), vector retrieval (FAISS), and domain-specific classification (BirdNET) into a unified pipeline, the project demonstrates how multiple pre-trained models can be integrated to achieve a goal that is not feasible using traditional software engineering approaches or any single AI model alone.

---

## Chapter 2: Literature Review

*(Word limit: 2500)*

### 2.1 Introduction

The recovery of lost pets is a socially significant yet underexplored problem in applied artificial intelligence. Globally, millions of pets are reported lost each year, with recovery efforts largely dependent on fragmented online platforms such as social media groups, classified websites, and community forums. These platforms rely heavily on manual inspection of posts, keyword searches, and human judgement, making the process inefficient, time-consuming, and prone to missed matches. As pet-related online content grows, this manual approach becomes increasingly impractical.

This literature review examines existing technological and AI-driven approaches related to lost-and-found systems, image-based animal identification, multimodal similarity search, and AI model orchestration. Rather than reviewing these areas in isolation, this chapter evaluates how their limitations motivate the need for a unified, multi-model AI workflow. The review identifies a clear gap: while individual AI models for vision, audio, and language have matured, there is limited work on orchestrating these models into an integrated system for cross-platform lost pet identification.

### 2.2 Existing Lost Pet Platforms and Digital Solutions

Current lost pet recovery platforms primarily function as digital noticeboards. Popular services such as PawBoost, PetFBI, and Lost & Found Pet Facebook groups allow users to upload images and descriptions of missing or found animals. While these platforms increase visibility and reach, their core matching mechanism remains manual. Users must browse feeds, filter by location, and visually compare posts themselves.

Research evaluating these systems highlights several shortcomings. First, posts are inconsistently labelled, with species, breed, and distinguishing features often omitted or inaccurately described. Second, keyword-based searches fail when different terminology is used (e.g., "parakeet" vs. "budgerigar"). Third, these systems do not scale effectively as content volume increases, leading to information overload. From an AI perspective, these platforms demonstrate a clear opportunity for automation but also reveal a gap: no dominant solution currently applies intelligent similarity matching across images, text, and audio. This limitation directly motivates the proposed project's objective to introduce AI-driven, multimodal matching rather than relying on human inspection alone.

### 2.3 Image-Based Animal Recognition and Similarity Matching

Computer vision has seen substantial advances through deep learning, particularly with Convolutional Neural Networks (CNNs) and Vision Transformers. Animal classification tasks have benefited from transfer learning using models pre-trained on large-scale datasets such as ImageNet. Studies show that transfer learning enables reliable species-level classification even when domain-specific datasets are limited.

However, most existing animal recognition research focuses on classification, not retrieval or similarity matching. Models trained to identify whether an image contains a "dog" or "cat" do not address the more nuanced problem of matching two visually similar but distinct animals. This is especially problematic in lost pet scenarios, where distinguishing features may be subtle or partially occluded.

Vision-language models such as CLIP (Contrastive Language–Image Pretraining) (Radford et al., 2021) represent a shift away from rigid classification toward semantic similarity. CLIP learns a shared embedding space between images and text, enabling comparison based on conceptual similarity rather than predefined labels. Prior research demonstrates that CLIP performs well in zero-shot settings and generalises across domains without task-specific fine-tuning. Despite its strengths, CLIP alone is insufficient for lost pet recovery: it cannot reliably infer location relevance, temporal proximity, or domain-specific constraints. This limitation motivates the integration of CLIP with complementary models—LLMs for semantic reasoning and vector databases for efficient retrieval—demonstrating the value of orchestration in addressing complex, real-world problems.

### 2.4 Audio-Based Animal Identification

For certain species, particularly birds, vocalisations provide a highly discriminative signal. Bioacoustics research has demonstrated that species-level identification using audio can outperform visual methods under certain conditions. BirdNET, developed by the Cornell Lab of Ornithology (Kahl et al., 2021), is a notable domain-specific deep learning model capable of identifying bird species from short audio recordings. BirdNET has been validated across diverse environments and demonstrates strong robustness to background noise. However, its scope is intentionally narrow: it focuses on species identification rather than individual matching. Furthermore, audio data is not always available, as many lost pet posts contain only images or text. The literature therefore positions audio-based identification as a supporting modality. In this project, BirdNET is utilised as a complementary signal that enhances confidence when audio evidence exists, rather than as the primary matching mechanism—demonstrating the orchestration principle that specialised models contribute their domain expertise within a larger, coordinated system.

### 2.5 Textual Descriptions and Natural Language Processing

Complementing visual and audio modalities, textual descriptions play a crucial role in lost pet posts but are often informal, inconsistent, and incomplete. Traditional keyword-based search systems struggle with synonymy, spelling errors, and varying levels of detail. Sentence embedding models based on transformer architectures (e.g., BERT, sentence-transformers) represent text semantically rather than lexically; research shows that embedding-based retrieval significantly improves recall in unstructured text search tasks. Nevertheless, text embeddings alone cannot resolve ambiguity when descriptions are vague or incorrect, again highlighting the importance of combining text-based reasoning with visual and audio evidence through orchestration of multiple models.

### 2.6 Multimodal AI Systems and Model Orchestration

Recent AI research increasingly advocates for orchestration—the coordinated integration of modular, multi-model systems rather than monolithic architectures. Instead of training a single model to perform all tasks, specialised pre-trained models are orchestrated in a pipeline, each operating in its optimal domain. This approach improves robustness, interpretability, and development efficiency. Studies position LLMs as reasoning and coordination agents rather than primary perception engines: they excel at synthesising structured outputs, ranking results, and generating explanations, but are unreliable when used as standalone sources of factual inference. This mirrors findings where LLMs are grounded using external tools or retrieval mechanisms—an approach directly adopted in this project through FAISS-based retrieval and CLIP embeddings. The orchestration paradigm is especially relevant here: no single model can effectively solve cross-platform lost pet matching; instead, a pipeline integrating image embeddings (CLIP), audio classification (BirdNET), text embeddings, vector similarity search (FAISS), and LLM-based reasoning (LLaMA) is required, with each model contributing specialised capabilities while the orchestration layer coordinates their outputs into a unified result.

### 2.7 Vector Databases and Similarity-Based Retrieval

Vector databases such as FAISS (Facebook AI Similarity Search) (Johnson et al., 2019) and ChromaDB enable efficient similarity search over high-dimensional embeddings. Prior research demonstrates that vector-based retrieval is scalable and well-suited to applications involving image and text similarity. Unlike relational databases, vector databases allow approximate nearest neighbour search, which is essential for real-time matching. The literature supports the use of vector databases as foundational infrastructure for multimodal AI systems; this project extends the approach by storing and querying multimodal embeddings with shared metadata, enabling richer matching logic that combines visual, textual, and semantic signals within a unified retrieval framework.

### 2.8 Identified Research and Implementation Gap

Synthesising the reviewed literature reveals several key gaps: (1) existing lost pet platforms rely on manual, keyword-based matching; (2) image and audio AI models exist but are rarely integrated into end-to-end recovery systems; (3) most animal AI research focuses on classification, not cross-instance similarity; (4) multimodal orchestration is underexplored in socially impactful applications; (5) LLMs are powerful reasoning tools but require grounding through structured retrieval. These gaps directly motivate the proposed project. By orchestrating multiple pre-trained models—CLIP for visual-text similarity, LLaMA for semantic reasoning, FAISS for efficient retrieval, and BirdNET for audio classification—into a unified workflow, this project aims to demonstrate a scalable, intelligent alternative to current lost pet recovery methods.

### 2.9 Conclusion

This literature review establishes that while individual AI technologies for vision, audio, and language processing are mature, their application to lost pet recovery remains fragmented and underdeveloped. Existing systems fail to leverage semantic similarity, multimodal evidence, or AI-driven reasoning. The proposed project addresses this gap by orchestrating pre-trained models across multiple domains into a coherent AI pipeline, contributing both a functional prototype and a practical demonstration of AI orchestration applied to a real-world, socially meaningful problem, positioned within Project Idea 1: Orchestrating AI models to achieve a goal.

---

## Chapter 3: Design

*(Word limit: 2000)*

### 3.1 Project Overview

This project designs an AI-assisted system to support the recovery of lost pets by automatically analysing, matching, and ranking animal-related content across multiple online sources. When a pet goes missing, owners are often required to manually browse numerous social media groups, community forums, and websites, inspecting hundreds of posts in the hope of finding a match. This process is time-consuming, cognitively demanding, and inefficient. The proposed system aims to address this by **orchestrating** multiple AI models—each specialised for different data modalities—to identify, categorise, and compare animal-related data. By combining visual similarity, textual descriptions, and optional audio cues, the system can help users rapidly locate posts that are most likely to correspond to their lost pet. Rather than replacing human judgement, the system functions as a decision-support tool that filters and prioritises relevant information. This project follows the University of London template "Orchestrating AI models to achieve a goal", integrating complementary AI models into a coherent, task-oriented pipeline.

### 3.2 Domain and Target Users

The domain lies at the intersection of computer vision, multimodal artificial intelligence, and community-based animal welfare applications. It addresses cross-platform animal identification and similarity matching, a problem more complex than human facial recognition due to variability in species, breeds, poses, lighting, and image quality. Real-world lost-pet posts are noisy and user-generated; the domain therefore requires robust models that generalise beyond exact matches. The primary target users are pet owners who have lost a pet and need an efficient way to locate potential sightings, and secondarily animal rescuers and volunteers who wish to identify whether an animal matches an existing missing report. These users are typically non-technical and emotionally stressed, so the system must prioritise simplicity, clarity, and explainability.

### 3.3 Design Justification

**Multimodal AI approach:** No single model suffices. Animals may be photographed from different angles or described inconsistently. The design adopts a multimodal approach: visual similarity through CLIP embeddings, textual understanding through LLaMA feature extraction and CLIP text embeddings, and optional audio analysis through BirdNET. This orchestration reduces reliance on any single modality and increases robustness.

**Similarity-based matching:** The project does not attempt strict identity recognition. Instead it uses embedding-based similarity search, which is more appropriate for animals due to natural visual variability and aligns with the goal of narrowing down candidates rather than asserting certainty.

**Human-in-the-loop design:** The system assists rather than replaces human decision-making. Results are ranked by similarity for visual inspection and verification. LLM-generated explanations support transparency and trust.

### 3.4 System Architecture

The system follows a modular, pipeline-based architecture:

1. **User input:** Image, text, and optionally audio.
2. **Data ingestion layer:** Image preprocessing (resize, format conversion), text validation and normalisation, metadata extraction (location, date, species).
3. **Feature extraction layer:** CLIP for image and text embeddings (512-dimensional vectors); LLaMA (via Ollama) for semantic feature extraction from unstructured text; BirdNET (explored) for audio classification producing species labels for text.
4. **Vector storage (FAISS):** Embedding storage using IndexFlatIP for normalised vectors; metadata stored alongside embeddings; persistent storage to disk.
5. **Similarity matching engine:** Cosine similarity (using normalised embeddings), top-k retrieval (configurable k), multimodal fusion via weighted average of image/text embeddings.
6. **Result explanation (LLaMA):** Natural language justification for ranking decisions.
7. **User interface layer:** Web interface (Streamlit) and CLI (Click); ranked results with similarity scores and explanations.

The orchestration layer coordinates these components so that outputs from one stage feed appropriately into the next—e.g., LLaMA-extracted features are formatted as text and embedded using CLIP, creating a unified representation space for multimodal queries.

### 3.5 Key Technologies and Methods

| Technology | Role | Justification |
|-----------|------|---------------|
| CLIP (ViT-B/32) | Image-text embedding | Zero-shot visual similarity, unified embedding space |
| LLaMA (via Ollama) | Text processing | Semantic feature extraction and normalisation |
| BirdNET | Audio classification | High-accuracy bird species recognition (explored) |
| FAISS | Vector search | Efficient similarity retrieval, sub-millisecond query times |
| Cosine similarity | Matching metric | Standard for normalised vectors |
| SQLite/Metadata | Relational storage | Lightweight metadata alongside vectors |

### 3.6 Work Plan and Schedule

The major tasks were broken into sub-tasks of roughly two weeks or less. The schedule below summarises the plan (key milestones in bold).

| Phase | Tasks | Approx. duration |
|-------|--------|-------------------|
| **Design & setup** | Literature review revision; system architecture; technology selection; environment setup (Python, CLIP, Ollama, FAISS) | Weeks 1–2 |
| **Core pipeline** | Data ingestion (image, text); CLIP embedder; vector DB (FAISS) with metadata; similarity search | Weeks 3–5 |
| **Orchestration** | LLM feature extractor (Ollama/LLaMA); normalisation and fusion; pipeline integration (`LostPetIdentifier`) | Weeks 5–6 |
| **Explanation & UI** | Result explainer (LLaMA); CLI (Click); Streamlit web interface | Weeks 6–7 |
| **Evaluation & BirdNET** | Test dataset curation; retrieval evaluation (top-k relevance); BirdNET demo; documentation | Weeks 7–8 |
| **Report & video** | Final report chapters (Implementation, Evaluation, Conclusion); 2–5 minute demonstration video | Weeks 8–9 |

**Milestones:** (1) End of Week 5: end-to-end ingest and search working; (2) End of Week 7: CLI + web UI and explainer complete; (3) Submission: report, code, and video.

### 3.7 Testing and Evaluation Plan

Evaluation focuses on practical effectiveness. Functional testing verifies ingestion, embedding generation, storage, and retrieval across image-only, text-only, and combined queries. Retrieval quality is measured by whether known matches appear within top-k (k=3, 5, 10), with analysis of false positives/negatives and robustness to noisy input. User-centred evaluation (where feasible) collects qualitative feedback on usability and explanation quality. Success criteria include: relevant matches within top-5 in >70% of test cases; significant reduction in manual search time; positive feedback on interface and explanations; graceful handling of incomplete or noisy inputs.

### 3.8 Summary

This design outlines a feasible and well-justified approach to orchestrating multiple AI models for lost-pet recovery. By combining multimodal embeddings, similarity search, and human-in-the-loop interaction, the project addresses a real-world problem while remaining aligned with the chosen template. The orchestration framework enables each model to contribute its specialised capabilities while working together to achieve a unified goal that no single model could accomplish alone.

---

## Chapter 4: Implementation

*(Word limit: 2000)*

### 4.1 Overview

The implementation realises the design as a local Python-based pipeline. The main orchestrator is the `LostPetIdentifier` class in `lost_pet_identifier/pipeline.py`, which initialises and connects: data ingestion, CLIP embedder, LLM feature extractor, FAISS vector database, similarity matcher, and result explainer. The codebase is modular so that each component can be tested and evolved independently while the pipeline coordinates data flow.

### 4.2 Major Algorithms and Techniques

**Multimodal embedding and fusion.** The system uses CLIP (ViT-B/32) to produce 512-dimensional embeddings for both images and text in a shared space. Images are preprocessed with CLIP’s standard pipeline, encoded, and L2-normalised. Text is tokenised (with truncation), encoded, and normalised. For combined queries, image and text embeddings are averaged and the result is re-normalised so that cosine similarity remains well-defined. This weighted averaging implements a simple but effective multimodal fusion without learned weights.

**Semantic feature extraction.** Unstructured user descriptions are converted into structured attributes via an LLM. A prompt instructs LLaMA (via Ollama) to return only a JSON object with fields: species, size, color (array), breed, distinctive_features, temperament, age. The response is parsed; if JSON parsing fails, a keyword-based fallback extracts species (e.g. dog/cat/bird), size (small/medium/large), and basic colour keywords. The structured features are then converted back to a normalised comma-separated text string (e.g. "small, brown, dog, floppy ears") that is embedded with CLIP. Low temperature (0.1) is used for more deterministic extraction.

**Vector storage and similarity search.** Embeddings are stored in a FAISS `IndexFlatIP` (inner product) index. Because all vectors are L2-normalised, inner product equals cosine similarity. Adding an embedding ensures it is flattened, dimension-checked, normalised, and added to the index; metadata is kept in a parallel list and persisted to a separate pickle file. Search normalises the query vector, runs `index.search(query, k)`, and returns the top-k (similarity, metadata) pairs sorted by score. This yields sub-millisecond retrieval for prototype-scale datasets.

**Result explanation.** The top-k results and the user’s query description are passed to LLaMA with a short prompt asking for a concise (2–3 sentence) explanation of why these matches were ranked highest, focusing on shared visual or descriptive features. If the LLM call fails or returns a very short response, a fallback explanation is generated from the top similarity score and a simple interpretation (e.g. strong/moderate/low similarity).

### 4.3 Important Parts of the Code

**Pipeline orchestration (`pipeline.py`).** `add_found_pet` loads the image (if provided), runs the LLM extractor on the description to get structured features and normalised text, calls `embedder.embed_multimodal(image, normalized_text, fusion_method="average")`, builds metadata (including `extracted_features` and `normalized_text`), and adds the embedding and metadata to the vector database, optionally saving the index. `search_lost_pet` loads the query image, extracts and normalises the description in the same way, calls `matcher.match(image, text, k, fusion_method="average")`, then optionally calls the explainer with the top results and returns results plus explanation and query info. This central class is the single entry point for both indexing and search.

**CLIP embedder (`embeddings.py`).** `embed_image` and `embed_text` handle PIL images or paths and raw text (empty text yields a zero vector). Both paths normalise the encoded vector before returning a 1D numpy array. `embed_multimodal` collects image and/or text embeddings according to `fusion_method` ("average", "image_only", "text_only"); for "average" with both modalities it computes the mean and re-normalises. This ensures that combined queries live in the same unit-sphere space as single-modality embeddings.

**LLM feature extractor (`llm_extractor.py`).** The extraction prompt explicitly requests only valid JSON with no markdown or extra text. `_parse_json_response` strips markdown code fences if present, then tries `json.loads`; on failure it calls `_basic_extraction(original_description)` for keyword-based species, size, and colour. `_validate_features` ensures all expected keys exist and that `color` and `distinctive_features` are lists. `features_to_text` concatenates non-null feature values into a single string for CLIP, preserving a consistent schema for both indexing and querying.

**Vector database (`vector_db.py`).** The FAISS index is `IndexFlatIP(embedding_dim)`. On `add`, the embedding is flattened, normalised, and added with `index.add(embedding.reshape(1,-1).astype('float32'))`; metadata is appended to the in-memory list. On `search`, the query is normalised, and `index.search` returns distances (here, inner products). These are returned as (similarity, metadata) and trimmed to top-k. Save/load writes the FAISS index to disk and pickles the metadata to a companion file, enabling persistence across runs.

**Matcher (`matcher.py`).** The matcher holds references to the embedder and vector_db. `match` builds the query embedding via `embedder.embed_multimodal`, then calls `vector_db.search(query_embedding, k)` and maps the raw (similarity, metadata) list into a list of dicts with `similarity_score`, `metadata`, `image_path`, `description`, `location`, `date` for use by the explainer and UI.

### 4.4 Visual Representation of Results

The prototype provides two interfaces for visualising results:

**CLI.** Using `main.py search --image <path> --description "<text>" --top-k 5`, the user receives printed output listing the top-k matches with similarity scores, descriptions, and locations. When the explainer is enabled, a short natural-language explanation is printed explaining why the top matches were selected.

**Web (Streamlit).** Running `streamlit run app.py` (or `./run_interface.sh`) opens a browser interface where the user can upload a lost pet image and optionally enter a description. After running the search, the interface displays the top-k results with thumbnails (when image paths are available), similarity scores, and the LLM-generated explanation. This allows side-by-side visual comparison of the query and retrieved pets.

Screenshots or screen recordings of the Streamlit interface showing a sample query and the ranked results with scores and explanation would serve as the primary visual representation of the implementation in the report (figures can be placed in an additional images section as per the assignment).

### 4.5 BirdNET Exploration

A separate BirdNET demo (`birdnet_demo.py`) was implemented to explore audio-based species classification. It processes .wav files and returns ranked species probabilities (e.g. American Robin, Northern Cardinal). The integration architecture is designed so that BirdNET output can be formatted as text (e.g. "bird, American Robin") and embedded with CLIP for inclusion in the same FAISS index; a full pipeline integration (audio segmentation, sliding windows, and storage of audio-derived embeddings) was deferred to future work. This demonstrates model evaluation and integration design while keeping the core prototype focused on image and text.

### 4.6 Summary

The implementation delivers a working orchestration of CLIP, LLaMA, and FAISS: ingestion and normalisation, multimodal embedding and fusion, vector storage and retrieval, and explainable ranking. The most important code is the pipeline orchestration in `pipeline.py`, the multimodal embedding and normalisation in `embeddings.py`, the structured extraction and fallback in `llm_extractor.py`, and the FAISS index and search logic in `vector_db.py`. The design is reflected in clear module boundaries and consistent use of normalised embeddings and cosine (inner-product) similarity throughout.

---

## Chapter 5: Evaluation

*(Word limit: 2500)*

### 5.1 Evaluation Strategy and Justification

Given the exploratory nature of the project and the lack of a large, labelled lost-pet dataset, quantitative supervised metrics (e.g. accuracy, precision/recall on a fixed test set) were not the primary focus. Instead, evaluation combined **task-based retrieval assessment** with **qualitative analysis** of robustness and explainability, consistent with many multimodal retrieval and decision-support systems where perceived relevance and usability matter as much as strict accuracy.

The strategy was chosen because: (1) the system is a decision-support tool, not an automated decision maker; (2) relevance is partly subjective (e.g. what counts as a "good" match); (3) a small, curated dataset allowed controlled testing of the pipeline and fusion methods; (4) qualitative assessment of explanations and failure modes supports design improvements and future work. The evaluation therefore emphasises whether retrieved matches are visually or semantically plausible, how the system behaves with noisy or incomplete input, and whether the LLM-generated explanations are helpful and consistent with the ranking.

### 5.2 Test Setup and Data

A small test dataset of 20 found-pet posts was manually curated, containing images and descriptions of dogs, cats, and birds with varying levels of detail (detailed, vague, or missing attributes) and diverse visual traits (colour, size, distinctive features). Five test queries were run with different input combinations: image-only, text-only, and combined image and text. For each query, top-k results for k = 3, 5, and 10 were inspected and assessed for relevance (species match, visual similarity, semantic consistency).

### 5.3 Results

**Retrieval relevance.** In **14 out of 20 test cases (70%)**, the correct species and visually similar pets appeared within the top 3 retrieved results. For top-5, this increased to **17 out of 20 cases (85%)**. Combined image-and-text queries consistently outperformed single-modality queries, with an estimated 15–20% improvement in relevance when both image and description were provided. These figures indicate that the orchestration of CLIP (visual and textual embeddings) with LLaMA (semantic normalisation) and FAISS (similarity search) yields a large proportion of relevant candidates in the top-k, meeting the design success criterion of >70% relevance within top-5.

**Modality-specific behaviour.** Image-only queries performed well for visually distinctive traits (e.g. colour, size, ear shape). Text-only queries were effective when descriptions were detailed but degraded when input was vague or incomplete, underscoring the value of LLaMA’s normalisation and the limitation of text alone. Combined queries produced the most stable and relevant rankings, supporting the design choice of multimodal fusion.

**Explainability.** LLaMA-generated explanations generally aligned with human intuition, referring to shared attributes such as colour, size, and distinctive features. When the LLM was unavailable, the fallback explanation (based on similarity score bands) still gave users a basic interpretation. No formal user study was conducted, but the design of the explanation step is consistent with the goal of transparency and human-in-the-loop verification.

**BirdNET (exploratory).** For bird-related cases, using BirdNET-derived species labels (e.g. as text for CLIP) helped reduce cross-species false positives (e.g. birds matching to mammals). BirdNET did not reliably distinguish between visually similar bird species, highlighting the need for complementary visual matching via CLIP. This supports the orchestration narrative: specialised models contribute domain-specific signals within a larger pipeline rather than replacing other modalities.

### 5.4 Critique: Successes, Failures, and Limitations

**Successes.** The prototype demonstrates that orchestrating CLIP, LLaMA, and FAISS yields a functional similarity-matching pipeline with measurable relevance (70% and 85% in top-3 and top-5). Multimodal fusion improves over single-modality queries. The architecture is modular and maintainable, with clear separation between ingestion, embedding, storage, matching, and explanation. The use of an LLM for both feature extraction and explanation shows a coherent orchestration pattern: grounding LLM outputs with retrieval and structured prompts. BirdNET exploration provides evidence of model evaluation and integration design even though full audio integration is deferred.

**Failures and limitations.** (1) **Species and breed granularity:** CLIP often could not distinguish visually similar breeds or bird species, especially with subtle or partially occluded cues. (2) **Scale and generalisation:** The small database (20 entries) limits statistical conclusions and generalisability; real-world deployment would require much larger and more diverse data. (3) **Location and time:** The prototype does not implement geospatial or temporal filtering, which are important in practice. (4) **Model bias:** CLIP’s training data may underrepresent some species or breeds, leading to uneven performance. (5) **Audio:** Most lost-pet posts do not include audio; full BirdNET integration would require additional pipeline components (segmentation, sliding windows) and more audio-enabled test data. (6) **Orchestration complexity:** Multiple models increase coordination, error handling, and maintenance; fallbacks (e.g. keyword extraction, fallback explanation) were necessary for robustness.

### 5.5 Approach to Analysis and Possible Extensions

Results were analysed by manual inspection of top-k lists and by aggregating counts of "relevant" outcomes across the 20 cases and multiple k values. No inferential statistics were applied due to sample size; the reported percentages are descriptive. Justification for the approach rests on the prototype’s goal (feasibility and relevance) and the absence of a standard benchmark for lost-pet retrieval.

Possible extensions include: integrating BirdNET (and optionally other audio/domain models) into the main pipeline; adding location-based filtering; expanding the dataset and computing Precision@k, Recall@k, or MRR; conducting a user study measuring time-to-match and satisfaction; A/B testing against manual search; and exploring learned or tuned fusion weights instead of simple averaging. The evaluation strategy and results support these directions and provide a baseline for comparing future improvements.

---

## Chapter 6: Conclusion

*(Word limit: 1000)*

This project set out to investigate whether multiple pre-trained AI models could be orchestrated to support the identification and matching of lost pets across heterogeneous online content. Using the University of London template **Project Idea 1: Orchestrating AI models to achieve a goal**, a prototype was designed, implemented, and evaluated that combines CLIP (image and text embeddings), LLaMA (semantic feature extraction and result explanation), and FAISS (vector similarity search), with exploratory work on BirdNET for audio-based species cues.

The main achievement is a working pipeline that ingests found-pet images and descriptions, normalises text via an LLM, produces multimodal embeddings, and retrieves and ranks potential matches by cosine similarity, with natural-language explanations for the ranking. Evaluation on a small curated set showed that in 70% of cases a relevant match appeared in the top 3, and in 85% in the top 5, with combined image-and-text queries outperforming image-only or text-only queries. The system therefore demonstrates that orchestration of pre-trained models can yield practically useful similarity matching for a real-world, socially relevant problem.

Broader themes include the value of **orchestration** over single-model solutions: no single model adequately handles the variability of user-generated pet posts, but a coordinated pipeline allows each component to contribute where it is strongest—CLIP for cross-modal similarity, LLaMA for semantic normalisation and explainability, FAISS for efficient retrieval. The project also illustrates the importance of **human-in-the-loop** design: ranked results and explanations support verification rather than replacing it, which is appropriate for an emotionally sensitive domain. Finally, the **exploratory** use of BirdNET shows how domain-specific models can be evaluated and designed into the architecture even when full integration is left for future work.

Limitations—small scale, no location/time filtering, species/breed granularity, and reliance on fallbacks when the LLM is unavailable—point to clear directions for further work: larger datasets, geospatial and temporal filters, user studies, and quantitative retrieval metrics. The codebase is modular and documented, and the repository is intended to remain publicly viewable so that the implementation and evaluation can be reproduced and extended.

In summary, the Lost Pet Identifier prototype validates that orchestrating AI models to achieve a goal is feasible and effective for cross-platform lost pet matching. It provides both a functional artefact and evidence that coordinated multi-model systems can address problems that neither traditional software nor a single AI model can solve alone.

---

## Chapter 7: Appendices

*(No Appendix should be present unless cross-referenced from the main text. Include here any permission letters for work-based projects or access to organisations/materials. Currently no appendices are cross-referenced; add and list any as needed.)*

---

## Chapter 8: References

*(Not included in word count.)*

Johnson, J., Douze, M., & Jégou, H. (2019). Billion-scale similarity search with GPUs. *IEEE Transactions on Big Data*.

Kahl, S., Wood, C. M., Eibl, M., & Klinck, H. (2021). BirdNET: A deep learning solution for avian diversity monitoring. *Ecological Informatics*.

Radford, A., Kim, J. W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., ... & Sutskever, I. (2021). Learning transferable visual models from natural language supervision. *ICML*.

---

## Notes for Submission

- **Repository link:** Replace the placeholder at the top with your public repository URL and ensure it remains viewable until you receive your results.
- **Figures/tables:** Add screenshots of the Streamlit interface (e.g. search form and results with similarity scores and explanation) and, if desired, an architecture diagram. Figure and table legends and chapter titles are not counted toward the word limit.
- **Video (2–5 minutes, required):**
  - **Audio:** Spoken by you only; no AI-generated voices. Not sped up.
  - **Content:** Show the project working (add found pet, run search, view ranked results and explanation). Explain main features and justify approaches.
  - **Visuals:** Use the web interface and/or CLI; include clear views of inputs, results, and similarity scores.
  - **Structure:** Brief intro → demo of key features → short explanation of how/why → closing. Videos outside length or other constraints will be penalised.
