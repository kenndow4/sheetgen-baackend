from pydantic import BaseModel

class PromptRequestDto(BaseModel):
    prompt: str
