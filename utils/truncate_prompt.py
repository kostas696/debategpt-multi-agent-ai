def truncate_prompt(prompt, tokenizer=None, max_tokens=512):
    """
    Truncates a prompt to fit within the token limit.
    If tokenizer is provided, uses tokenizer-based truncation;
    otherwise, falls back to character slicing.
    """
    if tokenizer:
        tokens = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=max_tokens)
        return tokenizer.decode(tokens['input_ids'][0], skip_special_tokens=True)
    else:
        return prompt[:2048]