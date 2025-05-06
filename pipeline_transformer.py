from transformers import pipeline

# Load a text generation pipeline
generator = pipeline("text-generation", model="gpt2")

# Provide a prompt
prompt = "The future of artificial intelligence is"

# Get generated text
output = generator(prompt, max_length=50, num_return_sequences=1)

# Print the result
print(output[0]['generated_text'])
