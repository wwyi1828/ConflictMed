
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModel

class SentenceEncoder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.device = self.model.device
        print(f"Device: {self.device}")
        
    def encode(self, texts, batch_size=8):
        if isinstance(texts, str):
            texts = [texts]
        
        all_embeddings = self.model.encode(texts, batch_size=batch_size, 
                                          show_progress_bar=True, 
                                          convert_to_numpy=True)
        
        return np.array(all_embeddings)

class RobertaEncoder:
    def __init__(self, model_name='allenai/biomed_roberta_base'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        print(f"Device: {self.device}")
        print(f"Using model: {model_name}")
        
    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        
    def encode(self, texts, batch_size=8):
        if isinstance(texts, str):
            texts = [texts]
        
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            
            encoded_input = self.tokenizer(batch_texts, padding=True, truncation=True, 
                                          max_length=512, return_tensors='pt')
            encoded_input = {k: v.to(self.device) for k, v in encoded_input.items()}
            
            with torch.no_grad():
                model_output = self.model(**encoded_input)
                
            batch_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask']).cpu().numpy()
            all_embeddings.extend(batch_embeddings)
        
        return np.array(all_embeddings) 