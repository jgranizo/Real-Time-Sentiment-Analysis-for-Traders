import json
import os
import re
import torch
from transformers import BertTokenizer, BertForSequenceClassification, AutoTokenizer, AutoModelForTokenClassification



# Text preprocessing function
def preProcess(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '[URL]', text)
    text = re.sub(r'@\w+', '[USER]', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Tokenization function for sentiment analysis
def tokenize_texts(texts, tokenizer, max_len=140):
    input_ids = []
    attention_masks = []

    for text in texts:
        encoded = tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=max_len,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        input_ids.append(encoded['input_ids'])
        attention_masks.append(encoded['attention_mask'])

    input_ids = torch.cat(input_ids, dim=0)
    attention_masks = torch.cat(attention_masks, dim=0)

    return input_ids, attention_masks

# Load models and tokenizers
base_dir = os.path.dirname(os.path.abspath(__file__))  # location of the current file
model_dir = os.path.join(base_dir,"..", "SentimentalModel")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load sentiment analysis model and tokenizer
tokenizer = BertTokenizer.from_pretrained(model_dir)
model = BertForSequenceClassification.from_pretrained(model_dir).to(device)
model.eval()




def predict(text):
        preprocessed_text = preProcess(text)

        # Tokenize and run sentiment analysis
        input_ids, attention_masks = tokenize_texts([preprocessed_text], tokenizer, max_len=140)
        input_ids, attention_masks = input_ids.to(device), attention_masks.to(device)

        label_mapping = {0: "Negative", 1: "Neutral", 2: "Positive"}
        with torch.no_grad():
            outputs = model(input_ids, attention_mask=attention_masks)
            sentiment = torch.argmax(outputs.logits, dim=1).item()
        return sentiment

