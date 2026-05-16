"""The utility functions for prompting models."""
import time
import openai


def call_openai_server_single_prompt(
    prompt, model="meta/llama-3.3-70b-instruct", max_decode_steps=512, temperature=0.8
):
  try:
    client = openai.OpenAI(
        api_key="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",
        base_url="https://integrate.api.nvidia.com/v1"
    )
    completion = client.chat.completions.create(
        model="meta/llama-3.3-70b-instruct",
        temperature=temperature,
        max_tokens=max_decode_steps,
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message.content
  except Exception as e:
    retry_time = 30
    print(f"Error: {e}. Retrying in {retry_time} seconds...")
    time.sleep(retry_time)
    return call_openai_server_single_prompt(prompt, model, max_decode_steps, temperature)


def call_openai_server_func(
    inputs, model="meta/llama-3.3-70b-instruct", max_decode_steps=512, temperature=0.8
):
  if isinstance(inputs, str):
    inputs = [inputs]
  outputs = []
  for input_str in inputs:
    output = call_openai_server_single_prompt(
        input_str, model=model,
        max_decode_steps=max_decode_steps,
        temperature=temperature,
    )
    outputs.append(output)
  return outputs


def call_palm_server_from_cloud(
    input_text, model="meta/llama-3.3-70b-instruct", max_decode_steps=512, temperature=0.8
):
  return call_openai_server_func(input_text, model, max_decode_steps, temperature)
