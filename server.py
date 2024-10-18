"""
This module contains the FastAPI application and endpoint for running the agent.
"""

from fastapi import FastAPI, Request
from pydantic import BaseModel
from agent import prompt_agent

app = FastAPI()


class Message(BaseModel):
    """
    Message model for the agent response.
    """

    msg: str


@app.post("/agent", response_model=Message)
async def run_agent(req: Request) -> Message:
    """
    Endpoint to run the agent with the provided message.
    """
    json = await req.json()
    res = await prompt_agent(json["msg"])
    return Message(msg=res)
