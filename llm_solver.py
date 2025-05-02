from openai import OpenAI
import time

# Make sure to export environment variable OPENAI_API_KEY

TSP_4o_ID = 'asst_sv7Y0koVte4odmHCmnJoKz8V'
TSP_o1_ID = 'asst_QrJ43lrH8FWXD8xc7Y3l8ayB'

class LLMSolver():
  def __init__(self, model="gpt-4o"):
    if model == "gpt-4o":
      self.ASSISTANT_ID = TSP_4o_ID
    elif model == "o1":
      self.ASSISTANT_ID = TSP_o1_ID

    self.client = OpenAI()
    self.thread = self.client.beta.threads.create()

  def set_assistant(self, model):
    if model == "gpt-4o":
      self.ASSISTANT_ID = TSP_4o_ID
    elif model == "o1":
      self.ASSISTANT_ID = TSP_o1_ID

  def analyze(self, text):
    # Add message to a thread
    message = self.client.beta.threads.messages.create(
        thread_id=self.thread.id,
        role="user",
        content=str(text),
    )

    # Create a run
    run = self.client.beta.threads.runs.create(
      thread_id=self.thread.id,
      assistant_id=self.ASSISTANT_ID,
    )
      
    # Check for status of run
    while run.status in ['queued', 'in_progress', 'cancelling']:
      time.sleep(1) # Wait for 1 second
      run = self.client.beta.threads.runs.retrieve(
        thread_id=self.thread.id,
        run_id=run.id
      )

    # return message
    if run.status == 'completed': 
      message_response = self.client.beta.threads.messages.list(
        thread_id=self.thread.id
      )
      messages = message_response.data
      latest_message = messages[0]

      return latest_message.content[0].text.value
    else:
      return run.status
