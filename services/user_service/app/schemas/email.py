from pydantic import BaseModel
from typing import Dict

class EmailTemplate(BaseModel):
    template_name: str
    context: Dict[str, str] 