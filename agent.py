"""
Agent module for handling shell commands and interacting with Google Generative AI.
"""

import os
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
import dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

dotenv.load_dotenv()


class CommandOutput(BaseModel):
    """Return the command and the output of the terminal after executing the command."""

    command: str = Field(..., description="Command that was executed")
    output: str = Field(
        ..., description="Output of the terminal after executing the command"
    )


@tool
async def run_command(command: str) -> CommandOutput:
    """Run a shell command and return the output.

    Args:
        command: a shell command to be run
    """
    try:
        process = await asyncio.create_subprocess_shell(
            command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout_lines: list[str] = []
        stderr_lines: list[str] = []

        async def read_stream(stream, lines, prefix: Optional[str] = None):
            while True:
                line = await stream.readline()
                if not line:
                    break
                decoded_line = line.decode().strip()
                if prefix:
                    print(f"{prefix}: {decoded_line}")
                lines.append(decoded_line)

        # Create coroutines for reading both stdout and stderr simultaneously
        await asyncio.gather(
            read_stream(process.stdout, stdout_lines, "stdout"),
            read_stream(process.stderr, stderr_lines, "stderr"),
        )

        await process.wait()

        output = "\n".join(stdout_lines + stderr_lines)
        return CommandOutput(command=command, output=output)
    except OSError as e:
        return CommandOutput(command="error", output=str(e))


tools = [run_command]

os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
llm_with_tools = llm.bind_tools(tools)


async def prompt_agent(msg: str = "") -> str:
    """Handle user input and generate a response using the LLM and available tools."""
    messages = [HumanMessage(msg)]

    ai_msg = llm_with_tools.invoke(messages)
    messages.append(HumanMessage(content=ai_msg.content))

    if hasattr(ai_msg, "tool_calls"):
        for tool_call in ai_msg.tool_calls:
            selected_tool = {"run_command": run_command}[tool_call["name"].lower()]
            tool_msg = await selected_tool.ainvoke(tool_call)
            messages.append(tool_msg)

    # Get the final response from the LLM
    ai_msg = llm_with_tools.invoke(messages)
    return str(ai_msg.content)
