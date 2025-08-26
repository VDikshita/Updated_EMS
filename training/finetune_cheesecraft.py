from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import get_peft_model, LoraConfig, TaskType

model_name = "mistralai/Mistral-7B-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

dataset = load_dataset("json", data_files="data/training_dataset.jsonl", split="train")

def tokenize(batch):
    return tokenizer(f"### Input:\n{batch['input']}\n\n### Response:\n{batch['output']}", truncation=True, padding="max_length")

tokenized = dataset.map(tokenize)
base_model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

lora_config = LoraConfig(task_type=TaskType.CAUSAL_LM, r=8, lora_alpha=16, lora_dropout=0.1)
model = get_peft_model(base_model, lora_config)

trainer = Trainer(
    model=model,
    train_dataset=tokenized,
    args=TrainingArguments(
        output_dir="cheesecraft-model",
        per_device_train_batch_size=2,
        num_train_epochs=3,
        logging_dir="logs",
        logging_steps=10,
        save_strategy="epoch"
    ),
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
)

trainer.train()
