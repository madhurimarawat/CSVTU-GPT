# Import necessary libraries and modules from Hugging Face's `transformers` library.
from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer,
    GPT2Config,
    TextDataset,
    DataCollatorForLanguageModeling,
)
from transformers import Trainer, TrainingArguments

# Load the pre-trained GPT-2 model and tokenizer from the Hugging Face model hub.
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Create a TextDataset object to prepare the training data for the model.
# The `file_path` parameter specifies the location of the text file containing training data.
# The `block_size` determines the maximum length of each input sequence (in tokens).
dataset = TextDataset(
    tokenizer=tokenizer,  # The tokenizer used for encoding the text data.
    file_path=r"C:\Users\YASH\Downloads\Telegram Desktop\Complete_website_data.txt",  # Path to the training data.
    block_size=128,  # Maximum number of tokens in each training example.
)

# Create a DataCollator for language modeling to handle data preprocessing during training.
# This will help in batch creation and padding sequences.
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,  # The tokenizer used to prepare input data.
    mlm=False,  # Indicates that we are not using masked language modeling (MLM).
)

# Set up training arguments to configure the training process.
# The `output_dir` specifies where the model and checkpoints will be saved.
# The `num_train_epochs` sets the number of training epochs.
# `per_device_train_batch_size` sets the batch size per device (GPU or CPU).
# `save_steps` determines how frequently the model is saved during training.
# `save_total_limit` limits the number of saved models to keep disk space usage in check.
training_args = TrainingArguments(
    output_dir="./gpt2_output",  # Directory to save the trained model and checkpoints.
    overwrite_output_dir=True,  # Whether to overwrite the output directory if it already exists.
    num_train_epochs=3,  # Number of training epochs.
    per_device_train_batch_size=32,  # Batch size per device.
    save_steps=10_000,  # Number of steps between saving checkpoints.
    save_total_limit=2,  # Limit the total number of saved checkpoints.
)

# Initialize the `Trainer` class to manage the training process.
# It handles the training loop, evaluation, and model saving.
trainer = Trainer(
    model=model,  # The pre-trained GPT-2 model to be fine-tuned.
    args=training_args,  # The training arguments.
    data_collator=data_collator,  # The data collator to use for training.
    train_dataset=dataset,  # The dataset used for training.
)

# Start the training process.
trainer.train()

# Import `pipeline` from `transformers` to create a simple text generation pipeline.
from transformers import pipeline

# Initialize the text generation pipeline using the fine-tuned GPT model and tokenizer.
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Generate text using the `generator` pipeline with a given prompt.
# The `max_length` sets the maximum length of the generated text.
# `num_return_sequences` determines the number of generated text sequences to return.
output = generator("University", max_length=50, num_return_sequences=5)

# Print each generated text sequence to the console.
for i, sequence in enumerate(output):
    print(f"Generated Text {i+1}: {sequence['generated_text']}")
