import gradio as gr
from transformers import pipeline
import re

# Load grammar correction model
grammar_corrector = pipeline("text2text-generation", model="prithivida/grammar_error_correcter_v1")

# Whitelist for names / proper nouns
whitelist = ["Mona", "Priya", "Mohana", "AI", "HF", "Gradio"]

# Preprocessing casual greetings
def preprocess_text(text):
    text = re.sub(r"\bh+ii+\b", "Hi", text, flags=re.IGNORECASE)
    return text

# Postprocess to restore proper nouns
def restore_whitelist(text):
    words = text.split()
    for i, w in enumerate(words):
        for name in whitelist:
            if w.lower() == name.lower():
                words[i] = name
    return " ".join(words)

def correct_text(input_text, tone):
    if not input_text.strip():
        return "Please enter some text.", "", ""
    
    # Preprocess
    preprocessed = preprocess_text(input_text)
    
    # Grammar correction
    corrected = grammar_corrector(preprocessed)
    corrected_text = corrected[0]['generated_text']
    
    # Restore proper nouns
    corrected_text = restore_whitelist(corrected_text)
    
    # Add emoji feedback
    emoji = ""
    if tone == "Professional":
        emoji = "💼"
    elif tone == "Student":
        emoji = "📚"
    elif tone == "Friendly / Casual":
        emoji = "😄"
    elif tone == "Academic / Formal":
        emoji = "🎓"
    
    return input_text, corrected_text, emoji

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# ✨ GrammarPolishAI – Grammarly-Style Demo 💬")
    
    with gr.Row():
        user_input = gr.Textbox(label="Enter Your Text", placeholder="Paste your paragraph here...", lines=7)
        tone_select = gr.Dropdown(
            label="Select Tone",
            choices=["Student", "Professional", "Friendly / Casual", "Academic / Formal"],
            value="Professional"
        )
    
    generate_btn = gr.Button("Polish Text")
    
    with gr.Row():
        original_box = gr.Textbox(label="Original Text", lines=7)
        corrected_box = gr.Textbox(label="Corrected Text", lines=7)
        emoji_box = gr.Textbox(label="Tone Emoji", lines=1)
    
    generate_btn.click(fn=correct_text, inputs=[user_input, tone_select], outputs=[original_box, corrected_box, emoji_box])

demo.launch()
