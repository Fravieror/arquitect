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

    # API configuration
    api_title: str = "Model-as-a-service API"
    api_version: str = "1.0.0"
    api_prefix: str = "/api/v1"

    # Model Configuration
    model_cache_dr: str = "./model_cache"
    default_model_version: str = "latest"
    model_timeout_seconds: int = 30

    # rate limiting
    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60

    # monitoring
    enable_metrics: bool = True
    metrics_port: int = 9090

    # feature flags
    enable_model_caching: bool = True
    enable_batch_inference: bool = True
    max_batch_size: int = 32

    # security
    api_key_header: str = "X-API-Key"
    require_api_key: bool = False

    class Config:
        env_file = ".env"
        env_prefix = "MAAS_"

@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()