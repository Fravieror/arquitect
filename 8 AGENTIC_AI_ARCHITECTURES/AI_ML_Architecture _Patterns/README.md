# Model-as-a-Service (MaaS) Architecture

A critical architectural pattern for deploying, managing, and consuming machine learning models in production. Essential knowledge for any AI/ML architect.

---

## Core Concepts

### What is Model-as-a-Service?

Model-as-a-Service (MaaS) is an architectural pattern that:
- **Decouples** ML models from consuming applications
- **Exposes** models via APIs (REST, gRPC, WebSocket)
- **Enables** independent scaling, versioning, and deployment
- **Abstracts** model complexity from client applications

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENTS                                        │
│    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐            │
│    │ Web App  │    │ Mobile   │    │ Backend  │    │   IoT    │            │
│    └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘            │
└─────────┼───────────────┼───────────────┼───────────────┼──────────────────┘
          │               │               │               │
          ▼               ▼               ▼               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           API GATEWAY                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Auth/AuthZ  │  │ Rate Limit  │  │  Routing    │  │  Caching    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          ▼                      ▼                      ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│  Model Service  │   │  Model Service  │   │  Model Service  │
│    (Sentiment)  │   │    (Image)      │   │    (LLM)        │
│   ┌───────────┐ │   │   ┌───────────┐ │   │   ┌───────────┐ │
│   │  Model    │ │   │   │  Model    │ │   │   │  Model    │ │
│   │  v1.2.0   │ │   │   │  v2.0.1   │ │   │   │  v3.0.0   │ │
│   └───────────┘ │   │   └───────────┘ │   │   └───────────┘ │
└────────┬────────┘   └────────┬────────┘   └────────┬────────┘
         │                     │                     │
         ▼                     ▼                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        INFRASTRUCTURE                                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ Model    │  │ Feature  │  │ Metrics  │  │ Logging  │  │ Object   │      │
│  │ Registry │  │ Store    │  │ Store    │  │          │  │ Storage  │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Components

| Component | Responsibility |
|-----------|---------------|
| **Model Service** | Wraps model, handles inference requests |
| **API Gateway** | Authentication, rate limiting, routing |
| **Model Registry** | Version control, model metadata, lineage |
| **Feature Store** | Consistent feature serving for training & inference |
| **Monitoring** | Performance metrics, drift detection, alerting |

### MaaS vs Traditional Deployment

| Aspect | Traditional | Model-as-a-Service |
|--------|-------------|-------------------|
| Coupling | Model embedded in app | Model decoupled, API-based |
| Scaling | Scale entire app | Scale model independently |
| Updates | Redeploy app | Update model only |
| Versioning | Code versioning | Model versioning + A/B testing |
| Reusability | Per-application | Shared across organization |

---

## Python Implementation Patterns

### Project Structure

```
maas_python/
├── requirements.txt
├── config/
│   └── settings.py
├── models/
│   ├── __init__.py
│   ├── base.py              # Abstract model interface
│   ├── sentiment_model.py   # Sentiment analysis model
│   └── embedding_model.py   # Text embedding model
├── services/
│   ├── __init__.py
│   ├── model_service.py     # Model serving logic
│   ├── registry.py          # Model registry
│   └── monitoring.py        # Metrics and monitoring
├── api/
│   ├── __init__.py
│   ├── routes.py            # API endpoints
│   ├── schemas.py           # Request/Response models
│   └── middleware.py        # Auth, rate limiting
├── tests/
│   └── test_models.py
└── main.py
```

### Commands to Run

```powershell
# Create project directory
mkdir maas_python
cd maas_python

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1
# on windows: source venv/Scripts/activate

# Install dependencies
pip install fastapi uvicorn pydantic numpy scikit-learn transformers torch httpx prometheus-client python-dotenv

# Create requirements.txt
pip freeze > requirements.txt
```

---

## Code to Type

### 1. Configuration - `config/settings.py`

```python
"""
Configuration management for Model-as-a-Service.

As an architect, externalize ALL configuration:
- Model paths, versions
- API settings
- Feature flags
- Environment-specific settings
"""
from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment."""
    
    # API Configuration
    api_title: str = "Model-as-a-Service API"
    api_version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    
    # Model Configuration
    model_cache_dir: str = "./model_cache"
    default_model_version: str = "latest"
    model_timeout_seconds: int = 30
    
    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60
    
    # Monitoring
    enable_metrics: bool = True
    metrics_port: int = 9090
    
    # Feature Flags
    enable_model_caching: bool = True
    enable_batch_inference: bool = True
    max_batch_size: int = 32
    
    # Security
    api_key_header: str = "X-API-Key"
    require_api_key: bool = False
    
    class Config:
        env_file = ".env"
        env_prefix = "MAAS_"


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()
```

### 2. Base Model Interface - `models/base.py`

```python
"""
Abstract Model Interface - The contract all models must follow.

Key Architectural Principle:
- Program to an interface, not implementation
- All models share the same contract
- Enables hot-swapping, A/B testing, versioning
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar, Generic
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class ModelStatus(str, Enum):
    """Model lifecycle status."""
    LOADING = "loading"
    READY = "ready"
    ERROR = "error"
    UNLOADING = "unloading"


class ModelMetadata(BaseModel):
    """Model metadata for registry."""
    name: str
    version: str
    description: str
    created_at: datetime
    framework: str  # pytorch, tensorflow, sklearn, etc.
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    tags: List[str] = []
    metrics: Dict[str, float] = {}  # accuracy, latency, etc.


# Generic types for input/output
InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


class BaseMLModel(ABC, Generic[InputType, OutputType]):
    """
    Abstract base class for all ML models.
    
    Every model in the system must implement this interface.
    This enables:
    - Consistent API across all models
    - Easy swapping of model implementations
    - Unified monitoring and lifecycle management
    """
    
    def __init__(self):
        self._status = ModelStatus.LOADING
        self._load_time: Optional[datetime] = None
        self._inference_count: int = 0
    
    @property
    def status(self) -> ModelStatus:
        return self._status
    
    @property
    def inference_count(self) -> int:
        return self._inference_count
    
    @abstractmethod
    def load(self) -> None:
        """
        Load model into memory.
        
        Should handle:
        - Downloading from model registry if needed
        - Loading weights
        - Warming up (optional inference to compile)
        """
        pass
    
    @abstractmethod
    def unload(self) -> None:
        """
        Unload model from memory.
        
        Should handle:
        - Releasing GPU memory
        - Cleanup resources
        """
        pass
    
    @abstractmethod
    def predict(self, inputs: InputType) -> OutputType:
        """
        Single inference.
        
        Args:
            inputs: Model-specific input format
            
        Returns:
            Model-specific output format
        """
        pass
    
    @abstractmethod
    def predict_batch(self, inputs: List[InputType]) -> List[OutputType]:
        """
        Batch inference for efficiency.
        
        Args:
            inputs: List of inputs
            
        Returns:
            List of outputs in same order
        """
        pass
    
    @abstractmethod
    def get_metadata(self) -> ModelMetadata:
        """Return model metadata."""
        pass
    
    def health_check(self) -> Dict[str, Any]:
        """
        Health check for load balancers.
        
        Returns:
            Health status and diagnostics
        """
        return {
            "status": self._status.value,
            "loaded_at": self._load_time.isoformat() if self._load_time else None,
            "inference_count": self._inference_count,
            "healthy": self._status == ModelStatus.READY,
        }
    
    def _increment_inference_count(self, count: int = 1) -> None:
        """Track inference count for monitoring."""
        self._inference_count += count


class ModelLoadError(Exception):
    """Raised when model fails to load."""
    pass


class ModelInferenceError(Exception):
    """Raised when inference fails."""
    pass
```

### 3. Sentiment Model Implementation - `models/sentiment_model.py`

```python
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
    ModelInferenceError,
)


class SentimentInput:
    """Input schema for sentiment model."""
    def __init__(self, text: str, language: str = "en"):
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        self.text = text.strip()
        self.language = language


class SentimentOutput:
    """Output schema for sentiment model."""
    def __init__(
        self,
        label: str,
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
        self.model_path = model_path
        self._model = None
        self._tokenizer = None
    
    def load(self) -> None:
        """Load the sentiment model."""
        try:
            self._status = ModelStatus.LOADING
            
            # In production, load actual model:
            # from transformers import pipeline
            # self._model = pipeline("sentiment-analysis", 
            #     model="distilbert-base-uncased-finetuned-sst-2-english")
            
            # Mock model for demo
            self._model = self._create_mock_model()
            
            self._status = ModelStatus.READY
            self._load_time = datetime.utcnow()
            
        except Exception as e:
            self._status = ModelStatus.ERROR
            raise ModelLoadError(f"Failed to load sentiment model: {e}")
    
    def unload(self) -> None:
        """Unload model and free resources."""
        self._status = ModelStatus.UNLOADING
        self._model = None
        self._tokenizer = None
        self._status = ModelStatus.LOADING
    
    def predict(self, inputs: SentimentInput) -> SentimentOutput:
        """
        Predict sentiment for a single text.
        
        Args:
            inputs: SentimentInput with text
            
        Returns:
            SentimentOutput with label, score, probabilities
        """
        if self._status != ModelStatus.READY:
            raise ModelInferenceError("Model not ready for inference")
        
        try:
            result = self._model(inputs.text)
            self._increment_inference_count()
            
            return SentimentOutput(
                label=result["label"],
                score=result["score"],
                probabilities=result["probabilities"],
            )
        except Exception as e:
            raise ModelInferenceError(f"Inference failed: {e}")
    
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
            raise ModelInferenceError("Model not ready for inference")
        
        try:
            texts = [inp.text for inp in inputs]
            results = [self._model(text) for text in texts]
            self._increment_inference_count(len(inputs))
            
            return [
                SentimentOutput(
                    label=r["label"],
                    score=r["score"],
                    probabilities=r["probabilities"],
                )
                for r in results
            ]
        except Exception as e:
            raise ModelInferenceError(f"Batch inference failed: {e}")
    
    def get_metadata(self) -> ModelMetadata:
        """Return model metadata."""
        return ModelMetadata(
            name=self.MODEL_NAME,
            version=self.MODEL_VERSION,
            description="Sentiment analysis model for English text",
            created_at=datetime.utcnow(),
            framework="transformers",
            input_schema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "maxLength": 512},
                    "language": {"type": "string", "default": "en"},
                },
                "required": ["text"],
            },
            output_schema={
                "type": "object",
                "properties": {
                    "label": {"type": "string", "enum": ["POSITIVE", "NEGATIVE", "NEUTRAL"]},
                    "score": {"type": "number", "minimum": 0, "maximum": 1},
                    "probabilities": {"type": "object"},
                },
            },
            tags=["nlp", "sentiment", "production"],
            metrics={"accuracy": 0.92, "latency_p50_ms": 15, "latency_p99_ms": 45},
        )
    
    def _create_mock_model(self):
        """Create mock model for demonstration."""
        def mock_sentiment(text: str) -> Dict[str, Any]:
            # Simple keyword-based mock
            text_lower = text.lower()
            positive_words = {"good", "great", "excellent", "amazing", "love", "best", "happy"}
            negative_words = {"bad", "terrible", "awful", "hate", "worst", "sad", "angry"}
            
            pos_count = sum(1 for w in text_lower.split() if w in positive_words)
            neg_count = sum(1 for w in text_lower.split() if w in negative_words)
            
            if pos_count > neg_count:
                label, score = "POSITIVE", 0.7 + (pos_count * 0.05)
            elif neg_count > pos_count:
                label, score = "NEGATIVE", 0.7 + (neg_count * 0.05)
            else:
                label, score = "NEUTRAL", 0.6
            
            score = min(score, 0.99)
            
            # Generate probabilities
            if label == "POSITIVE":
                probs = {"POSITIVE": score, "NEGATIVE": (1-score)*0.6, "NEUTRAL": (1-score)*0.4}
            elif label == "NEGATIVE":
                probs = {"POSITIVE": (1-score)*0.4, "NEGATIVE": score, "NEUTRAL": (1-score)*0.6}
            else:
                probs = {"POSITIVE": 0.2, "NEGATIVE": 0.2, "NEUTRAL": score}
            
            return {"label": label, "score": score, "probabilities": probs}
        
        return mock_sentiment
```

### 4. Model Registry - `services/registry.py`

```python
"""
Model Registry - Version control and management for models.

Key responsibilities:
- Track all model versions
- Enable model discovery
- Support A/B testing and canary deployments
- Maintain model lineage
"""
from typing import Dict, List, Optional, Type
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import threading

from models.base import BaseMLModel, ModelMetadata, ModelStatus


class DeploymentStage(str, Enum):
    """Model deployment stages."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    ARCHIVED = "archived"


@dataclass
class RegisteredModel:
    """A model registered in the registry."""
    name: str
    version: str
    model_class: Type[BaseMLModel]
    stage: DeploymentStage
    registered_at: datetime
    metadata: Optional[ModelMetadata] = None
    model_instance: Optional[BaseMLModel] = None
    tags: Dict[str, str] = field(default_factory=dict)
    
    @property
    def model_key(self) -> str:
        """Unique identifier for this model version."""
        return f"{self.name}:{self.version}"


class ModelRegistry:
    """
    Central registry for all models.
    
    In production, this would be backed by:
    - MLflow Model Registry
    - AWS SageMaker Model Registry
    - Azure ML Model Registry
    - Weights & Biases
    - Custom database
    
    This implementation is in-memory for demonstration.
    """
    
    def __init__(self):
        self._models: Dict[str, Dict[str, RegisteredModel]] = {}
        self._lock = threading.RLock()
        self._latest_versions: Dict[str, str] = {}
    
    def register(
        self,
        name: str,
        version: str,
        model_class: Type[BaseMLModel],
        stage: DeploymentStage = DeploymentStage.DEVELOPMENT,
        tags: Optional[Dict[str, str]] = None,
    ) -> RegisteredModel:
        """
        Register a new model version.
        
        Args:
            name: Model name (e.g., "sentiment-analyzer")
            version: Semantic version (e.g., "1.0.0")
            model_class: The model class to instantiate
            stage: Deployment stage
            tags: Optional metadata tags
            
        Returns:
            RegisteredModel instance
        """
        with self._lock:
            if name not in self._models:
                self._models[name] = {}
            
            registered = RegisteredModel(
                name=name,
                version=version,
                model_class=model_class,
                stage=stage,
                registered_at=datetime.utcnow(),
                tags=tags or {},
            )
            
            self._models[name][version] = registered
            self._latest_versions[name] = version
            
            return registered
    
    def get(
        self,
        name: str,
        version: Optional[str] = None,
    ) -> Optional[RegisteredModel]:
        """
        Get a registered model.
        
        Args:
            name: Model name
            version: Specific version or None for latest
            
        Returns:
            RegisteredModel or None if not found
        """
        with self._lock:
            if name not in self._models:
                return None
            
            if version is None:
                version = self._latest_versions.get(name)
            
            if version is None:
                return None
            
            return self._models[name].get(version)
    
    def get_loaded_instance(
        self,
        name: str,
        version: Optional[str] = None,
    ) -> Optional[BaseMLModel]:
        """
        Get a loaded model instance, loading if necessary.
        
        This is the primary method for model serving.
        """
        registered = self.get(name, version)
        if registered is None:
            return None
        
        with self._lock:
            # Load if not already loaded
            if registered.model_instance is None:
                instance = registered.model_class()
                instance.load()
                registered.model_instance = instance
                registered.metadata = instance.get_metadata()
            
            return registered.model_instance
    
    def list_models(self) -> List[str]:
        """List all registered model names."""
        with self._lock:
            return list(self._models.keys())
    
    def list_versions(self, name: str) -> List[str]:
        """List all versions of a model."""
        with self._lock:
            if name not in self._models:
                return []
            return list(self._models[name].keys())
    
    def get_production_model(self, name: str) -> Optional[RegisteredModel]:
        """Get the production version of a model."""
        with self._lock:
            if name not in self._models:
                return None
            
            for version, model in self._models[name].items():
                if model.stage == DeploymentStage.PRODUCTION:
                    return model
            
            return None
    
    def promote_to_production(self, name: str, version: str) -> bool:
        """
        Promote a model version to production.
        
        Demotes current production version to staging.
        """
        with self._lock:
            # Demote current production
            current_prod = self.get_production_model(name)
            if current_prod:
                current_prod.stage = DeploymentStage.STAGING
            
            # Promote new version
            model = self.get(name, version)
            if model:
                model.stage = DeploymentStage.PRODUCTION
                return True
            
            return False
    
    def unload_model(self, name: str, version: str) -> bool:
        """Unload a model from memory."""
        with self._lock:
            model = self.get(name, version)
            if model and model.model_instance:
                model.model_instance.unload()
                model.model_instance = None
                return True
            return False


# Global registry singleton
_registry: Optional[ModelRegistry] = None


def get_registry() -> ModelRegistry:
    """Get the global model registry."""
    global _registry
    if _registry is None:
        _registry = ModelRegistry()
    return _registry
```

### 5. Model Service - `services/model_service.py`

```python
"""
Model Service - Orchestrates model inference.

This is the application layer that:
- Handles request validation
- Manages model lifecycle
- Implements inference patterns (sync, async, batch)
- Collects metrics
"""
from typing import Any, Dict, List, Optional
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging

from models.base import BaseMLModel, ModelInferenceError
from services.registry import get_registry, ModelRegistry
from services.monitoring import MetricsCollector, get_metrics_collector
from config.settings import get_settings


logger = logging.getLogger(__name__)


class ModelServiceError(Exception):
    """Base exception for model service."""
    pass


class ModelNotFoundError(ModelServiceError):
    """Model not found in registry."""
    pass


class InferenceTimeoutError(ModelServiceError):
    """Inference exceeded timeout."""
    pass


class ModelService:
    """
    Service layer for model inference.
    
    Provides:
    - Sync and async inference
    - Batch processing
    - Model versioning support
    - Metrics collection
    - Error handling
    """
    
    def __init__(
        self,
        registry: Optional[ModelRegistry] = None,
        metrics: Optional[MetricsCollector] = None,
    ):
        self.registry = registry or get_registry()
        self.metrics = metrics or get_metrics_collector()
        self.settings = get_settings()
        self._executor = ThreadPoolExecutor(max_workers=4)
    
    def predict(
        self,
        model_name: str,
        inputs: Any,
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Synchronous prediction.
        
        Args:
            model_name: Name of the model
            inputs: Model-specific input
            version: Optional specific version
            
        Returns:
            Prediction result with metadata
        """
        start_time = datetime.utcnow()
        
        try:
            # Get model instance
            model = self.registry.get_loaded_instance(model_name, version)
            if model is None:
                raise ModelNotFoundError(f"Model '{model_name}' not found")
            
            # Run inference
            result = model.predict(inputs)
            
            # Record metrics
            latency = (datetime.utcnow() - start_time).total_seconds() * 1000
            self.metrics.record_inference(model_name, latency, success=True)
            
            return {
                "model": model_name,
                "version": version or "latest",
                "result": result.to_dict() if hasattr(result, "to_dict") else result,
                "latency_ms": latency,
                "timestamp": datetime.utcnow().isoformat(),
            }
            
        except ModelNotFoundError:
            self.metrics.record_inference(model_name, 0, success=False)
            raise
        except ModelInferenceError as e:
            latency = (datetime.utcnow() - start_time).total_seconds() * 1000
            self.metrics.record_inference(model_name, latency, success=False)
            raise ModelServiceError(f"Inference failed: {e}")
    
    async def predict_async(
        self,
        model_name: str,
        inputs: Any,
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Asynchronous prediction.
        
        Non-blocking for better concurrency in async frameworks.
        """
        loop = asyncio.get_event_loop()
        
        try:
            result = await asyncio.wait_for(
                loop.run_in_executor(
                    self._executor,
                    lambda: self.predict(model_name, inputs, version),
                ),
                timeout=self.settings.model_timeout_seconds,
            )
            return result
        except asyncio.TimeoutError:
            self.metrics.record_inference(model_name, 0, success=False)
            raise InferenceTimeoutError(
                f"Inference timeout after {self.settings.model_timeout_seconds}s"
            )
    
    def predict_batch(
        self,
        model_name: str,
        inputs_list: List[Any],
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Batch prediction for efficiency.
        
        Benefits:
        - Better GPU utilization
        - Reduced per-request overhead
        - Higher throughput
        """
        start_time = datetime.utcnow()
        batch_size = len(inputs_list)
        
        # Enforce max batch size
        if batch_size > self.settings.max_batch_size:
            raise ModelServiceError(
                f"Batch size {batch_size} exceeds max {self.settings.max_batch_size}"
            )
        
        try:
            model = self.registry.get_loaded_instance(model_name, version)
            if model is None:
                raise ModelNotFoundError(f"Model '{model_name}' not found")
            
            results = model.predict_batch(inputs_list)
            
            latency = (datetime.utcnow() - start_time).total_seconds() * 1000
            self.metrics.record_batch_inference(model_name, batch_size, latency, success=True)
            
            return {
                "model": model_name,
                "version": version or "latest",
                "batch_size": batch_size,
                "results": [r.to_dict() if hasattr(r, "to_dict") else r for r in results],
                "latency_ms": latency,
                "avg_latency_ms": latency / batch_size,
                "timestamp": datetime.utcnow().isoformat(),
            }
            
        except ModelNotFoundError:
            raise
        except Exception as e:
            latency = (datetime.utcnow() - start_time).total_seconds() * 1000
            self.metrics.record_batch_inference(model_name, batch_size, latency, success=False)
            raise ModelServiceError(f"Batch inference failed: {e}")
    
    def list_available_models(self) -> List[Dict[str, Any]]:
        """List all available models with their status."""
        models = []
        for name in self.registry.list_models():
            versions = self.registry.list_versions(name)
            for version in versions:
                registered = self.registry.get(name, version)
                if registered:
                    models.append({
                        "name": name,
                        "version": version,
                        "stage": registered.stage.value,
                        "loaded": registered.model_instance is not None,
                        "registered_at": registered.registered_at.isoformat(),
                        "tags": registered.tags,
                    })
        return models
    
    def get_model_info(
        self,
        model_name: str,
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get detailed model information."""
        registered = self.registry.get(model_name, version)
        if registered is None:
            raise ModelNotFoundError(f"Model '{model_name}' not found")
        
        info = {
            "name": registered.name,
            "version": registered.version,
            "stage": registered.stage.value,
            "registered_at": registered.registered_at.isoformat(),
            "loaded": registered.model_instance is not None,
            "tags": registered.tags,
        }
        
        if registered.metadata:
            info["metadata"] = registered.metadata.model_dump()
        
        if registered.model_instance:
            info["health"] = registered.model_instance.health_check()
        
        return info


# Service singleton
_model_service: Optional[ModelService] = None


def get_model_service() -> ModelService:
    """Get the global model service."""
    global _model_service
    if _model_service is None:
        _model_service = ModelService()
    return _model_service
```

### 6. Monitoring - `services/monitoring.py`

```python
"""
Monitoring and Metrics for Model-as-a-Service.

Critical for production:
- Track inference latency
- Monitor error rates
- Detect model drift
- Capacity planning
"""
from typing import Dict, Optional
from datetime import datetime
from dataclasses import dataclass, field
import threading
from collections import defaultdict
import statistics


@dataclass
class ModelMetrics:
    """Metrics for a single model."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    latencies_ms: list = field(default_factory=list)
    last_request_at: Optional[datetime] = None
    
    @property
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.successful_requests / self.total_requests
    
    @property
    def error_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.failed_requests / self.total_requests
    
    @property
    def latency_p50(self) -> float:
        if not self.latencies_ms:
            return 0.0
        return statistics.median(self.latencies_ms)
    
    @property
    def latency_p95(self) -> float:
        if not self.latencies_ms:
            return 0.0
        sorted_latencies = sorted(self.latencies_ms)
        idx = int(len(sorted_latencies) * 0.95)
        return sorted_latencies[idx] if idx < len(sorted_latencies) else sorted_latencies[-1]
    
    @property
    def latency_p99(self) -> float:
        if not self.latencies_ms:
            return 0.0
        sorted_latencies = sorted(self.latencies_ms)
        idx = int(len(sorted_latencies) * 0.99)
        return sorted_latencies[idx] if idx < len(sorted_latencies) else sorted_latencies[-1]
    
    def to_dict(self) -> Dict:
        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": round(self.success_rate, 4),
            "error_rate": round(self.error_rate, 4),
            "latency_p50_ms": round(self.latency_p50, 2),
            "latency_p95_ms": round(self.latency_p95, 2),
            "latency_p99_ms": round(self.latency_p99, 2),
            "last_request_at": self.last_request_at.isoformat() if self.last_request_at else None,
        }


class MetricsCollector:
    """
    Collects and aggregates model metrics.
    
    In production, integrate with:
    - Prometheus (via prometheus_client)
    - DataDog
    - CloudWatch
    - Grafana
    """
    
    # Maximum latencies to store per model (for memory efficiency)
    MAX_LATENCIES = 10000
    
    def __init__(self):
        self._metrics: Dict[str, ModelMetrics] = defaultdict(ModelMetrics)
        self._lock = threading.RLock()
    
    def record_inference(
        self,
        model_name: str,
        latency_ms: float,
        success: bool = True,
    ) -> None:
        """Record a single inference request."""
        with self._lock:
            metrics = self._metrics[model_name]
            metrics.total_requests += 1
            
            if success:
                metrics.successful_requests += 1
                # Only store latency for successful requests
                if len(metrics.latencies_ms) >= self.MAX_LATENCIES:
                    metrics.latencies_ms = metrics.latencies_ms[-self.MAX_LATENCIES//2:]
                metrics.latencies_ms.append(latency_ms)
            else:
                metrics.failed_requests += 1
            
            metrics.last_request_at = datetime.utcnow()
    
    def record_batch_inference(
        self,
        model_name: str,
        batch_size: int,
        total_latency_ms: float,
        success: bool = True,
    ) -> None:
        """Record a batch inference request."""
        # Record as batch_size individual requests
        avg_latency = total_latency_ms / batch_size
        for _ in range(batch_size):
            self.record_inference(model_name, avg_latency, success)
    
    def get_metrics(self, model_name: str) -> Optional[Dict]:
        """Get metrics for a specific model."""
        with self._lock:
            if model_name not in self._metrics:
                return None
            return self._metrics[model_name].to_dict()
    
    def get_all_metrics(self) -> Dict[str, Dict]:
        """Get metrics for all models."""
        with self._lock:
            return {
                name: metrics.to_dict()
                for name, metrics in self._metrics.items()
            }
    
    def reset_metrics(self, model_name: Optional[str] = None) -> None:
        """Reset metrics for a model or all models."""
        with self._lock:
            if model_name:
                self._metrics[model_name] = ModelMetrics()
            else:
                self._metrics.clear()


# Prometheus integration (optional)
try:
    from prometheus_client import Counter, Histogram, Gauge
    
    INFERENCE_COUNTER = Counter(
        'model_inference_total',
        'Total number of inference requests',
        ['model_name', 'status']
    )
    
    INFERENCE_LATENCY = Histogram(
        'model_inference_latency_seconds',
        'Inference latency in seconds',
        ['model_name'],
        buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
    )
    
    MODELS_LOADED = Gauge(
        'models_loaded_total',
        'Number of models currently loaded'
    )
    
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False


# Global metrics collector
_metrics_collector: Optional[MetricsCollector] = None


def get_metrics_collector() -> MetricsCollector:
    """Get the global metrics collector."""
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
    return _metrics_collector
```

### 7. API Schemas - `api/schemas.py`

```python
"""
API Request/Response Schemas.

Using Pydantic for:
- Automatic validation
- OpenAPI documentation
- Type safety
"""
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from datetime import datetime


# ============ Request Schemas ============

class PredictRequest(BaseModel):
    """Single prediction request."""
    text: str = Field(..., min_length=1, max_length=5000, description="Input text")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "This product is absolutely amazing! Best purchase ever."
            }
        }


class BatchPredictRequest(BaseModel):
    """Batch prediction request."""
    texts: List[str] = Field(
        ...,
        min_length=1,
        max_length=100,
        description="List of input texts"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "texts": [
                    "I love this!",
                    "This is terrible.",
                    "It's okay I guess."
                ]
            }
        }


# ============ Response Schemas ============

class SentimentResult(BaseModel):
    """Sentiment analysis result."""
    label: str = Field(..., description="POSITIVE, NEGATIVE, or NEUTRAL")
    score: float = Field(..., ge=0, le=1, description="Confidence score")
    probabilities: Dict[str, float] = Field(..., description="Class probabilities")


class PredictResponse(BaseModel):
    """Single prediction response."""
    model: str
    version: str
    result: SentimentResult
    latency_ms: float
    timestamp: str


class BatchPredictResponse(BaseModel):
    """Batch prediction response."""
    model: str
    version: str
    batch_size: int
    results: List[SentimentResult]
    latency_ms: float
    avg_latency_ms: float
    timestamp: str


class ModelInfo(BaseModel):
    """Model information response."""
    name: str
    version: str
    stage: str
    registered_at: str
    loaded: bool
    tags: Dict[str, str]
    metadata: Optional[Dict[str, Any]] = None
    health: Optional[Dict[str, Any]] = None


class ModelListResponse(BaseModel):
    """List of available models."""
    models: List[ModelInfo]
    total: int


class MetricsResponse(BaseModel):
    """Model metrics response."""
    model_name: str
    metrics: Dict[str, Any]


class HealthResponse(BaseModel):
    """API health check response."""
    status: str
    timestamp: str
    models_loaded: int
    version: str


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
```

### 8. API Routes - `api/routes.py`

```python
"""
API Routes - RESTful endpoints for Model-as-a-Service.

Follows REST best practices:
- Proper HTTP methods
- Meaningful status codes
- Consistent error handling
- OpenAPI documentation
"""
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from typing import Optional
from datetime import datetime

from .schemas import (
    PredictRequest,
    PredictResponse,
    BatchPredictRequest,
    BatchPredictResponse,
    ModelInfo,
    ModelListResponse,
    MetricsResponse,
    HealthResponse,
    ErrorResponse,
)
from services.model_service import (
    get_model_service,
    ModelService,
    ModelNotFoundError,
    ModelServiceError,
)
from services.monitoring import get_metrics_collector
from models.sentiment_model import SentimentInput


router = APIRouter()


def get_service() -> ModelService:
    """Dependency injection for model service."""
    return get_model_service()


# ============ Health & Info Endpoints ============

@router.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="API Health Check",
)
async def health_check(service: ModelService = Depends(get_service)):
    """Check API health and status."""
    models = service.list_available_models()
    loaded_count = sum(1 for m in models if m.get("loaded", False))
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        models_loaded=loaded_count,
        version="1.0.0",
    )


@router.get(
    "/models",
    response_model=ModelListResponse,
    tags=["Models"],
    summary="List Available Models",
)
async def list_models(service: ModelService = Depends(get_service)):
    """List all registered models and their status."""
    models = service.list_available_models()
    return ModelListResponse(
        models=[ModelInfo(**m) for m in models],
        total=len(models),
    )


@router.get(
    "/models/{model_name}",
    response_model=ModelInfo,
    tags=["Models"],
    summary="Get Model Details",
    responses={404: {"model": ErrorResponse}},
)
async def get_model(
    model_name: str = Path(..., description="Model name"),
    version: Optional[str] = Query(None, description="Model version (default: latest)"),
    service: ModelService = Depends(get_service),
):
    """Get detailed information about a specific model."""
    try:
        info = service.get_model_info(model_name, version)
        return ModelInfo(**info)
    except ModelNotFoundError:
        raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found")


# ============ Inference Endpoints ============

@router.post(
    "/models/{model_name}/predict",
    response_model=PredictResponse,
    tags=["Inference"],
    summary="Single Prediction",
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def predict(
    model_name: str = Path(..., description="Model name"),
    request: PredictRequest = ...,
    version: Optional[str] = Query(None, description="Model version"),
    service: ModelService = Depends(get_service),
):
    """
    Run inference on a single input.
    
    This endpoint is optimized for low-latency single predictions.
    For multiple predictions, use the batch endpoint.
    """
    try:
        # Convert request to model input
        model_input = SentimentInput(text=request.text)
        
        # Run inference
        result = await service.predict_async(model_name, model_input, version)
        
        return result
        
    except ModelNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ModelServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/models/{model_name}/predict/batch",
    response_model=BatchPredictResponse,
    tags=["Inference"],
    summary="Batch Prediction",
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def predict_batch(
    model_name: str = Path(..., description="Model name"),
    request: BatchPredictRequest = ...,
    version: Optional[str] = Query(None, description="Model version"),
    service: ModelService = Depends(get_service),
):
    """
    Run inference on multiple inputs.
    
    Benefits of batch prediction:
    - Higher throughput
    - Better GPU utilization
    - Lower average latency per item
    
    Maximum batch size is configurable (default: 32).
    """
    try:
        model_inputs = [SentimentInput(text=t) for t in request.texts]
        result = service.predict_batch(model_name, model_inputs, version)
        return result
        
    except ModelNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ModelServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============ Metrics Endpoints ============

@router.get(
    "/metrics/{model_name}",
    response_model=MetricsResponse,
    tags=["Monitoring"],
    summary="Get Model Metrics",
)
async def get_model_metrics(
    model_name: str = Path(..., description="Model name"),
):
    """Get performance metrics for a specific model."""
    metrics = get_metrics_collector().get_metrics(model_name)
    if metrics is None:
        metrics = {"message": "No metrics recorded yet"}
    
    return MetricsResponse(model_name=model_name, metrics=metrics)


@router.get(
    "/metrics",
    tags=["Monitoring"],
    summary="Get All Metrics",
)
async def get_all_metrics():
    """Get performance metrics for all models."""
    return get_metrics_collector().get_all_metrics()
```

### 9. Middleware - `api/middleware.py`

```python
"""
API Middleware - Cross-cutting concerns.

Handles:
- Rate limiting
- API key authentication
- Request logging
- Error handling
"""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Dict
import time
from datetime import datetime
import logging
from collections import defaultdict
import asyncio

from config.settings import get_settings


logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Simple rate limiting middleware.
    
    In production, use:
    - Redis-based rate limiting for distributed systems
    - Token bucket algorithm for smoother limits
    - Per-user/API-key limits
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.settings = get_settings()
        self._requests: Dict[str, list] = defaultdict(list)
        self._lock = asyncio.Lock()
    
    async def dispatch(self, request: Request, call_next: Callable):
        if not self.settings.require_api_key:
            return await call_next(request)
        
        client_ip = request.client.host if request.client else "unknown"
        
        async with self._lock:
            now = time.time()
            window_start = now - self.settings.rate_limit_window_seconds
            
            # Clean old requests
            self._requests[client_ip] = [
                ts for ts in self._requests[client_ip]
                if ts > window_start
            ]
            
            # Check limit
            if len(self._requests[client_ip]) >= self.settings.rate_limit_requests:
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "Rate limit exceeded",
                        "retry_after_seconds": self.settings.rate_limit_window_seconds,
                    },
                )
            
            # Record request
            self._requests[client_ip].append(now)
        
        return await call_next(request)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all API requests."""
    
    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url.path}")
        
        response = await call_next(request)
        
        # Log response
        duration_ms = (time.time() - start_time) * 1000
        logger.info(
            f"Response: {request.method} {request.url.path} "
            f"status={response.status_code} duration={duration_ms:.2f}ms"
        )
        
        return response


class APIKeyMiddleware(BaseHTTPMiddleware):
    """
    API Key authentication middleware.
    
    In production, integrate with:
    - OAuth 2.0
    - JWT tokens
    - API key management service
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.settings = get_settings()
        # In production, load from secure storage
        self._valid_keys = {"demo-api-key-12345"}
    
    async def dispatch(self, request: Request, call_next: Callable):
        if not self.settings.require_api_key:
            return await call_next(request)
        
        # Skip auth for health and docs
        if request.url.path in ["/health", "/docs", "/openapi.json", "/"]:
            return await call_next(request)
        
        api_key = request.headers.get(self.settings.api_key_header)
        
        if not api_key:
            return JSONResponse(
                status_code=401,
                content={"error": "API key required"},
            )
        
        if api_key not in self._valid_keys:
            return JSONResponse(
                status_code=403,
                content={"error": "Invalid API key"},
            )
        
        return await call_next(request)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Global error handler."""
    
    async def dispatch(self, request: Request, call_next: Callable):
        try:
            return await call_next(request)
        except Exception as e:
            logger.exception(f"Unhandled error: {e}")
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "timestamp": datetime.utcnow().isoformat(),
                },
            )
```

### 10. Main Application - `main.py`

```python
"""
Model-as-a-Service Application Entry Point.

This is where everything comes together:
- Initialize FastAPI app
- Register models
- Configure middleware
- Start server
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from config.settings import get_settings
from api.routes import router
from api.middleware import (
    RateLimitMiddleware,
    RequestLoggingMiddleware,
    APIKeyMiddleware,
    ErrorHandlerMiddleware,
)
from services.registry import get_registry, DeploymentStage
from models.sentiment_model import SentimentModel


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    
    Runs on startup and shutdown.
    """
    # ===== STARTUP =====
    logger.info("Starting Model-as-a-Service...")
    
    # Register models
    registry = get_registry()
    
    # Register sentiment model
    registry.register(
        name="sentiment",
        version="1.0.0",
        model_class=SentimentModel,
        stage=DeploymentStage.PRODUCTION,
        tags={"language": "en", "task": "sentiment-analysis"},
    )
    
    # You can register multiple versions
    registry.register(
        name="sentiment",
        version="0.9.0",
        model_class=SentimentModel,
        stage=DeploymentStage.STAGING,
        tags={"language": "en", "task": "sentiment-analysis"},
    )
    
    logger.info("Models registered successfully")
    
    # Pre-load production models (optional, reduces cold start)
    registry.get_loaded_instance("sentiment", "1.0.0")
    logger.info("Production models loaded")
    
    yield  # Application is running
    
    # ===== SHUTDOWN =====
    logger.info("Shutting down Model-as-a-Service...")
    
    # Unload all models
    for model_name in registry.list_models():
        for version in registry.list_versions(model_name):
            registry.unload_model(model_name, version)
    
    logger.info("All models unloaded")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description="""
# Model-as-a-Service API

Production-ready API for serving machine learning models.

## Features

- **Multi-model support**: Serve multiple models from a single API
- **Versioning**: Deploy and test multiple model versions
- **Batch inference**: Efficient batch processing for high throughput
- **Monitoring**: Built-in metrics and health checks
- **Rate limiting**: Protect against abuse

## Quick Start

1. List available models: `GET /api/v1/models`
2. Run inference: `POST /api/v1/models/sentiment/predict`
3. Check metrics: `GET /api/v1/metrics/sentiment`
        """,
        lifespan=lifespan,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add custom middleware (order matters - first added = outermost)
    app.add_middleware(ErrorHandlerMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(APIKeyMiddleware)
    
    # Include API routes
    app.include_router(router, prefix=settings.api_prefix)
    
    # Root redirect to docs
    @app.get("/", include_in_schema=False)
    async def root():
        return {"message": "Model-as-a-Service API", "docs": "/docs"}
    
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    settings = get_settings()
    
    print("=" * 60)
    print("  Model-as-a-Service")
    print("=" * 60)
    print(f"  API:     http://localhost:8000")
    print(f"  Docs:    http://localhost:8000/docs")
    print(f"  Health:  http://localhost:8000/api/v1/health")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Disable in production
        log_level="info",
    )
```

---

## Running the Application

### Start the Server

```powershell
# From the project directory
python main.py

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Test with cURL

```powershell
# Health check
curl http://localhost:8000/api/v1/health

# List models
curl http://localhost:8000/api/v1/models

# Get model info
curl http://localhost:8000/api/v1/models/sentiment

# Single prediction
curl -X POST http://localhost:8000/api/v1/models/sentiment/predict `
  -H "Content-Type: application/json" `
  -d '{"text": "This product is absolutely amazing!"}'

# Batch prediction
curl -X POST http://localhost:8000/api/v1/models/sentiment/predict/batch `
  -H "Content-Type: application/json" `
  -d '{"texts": ["I love it!", "Terrible experience", "Its okay"]}'

# Get metrics
curl http://localhost:8000/api/v1/metrics/sentiment
```

### Interactive Documentation

Open http://localhost:8000/docs in your browser for Swagger UI.

---

## Production Deployment Patterns

### 1. Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```powershell
# Build and run
docker build -t maas-api .
docker run -p 8000:8000 maas-api
```

### 2. Kubernetes Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: maas-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: maas-api
  template:
    metadata:
      labels:
        app: maas-api
    spec:
      containers:
      - name: maas-api
        image: maas-api:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        readinessProbe:
          httpGet:
            path: /api/v1/health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /api/v1/health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: maas-api
spec:
  selector:
    app: maas-api
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### 3. GPU-Enabled Deployment

```yaml
# For models requiring GPU
resources:
  limits:
    nvidia.com/gpu: 1
```

---

## Architect-Level Considerations

### 1. Scaling Strategies

| Strategy | When to Use |
|----------|-------------|
| **Horizontal (replicas)** | CPU-bound models, stateless |
| **Vertical (bigger instance)** | Large models, memory-bound |
| **GPU scaling** | Deep learning models |
| **Auto-scaling** | Variable traffic patterns |

### 2. Model Loading Patterns

```
Cold Start vs Warm Start:
┌─────────────────────────────────────────┐
│ COLD START (On-demand loading)          │
│ + Lower memory usage                    │
│ - High latency for first request        │
│ Use for: Infrequently used models       │
├─────────────────────────────────────────┤
│ WARM START (Pre-loaded)                 │
│ + Low latency                           │
│ - Higher memory usage                   │
│ Use for: Production models              │
└─────────────────────────────────────────┘
```

### 3. A/B Testing Architecture

```
┌──────────────┐
│   Request    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  A/B Router  │──── 90% ────▶ Model v1.0 (Production)
│              │
│              │──── 10% ────▶ Model v1.1 (Canary)
└──────────────┘
```

### 4. Monitoring Checklist

- [ ] Request latency (p50, p95, p99)
- [ ] Error rate
- [ ] Throughput (requests/second)
- [ ] Model load time
- [ ] Memory usage
- [ ] GPU utilization (if applicable)
- [ ] Model drift detection
- [ ] Input data quality

### 5. Security Best Practices

- [ ] API authentication (OAuth2, API keys)
- [ ] Rate limiting
- [ ] Input validation (size limits, content filtering)
- [ ] TLS encryption
- [ ] Audit logging
- [ ] Model access control
- [ ] Secrets management (no hardcoded keys!)

---

## Summary

| Component | Purpose |
|-----------|---------|
| **Model Interface** | Abstract contract all models implement |
| **Model Registry** | Version control, discovery, lifecycle |
| **Model Service** | Orchestration, inference execution |
| **API Layer** | HTTP endpoints, validation, docs |
| **Monitoring** | Metrics, health checks, alerting |
| **Middleware** | Auth, rate limiting, logging |

### Key Takeaways for Architects

1. **Decouple models from applications** - API-based access enables independent scaling
2. **Version everything** - Models, APIs, data schemas
3. **Design for failure** - Timeouts, retries, fallbacks
4. **Monitor obsessively** - Can't manage what you can't measure
5. **Automate deployment** - CI/CD for models, not just code
6. **Think about cold starts** - Pre-load critical models
7. **Plan for scale** - Batch inference, GPU utilization, horizontal scaling
