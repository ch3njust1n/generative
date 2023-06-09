"""
User-defined functions that generate code using LLM.
"""

import os
import openai
import anthropic
from dotenv import load_dotenv

from generative.metaclasses import AbstractGenerativeModel

load_dotenv()


class GPT4(AbstractGenerativeModel):
    """
    OpenAI Chat Completion API wrapper

    Args:
        prompt (string): The source code as context for function to replace.

    Returns:
        Source code of the generated function.
    """

    def generate(prompt: str) -> str:
        openai.api_key = os.getenv("OPENAI_API_KEY")

        if openai.api_key is None:
            raise ValueError(
                "The OPENAI_API_KEY environment variable is not set. Please provide your OpenAI API key."
            )

        messages = [
            {"role": "system", "content": "You are an elite Python programmer."},
            {"role": "user", "content": prompt},
        ]

        llm_code = openai.ChatCompletion.create(
            model=os.getenv("OPENAI_MODEL_GPT4"),
            messages=messages,
            temperature=float(os.getenv("TEMPERATURE", 0.7)),
        )

        return llm_code.choices[0].message.content


class GPT3(AbstractGenerativeModel):
    """
    OpenAI Completion API wrapper

    Args:
        prompt (string): The source code as context for function to replace.

    Returns:
        Source code of the generated function.
    """

    def generate(prompt: str) -> str:
        openai.api_key = os.getenv("OPENAI_API_KEY")

        if openai.api_key is None:
            raise ValueError(
                "The OPENAI_API_KEY environment variable is not set. Please provide your OpenAI API key."
            )

        llm_code = openai.Completion.create(
            model=os.getenv("OPENAI_MODEL"),
            prompt=prompt,
            temperature=float(os.getenv("TEMPERATURE", 0.7)),
            max_tokens=int(os.getenv("MAX_TOKENS", 3600)),
        )

        return llm_code.choices[0].text


class Claude(AbstractGenerativeModel):
    """
    Claude API wrapper

    Args:
        prompt (string): The source code as context for function to replace.

    Returns:
        Source code of the generated function.
    """

    def generate(prompt: str) -> str:
        c = anthropic.Client(os.getenv("ANTHROPIC_API_KEY"))
        llm_code = c.completion(
            prompt=f"{anthropic.HUMAN_PROMPT} {prompt}{anthropic.AI_PROMPT}",
            stop_sequences=[anthropic.HUMAN_PROMPT],
            model=os.getenv("ANTHROPIC_MODEL"),
            temperature=float(os.getenv("TEMPERATURE", 0.7)),
            max_tokens_to_sample=int(os.getenv("MAX_TOKENS", 3600)),
        )

        return llm_code["completion"]
