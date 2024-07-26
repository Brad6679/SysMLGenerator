from openai import OpenAI
import time
import re 

"""
OpenAI Handling Class
"""
class sysmlGPT():

  """ 
      Initializes sysmlGPT object

      asst : str
            Assistant to use (image or text based)
  """
  def __init__(self, asst):
      
      if asst == "Default":
        self.asstid = "<Asst_ID_1>"
      elif asst == "Image":
        self.asstid = "<Asst_ID_2>"
      else:
        self.asstid = None # Smart city assistant unimplemented
      key = "<OpenAI Key>"
      self.client = OpenAI(api_key=key)
      self.assistant = self.client.beta.assistants.retrieve(assistant_id=self.asstid)


      self.thread = self.client.beta.threads.create()

  """ 
      Sends a query to ChatGPT using API

      prompt : str
            Textual prompt to input to GPT, None if inputting img

      img : str
            Image path to input to GPT, None if inputting text


      Returns : str
        Message response from ChatGPT
  """
  def run(self, prompt, img):
    if prompt == None and img == None:
      raise RuntimeError("ERROR: No text or image inputted but request submitted. Exiting.")

    if img != None:
      if prompt == None:
        prompt = "Using SysMLv2, generate code that describes the system depicted in this image."
      file = self.client.files.create(
      file=open(img, "rb"),
      purpose="vision"
      )
      self.thread = self.client.beta.threads.create(
        messages=[
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": prompt
              },
              {
                "type": "image_file",
                "image_file": {"file_id": file.id}
              },
            ],
          }
        ]
      )
    else:
      self.thread = self.client.beta.threads.create(
        messages=[
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": prompt
              }
          ]}])


    run = self.client.beta.threads.runs.create(
      thread_id=self.thread.id,
      assistant_id=self.asstid,
      )

    print("Awaiting response from ChatGPT Assistant...")
    while run.status != 'completed':
      time.sleep(5)
      run = self.client.beta.threads.runs.retrieve(thread_id=self.thread.id, run_id=run.id)
      
    messages = self.client.beta.threads.messages.list(
        thread_id=self.thread.id
      )
    message = self.client.beta.threads.messages.retrieve(
        thread_id=self.thread.id,
        message_id=messages.first_id
      )
  
    return message.content[0].text.value
      

  """ 
      Extracts code from GPT response using regular expression

      text : str
            GPT response text
  """
  def extract_code_blocks(self, text):
    
    # Regular expression to match code blocks
    code_block_pattern = re.compile(r'```(\w+)\n(.*?)```', re.DOTALL)
    
    # Find all code blocks in the text
    matches = code_block_pattern.findall(text)
    
    code_blocks = []
    for match in matches:
        # match[0] is the language (e.g., 'py')
        # match[1] is the code
        code_blocks = match[1]

    # No languge shown after backticks
    if len(code_blocks) == 0:
      code_block_pattern = re.compile(r'```\n(.*?)```', re.DOTALL)
    
      # Find all code blocks in the text
      matches = code_block_pattern.findall(text)
      
      code_blocks = []
      for match in matches:
          # match[0] is the language (e.g., 'py')
          # match[1] is the code
          code_blocks = match[0]
      
    return code_blocks


