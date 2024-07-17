import base64
import requests
import glob
import os
from openai import OpenAI
import time
import re



class sysmlGPT():
  def __init__(self, asst):
      if asst == "Default":
        self.asstid = "asst_rkxmYDfYwpz7DH6x5MIFL2ID"
      else:
        self.asstid = None # Smart city assistant unimplemented
      key = "<OpenAI Key>"
      self.client = OpenAI(api_key=key)
      self.assistant = self.client.beta.assistants.retrieve(assistant_id=self.asstid)


      self.thread = self.client.beta.threads.create()

  

  # Function to encode the image
  def encode_image(self, image_path):
    with open(image_path, "rb") as image_file:
      return base64.b64encode(image_file.read()).decode('utf-8')


  def run(self, prompt, img):
    if prompt == None and img == None:
      #sys.exit("System exited. Input image or text")
      return "System exited. Input image or text"

    if img != None:
      if prompt == None:
        prompt = "Using SysMLv2, generate code that describes the system depicted in this image."
      #base64_image = encode_image(image_path)
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
  
    #d = content#messages.content[0].text
    
    #for message in messages.data:
     # d.append(message.content[0])
    return message.content[0].text.value
      

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
        #print(match[1])
    
    return code_blocks

#sys = sysmlGPT('Default')
#out = sys.run("Generate sysmlv2 code that models a car", None)
#out = sys.run("Generate sysmlv2 that models the system described in this image", "C:\\Users\\brady\\Downloads\\92bc146b.jpg")
#print(out)
#print(out.text)#message.content[0].text
