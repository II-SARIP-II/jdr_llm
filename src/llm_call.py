from typing import TypeVar

from ollama import chat
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class LLMClient:
    def __init__(self, model: str, temperature: float = 0.4):
        self.model = model
        self.temperature = temperature

    def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        """Pour les réponses en texte libre."""
        response = chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            options={"temperature": self.temperature},
        )
        return response.message.content or ""

    def generate_structured(
        self, system_prompt: str, user_prompt: str, response_model: type[T]
    ) -> T:
        """Force Ollama à respecter un schéma Pydantic et \
            renvoie directement l'objet Python."""
        response = chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            format=response_model.model_json_schema(),
            options={"temperature": self.temperature},
        )
        raw_json = response.message.content or "{}"
        return response_model.model_validate_json(raw_json)
