import logging
import cohere
from app.constants import COHERE_API_KEY
import guardrails as gd
from guardrails.validators import ValidRange, ValidChoices
from pydantic import BaseModel, Field
from rich import print
from typing import List, Optional
import json 
from rich import print




logging.basicConfig(level=logging.INFO)
logging.info('Program starts')


class VariableORM(BaseModel):
    name: str = Field(..., description="Name of the column")
    description: str = Field(..., description="Brief description of this column.")

    def __repr__(self) -> str:
        return f"VariableORM(id={self.id!r}, name={self.name!r})"


class DataframeORM(BaseModel):
    name: str = Field(..., description="Name of the table", validators=[ValidChoices(["CONTRACTS", "CUSTOMERS"], on_fail="reask")])
    description: str = Field(..., description="Brief description of this table")
    has_columns: bool
    # variables: Optional[List[VariableORM]] = Field(None, description="Columns present in this table. Each column should be classified into a separate item in the list.")

    def __repr__(self) -> str:
        return f"DataframeORM(id={self.id!r}, name={self.name!r})"


    


expert_message = """The "CONTRACTS" table contains information about the contracts the company has signed in the last 5 years in Europe. It is the only source of truth we have for this kind of data."""



PROMPT = """Given the following message from our company expert,
please extract a dictionary that contains a summary of what the expert says. Try not to miss anything the expert says but above all, DO NOT MAKE UP ANYTHING AND DO NOT CREATE COLUMNS THAT DO NOT EXIST.
Everything is to be written in English.

${expert_message}

${gr.complete_json_suffix_v2}
"""


guard = gd.Guard.from_pydantic(DataframeORM, prompt=PROMPT)



co = cohere.Client(api_key = COHERE_API_KEY)
res  = guard(
    co.generate,
    prompt_params={"expert_message": expert_message},
    model='command',
    max_tokens=1024,
    temperature=0.6
)

# Print the validated output from the LLM
print(json.dumps(res.validated_output, indent=2))

print(guard.history.last.iterations.first.rich_group)
