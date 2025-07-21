# Computer-Science-Final-Year-Project

Supermarket Path Optimizer

This application helps users find the most efficient path to collect items in a supermarket. Users can input shopping lists via text, image, or voice, and receive an optimized route visualized on a graph.

Features

Input via text, image (shopping list), or voice
Intelligent item recognition with spell correction
Item-to-location mapping
Shortest path calculation across supermarket layout
Interactive path visualization

Technologies Used

User Input:
Users can enter their shopping list via text, upload an image, or use voice input.
Technology: Flask
Purpose: Captures and routes user input through the processing pipeline.

OCR Extraction:
Text is extracted from images of handwritten or printed shopping lists.
Technology: PaddleOCR
Purpose: Converts shopping list images into text for further processing.

Voice Transcription:
Converts spoken shopping lists into written text.
Technology: SpeechRecognition / Google Speech API
Purpose: Enables hands-free interaction via voice commands.

Keyword Extraction:
Identifies relevant item names from the input text.
Technology: KeyBERT
Purpose: Filters out noise and extracts meaningful shopping items.

Spell Correction:
Corrects misspelled item names to improve matching accuracy.
Technology: SymSpell
Purpose: Ensures item names are correctly interpreted even with typos.

Fuzzy Matching:
Matches extracted item names to the known list of items in the supermarket.
Technology: FuzzyWuzzy
Purpose: Handles minor discrepancies in item naming for reliable identification.

Location Mapping:
Associates each item with its specific location in the supermarket layout.
Technology: Python Dictionary
Purpose: Maps items to aisles or sections for navigation.

Shortest Path Calculation:
Computes the most efficient route to collect all items.
Technology: NetworkX (Dijkstra, permutations)
Purpose: Optimizes the path to minimize walking distance/time.

Graph Visualization:
Displays the store layout and the shortest path to the user.
Technology: Plotly
Purpose: Provides an interactive visual guide through the supermarket.

Web Interface:
Renders the application interface and results in the browser.
Technology: Flask + HTML/CSS
Purpose: Enables user interaction with the system and visual outputs.

How It Works

1.User Input: Enter items manually, upload a shopping list image, or use voice input.
2.Text Extraction: OCR or speech-to-text processes extract raw item names.
3.Item Prediction: Keywords are extracted, corrected, and matched to known items.
4.Location Check: Items are mapped to their supermarket locations.
5.Shortest Path: NetworkX calculates the optimal route between item locations.
6.Visualization: An interactive graph shows the path to follow.
