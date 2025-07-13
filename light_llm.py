from langchain_community.llms import CTransformers

def load_llm():
    return CTransformers(
        model="models/tinyllama-1.1b-chat-v1.0.Q2_K.gguf",  
        model_type='llama',
        config={
            "max_new_tokens": 512,
            "context_length": 2048,
            "temperature": 0.7,
            "top_p": 0.9,
            "stop": ["</s>"]
        },
        # Prevent HF hub access
        local_files_only=True
    )
