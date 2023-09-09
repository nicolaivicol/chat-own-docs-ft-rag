import os
import time
import openai

import config


openai.api_key = os.getenv("OPENAI_API_KEY", config.OPENAI_API_KEY)

file_name = 'qa_manual_20230909_1650.jsonl'
suffix = 'manual_09_1650'

file_training_response = openai.File.create(
    file=open(f'{config.DIR_DATA}/qa/{file_name}', 'rb'),
    purpose='fine-tune',
)
training_file_id = file_training_response["id"]

# training_file_id = 'file-JMOeHhChjAcBKVqiSq26oPWm'
print("Training file ID:", training_file_id)

r = openai.File.retrieve(training_file_id)
print(f"file status: {r['status']}")
while r['status'] not in ['processed', 'error']:
    time.sleep(10)
    r = openai.File.retrieve(training_file_id)
    print(f"file status: {r['status']}")

response = openai.FineTuningJob.create(
    training_file=training_file_id,
    model='gpt-3.5-turbo-0613',
    suffix=f'{suffix}',
)
job_id = response["id"]
print("Training job ID:", job_id)
# job_id = 'ftjob-q8Cn5SMsW8jzVWyarctXdv81'

response = openai.FineTuningJob.retrieve(job_id)
print(f"status for training job {job_id} : {response['status']}")

while response['status'] not in ['succeeded', 'failed']:
    time.sleep(10)
    response = openai.FineTuningJob.retrieve(job_id)
    print(f"status for training job {job_id} : {response['status']}")
    print("Trained Tokens:", response["trained_tokens"])
