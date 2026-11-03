"""
Agent Package for OmniConvert AI
Contains the 24/7 autonomous copilot, customer support knowledge base, and tool execution system.
"""
from .knowledge_base import PROJECT_KNOWLEDGE_BASE, get_system_prompt, get_quick_prompts
from .chatbot import OmniAgentChatbot

__all__ = [
    "PROJECT_KNOWLEDGE_BASE",
    "get_system_prompt",
    "get_quick_prompts",
    "OmniAgentChatbot",
]
