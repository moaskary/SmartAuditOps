# huggingface_tasks/classify_text.py

from transformers import pipeline
import logging

# Configure basic logging to see informational messages in the container logs
logging.basicConfig(level=logging.INFO)

# Initialize the classifier variable to None.
# The actual model will be loaded into this variable on the first API call.
classifier = None

def analyze_code_snippet(snippet: str):
    """
    Analyzes a code snippet using zero-shot classification to detect potential issues.
    This function uses "lazy loading" to initialize the model on the first request.
    """
    # Use the 'global' keyword to modify the 'classifier' variable defined outside this function.
    global classifier

    # The lazy loading block: If the model hasn't been loaded yet, load it.
    if classifier is None:
        logging.info("Initializing Zero-Shot-Classification model for the first time...")
        try:
            # This is the line that takes a long time and downloads the model
            classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli"
            )
            logging.info("Model initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to load Hugging Face model: {e}")
            # Return a specific error message if the model fails to load
            return {"error": "Model could not be loaded. Check container logs for details."}

    # These are our new, more descriptive labels to help the model differentiate.
    candidate_labels = [
        "This code appears to be safe and follows best practices.",
        "This code contains a potential security vulnerability like SQL injection or insecure deserialization.",
        "This code contains a hardcoded secret like a password or an API key.",
        "This code contains sensitive Personally Identifiable Information (PII) like names, emails, or credit card numbers.",
        "This code may have performance issues or unoptimized logic."
    ]

    # Run the classification
    try:
        result = classifier(snippet, candidate_labels, multi_label=False) # multi_label=False can sometimes improve single-choice accuracy
        
        # The API response will contain the full descriptive labels, which is more readable.
        # We zip the labels and scores together into a dictionary.
        analysis_data = dict(zip(result['labels'], result['scores']))
        
        return {"analysis": analysis_data}

    except Exception as e:
        logging.error(f"Error during model inference: {e}")
        return {"error": "Failed to analyze snippet during model inference."}