"""
Sentiment Analysis Model - Concrete implementation.

Demonstrates:
- Implementing the model interface
- Handling model loading/unloading
- Input validation
- Error handling
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import numpy as np

from .base import (
    BaseMLModel,
    ModelMetadata,
    ModelStatus,
    ModelLoadError,
    ModelInfereceError,
)

class SentimentInput:
    """input schema for sentiment model"""
    def __init__(self, text:str, language: str = "en"):
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        self.text = text.strip()
        self.language = language


class SentimentOutput:
    """output schema for sentiment model"""
    def __init__(
            self,
            label:str,
            score: float,
            probabilities: Dict[str, float],
    ):
        self.label = label
        self.score = score
        self.probabilities = probabilities
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "label": self.label,
            "score": self.score,
            "probabilities": self.probabilities,
        }
    
class SentimentModel(BaseMLModel[SentimentInput, SentimentOutput]):
    """
    Production sentiment analysis model.
    
    In production, this would use a transformer model like:
    - DistilBERT
    - RoBERTa
    - Custom fine-tuned model
    
    For demo, we use a simple mock implementation.
    """

    MODEL_NAME = "sentiment-analyzer"
    MODEL_VERSION = "1.0.0"

    def __init__(self, model_path: Optional[str] = None):
        super().__init__() 
        # what does super() do here? It calls the __init__ method of the BaseMLModel class, 
        # which initializes the model's status to LOADING, sets the load time to None, 
        # and initializes the inference count to 0. 
        # This ensures that all the necessary attributes from the base class are properly initialized 
        # when we create an instance of SentimentModel.
        self.model_path = model_path
        self._model = None
        self._tokenizer = None 
        # what does _tokenizer means here? The _tokenizer is a component used in natural language processing (NLP) 
        # models to convert raw text into a format that the model can understand.
        # It typically breaks down the input text into smaller units called tokens (e.g., words, subwords, or characters)
        # and converts them into numerical representations (like token IDs) that can be fed into the model for inference.
        # Inference is the reasoning process where the model takes the input data and produces an output (like a prediction or classification).

        def load(self) -> None:
            """load the sentiment model"""
            try:
                self._status = ModelStatus.LOADING

                # In production, load actual model:
                # from transformers import pipeline
                # self._model = pipeline("sentiment-analysis", 
                #     model="distilbert-base-uncased-finetuned-sst-2-english")

                #mock model for demo
                self._model = self._create_mock_model()

                self._status = ModelStatus.READY
                self._load_time = datetime.now(datetime.timezone.utc)

            except Exception as e:
                self._status = ModelStatus.ERROR
                raise ModelLoadError(f"Failed to load sentiment model: {e}")
            
        def predict(self, inputs: SentimentInput) -> SentimentOutput:
            """
            Predict sentiment for a single text.
            
            Args:
                inputs: SentimentInput with text
                
            Returns:
                SentimentOutput with label, score, probabilities
            """
            if self._status != ModelStatus.READY:
                raise ModelInfereceError("Model not ready for inference")
            
            try:
                result = self._model(inputs.text)
                self._increment_inference_count()

                return SentimentOutput(
                    label=result["label"],
                    score=result["score"],
                    probabilities=result["probabilities"],
                )
            except Exception as e:
                raise ModelInfereceError(f"Inference failed: {e}")
        
        def predict_batch(
                self, inputs: List[SentimentInput]
        ) -> List[SentimentOutput]:
            """
            Batch prediction for efficiency.
            
            Batching improves throughput by:
            - Reducing per-request overhead
            - Better GPU utilization
            - Amortizing tokenization cost
            """
            if self._status != ModelStatus.READY:
                raise ModelInfereceError("model not ready for inference")
            
            try:
                texts = [inp.text for inp in inputs]
                results = [self.model(text) for text in texts]
                self._increment_inference_count(len(inputs))

                return [
                    SentimentOutput(
                        label=r["label"], 
                        # what does it mean the r here? The r refers to each individual result in the results list. 
                        # in other words, for each result r in the results list, we are creating a SentimentOutput object 
                        # using the label, score, and probabilities from that result. the r comes from the list comprehension 
                        # that iterates over the results of the batch prediction,
                        score=r["score"],
                        probabilities=r["probabilities"],
                    )
                    for r in results
                ]
            except Exception as e:
                raise ModelInfereceError(f"Batch inference failed: {e}")
        
        def get_metadata(self) -> ModelMetadata:
            """return model metadata"""
            return ModelMetadata(
                name=self.MODEL_NAME,
                version=self.MODEL_VERSION,
                description="sentiment analysis model for english text",
                created_at=datetime.now(datetime.timezone.utc),
                framework="transformers",
                input_schema={
                    "type":"object",
                    "properties":{
                        "text": {"type":"string", "maxLength": 512},
                        "language": {"type": "string", "default": "en"},
                    },
                    "required": ["text"],
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "label": {"type": "string", "enum": ["POSITIVE", "NEGATIVE", "NEAUTRAL"]},
                        "score": {"type": "number", "minimum":0, "maximum": 1},
                        "probabilities": {"type":"object"},
                    },                    
                },
                tags=["nlp", "sentiment", "production"],
                metrics={"accuaracy": 0.92, "latency_p50ms": 15, "latency_p99_ms":45},
            )


        