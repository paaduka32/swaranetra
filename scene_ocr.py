import cv2
import numpy as np
import pytesseract
import requests
import spacy
import language_tool_python
from spellchecker import SpellChecker
from transformers import Blip2ForConditionalGeneration, Blip2Processor
import torch

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Load BLIP-2 from local path
local_blip2_path = "path to your model"
processor = Blip2Processor.from_pretrained(local_blip2_path)
model = Blip2ForConditionalGeneration.from_pretrained(local_blip2_path)

# Load NLP tools
nlp = spacy.load("en_core_web_sm")
tool = language_tool_python.LanguageTool('en-US')


def describe_scene(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    inputs = processor(frame, return_tensors="pt")
    generated_ids = model.generate(
        **inputs, max_length=100, min_length=25, do_sample=True,
        repetition_penalty=2.0, temperature=0.2, top_k=0, top_p=0.9
    )
    return processor.decode(generated_ids[0], skip_special_tokens=True)

def run_ocr(frame):
    if frame is None or not hasattr(frame, 'shape'):
        raise ValueError("Invalid frame passed to OCR.")

    def preprocess_frame_for_ocr(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        return cv2.filter2D(gray, -1, kernel)

    def word_correction(text):
        spell = SpellChecker()
        return " ".join([spell.correction(word) if spell.correction(word) is not None else word for word in text.split()])

    def sentence_reconstruction(text):
        def correct_grammar(text):
            matches = tool.check(text)
            return language_tool_python.utils.correct(text, matches)

        def reconstruct_text(text):
            doc = nlp(text)
            sentences = []
            for sent in doc.sents:
                tokens = [token.text for token in sent]
                cleaned = " ".join(tokens)
                sentences.append(correct_grammar(cleaned))
            return " ".join(sentences)

        corrected = correct_grammar(text)
        return reconstruct_text(corrected)

    processed = preprocess_frame_for_ocr(frame)
    raw_ocr = pytesseract.image_to_string(processed)

    if not raw_ocr.strip():
        return "No text detected."

    corrected_words = word_correction(raw_ocr)
    final_text = sentence_reconstruction(corrected_words)
    return final_text