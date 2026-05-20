from dataclasses import dataclass
import os


DEFAULT_BASE_URL = "https://gorest.co.in/public/v2"


@dataclass(frozen=True)
class GorestConfig:
    base_url: str = DEFAULT_BASE_URL
    token: str | None = None
    timeout_seconds: int = 30
    max_retries: int = 5


def load_config_from_env() -> GorestConfig:
    return GorestConfig(
        base_url=os.getenv("GOREST_BASE_URL", DEFAULT_BASE_URL),
        token=os.getenv("GOREST_TOKEN"),
    )