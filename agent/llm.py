"""Optional LLM 'veto' layer.

Given a technical signal, asks an LLM to CONFIRM or VETO the trade based on
lightweight context. If no provider is configured, the layer is a no-op.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Optional

from .config import CONFIG
from .signals import SignalResult


@dataclass
class LLMDecision:
    approve: bool
    rationale: str


_SYSTEM = (
    "You are a risk-aware crypto trading analyst. Given a proposed action and "
    "recent price stats, respond with STRICT JSON {\"approve\": bool, \"rationale\": str}. "
    "Approve only if the action looks consistent with the evidence and risk is reasonable."
)


def _prompt(symbol: str, signal: SignalResult, stats: dict) -> str:
    return (
        f"Symbol: {symbol}\n"
        f"Proposed action: {signal.action} (score={signal.score})\n"
        f"Technical reason: {signal.reason}\n"
        f"Recent stats: {json.dumps(stats)}\n"
        "Respond with JSON only."
    )


def _call_openai(prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=CONFIG.openai_api_key)
    resp = client.chat.completions.create(
        model=CONFIG.openai_model,
        messages=[
            {"role": "system", "content": _SYSTEM},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )
    return resp.choices[0].message.content or "{}"


def _call_anthropic(prompt: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=CONFIG.anthropic_api_key)
    msg = client.messages.create(
        model=CONFIG.anthropic_model,
        max_tokens=256,
        system=_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    # Anthropic returns list of content blocks
    parts = [b.text for b in msg.content if getattr(b, "type", "") == "text"]
    return "".join(parts) or "{}"


def _call_groq(prompt: str) -> str:
    """Groq free-tier provider. OpenAI-compatible API, so we reuse the openai SDK
    pointed at https://api.groq.com/openai/v1. Default model: llama-3.3-70b-versatile.
    """
    from openai import OpenAI
    client = OpenAI(
        api_key=CONFIG.groq_api_key,
        base_url=CONFIG.groq_base_url,
    )
    resp = client.chat.completions.create(
        model=CONFIG.groq_model,
        messages=[
            {"role": "system", "content": _SYSTEM},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )
    return resp.choices[0].message.content or "{}"


def review(symbol: str, signal: SignalResult, stats: dict) -> Optional[LLMDecision]:
    provider = CONFIG.llm_provider
    if not provider:
        return None
    try:
        prompt = _prompt(symbol, signal, stats)
        if provider == "openai":
            raw = _call_openai(prompt)
        elif provider == "anthropic":
            raw = _call_anthropic(prompt)
        elif provider == "groq":
            raw = _call_groq(prompt)
        else:
            return None
        data = json.loads(raw)
        return LLMDecision(
            approve=bool(data.get("approve", False)),
            rationale=str(data.get("rationale", ""))[:500],
        )
    except Exception as e:
        # LLM layer must never crash the agent
        return LLMDecision(approve=True, rationale=f"LLM error, defaulting to approve: {e}")
