import os
import json
import urllib.request

# Fixture matches the real /v1/messages response shape so surrounding code is
# identical whether MOCK=1 or not. Set MOCK=1 (or omit ANTHROPIC_API_KEY) to
# skip the network entirely — mirrors the TypeScript port.
_MOCK_RESPONSE = {
    "content": [
        {
            "type": "text",
            "text": "A neural network is a stack of differentiable functions that learns patterns by adjusting weights against a loss signal.",
        }
    ],
    "usage": {"input_tokens": 12, "output_tokens": 28},
}

_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "mock")
_MOCK = os.environ.get("MOCK") == "1" or _API_KEY == "mock"


def call_with_sdk():
    if _MOCK:
        r = _MOCK_RESPONSE
        print(f"SDK response: {r['content'][0]['text']}")
        print(f"Tokens used: {r['usage']['input_tokens']} in, {r['usage']['output_tokens']} out")
        return

    try:
        import anthropic
    except ImportError:
        print("Install the SDK: pip install anthropic")
        return

    client = anthropic.Anthropic(api_key=_API_KEY)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        messages=[{"role": "user", "content": "What is a neural network in one sentence?"}]
    )
    print(f"SDK response: {response.content[0].text}")
    print(f"Tokens used: {response.usage.input_tokens} in, {response.usage.output_tokens} out")


def call_raw_http():
    if _MOCK:
        r = _MOCK_RESPONSE
        print(f"Raw HTTP response: {r['content'][0]['text']}")
        print(f"Tokens used: {r['usage']['input_tokens']} in, {r['usage']['output_tokens']} out")
        return

    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": _API_KEY,
        "anthropic-version": "2023-06-01",
    }
    body = json.dumps({
        "model": "claude-sonnet-4-6",
        "max_tokens": 256,
        "messages": [{"role": "user", "content": "What is a neural network in one sentence?"}],
    }).encode()

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
        print(f"Raw HTTP response: {result['content'][0]['text']}")
        print(f"Tokens used: {result['usage']['input_tokens']} in, {result['usage']['output_tokens']} out")


if __name__ == "__main__":
    mode = "MOCK (no network). Unset MOCK and export ANTHROPIC_API_KEY for a live call." if _MOCK else "LIVE."
    print("=== API Calls ===\n")
    print(f"Mode: {mode}\n")
    print("1. Using the SDK:")
    call_with_sdk()
    print("\n2. Using raw HTTP:")
    call_raw_http()
