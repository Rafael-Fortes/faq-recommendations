from pydantic import BaseModel, Field
from typing import Union, Dict

class BaseResponse(BaseModel):
    message: str = Field(..., description="The message to be displayed to the user")
    data: Union[BaseModel, Dict] = Field({}, description="The data to be displayed to the user")
