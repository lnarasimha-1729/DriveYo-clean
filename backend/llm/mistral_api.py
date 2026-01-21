import json
import urllib.request
from config.aws_config import MISTRAL_API_KEY

def explain_quote(ai_payload):

    system_prompt = (
        "You are a vehicle lease quote explainer.\n\n"

        "RULES:\n"
        "- Use ONLY values from the JSON\n"
        "- Compare dealer payment vs lowest market payment only\n"
        "- Include stackable incentives if present\n\n"

        "STACKABILITY RULES:\n"
        "- Stackable offers are discounts that can be combined\n"
        "- Display them under 'Stackable Incentives'\n\n"

        "TOP MARKET OFFERS RULES:\n"
        "- List the Top 3 Lowest Market Offers with payment and interest rate\n\n"

        "RATING RULES:\n"
        "- Dealer higher than market → Bad Deal\n"
        "- Equal → Average Deal\n"
        "- Lower → Good Deal\n"
    )

    req = urllib.request.Request(
        "https://api.mistral.ai/v1/chat/completions",
        data=json.dumps({
            "model": "mistral-small-latest",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(ai_payload, indent=2)}
            ],
            "temperature": 0.1
        }).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    res = json.loads(urllib.request.urlopen(req).read().decode())
    return res["choices"][0]["message"]["content"]
