from light_llm import load_llm

print("test_llm.py is running...")
print("LLM loading started...")

llm = load_llm()

print("LLM loaded.")
print("Invoking model...")

prompt = "<|system|>\nYou are a helpful assistant.\n<|user|>\nWhat is the capital of France?\n<|assistant|>\n"
output = llm.invoke(prompt)
print(f"Model output (repr): {repr(output)}")
