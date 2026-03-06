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
    """model metadata for registry."""
    name: str
    version: str
    description: str
    created_at: datetime
    framework: str # pytorch, tensorflow, sklearn, etc.
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    tags: List[str] = []
    metrics: Dict[str, float] = {} # accuracy, latency, etc.

# generic types for input/output
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
        # Expan on this in plain english: This is a counter that keeps track of 
        # how many times the model has been used to make predictions. 
        # It starts at zero when the model is initialized and increments each time 
        # the model's predict method is called. 
        # This can be useful for monitoring usage patterns, performance, 
        # and for implementing features like rate limiting or usage-based billing.       
        
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
    # what does pass here mean? It means that the method is defined but not implemented.
    # is like it is a handoff to the child class to implement the method. 
    # It is a way to define an interface that all child classes must follow.

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

class ModelInfereceError(Exception):
    """Raised when inference fails."""
    pass


