def generate_email(client, model, *, audience, product, value_proposition, tone):
    response = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "Write one concise, personalized cold outreach email. "
                    "Return only a JSON object with string fields 'subject' and 'body'. "
                    "Do not invent customer results or factual claims."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Audience: {audience}\n"
                    f"Product: {product}\n"
                    f"Value proposition: {value_proposition}\n"
                    f"Tone: {tone}"
                ),
            },
        ],
    )

    import json

    content = response.choices[0].message.content
    draft = json.loads(content)
    if not isinstance(draft.get("subject"), str) or not isinstance(
        draft.get("body"), str
    ):
        raise ValueError("Model response must contain string subject and body fields")
    return {"subject": draft["subject"], "body": draft["body"]}