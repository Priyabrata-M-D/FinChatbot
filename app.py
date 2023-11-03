import PyPDF2
from docx import Document
from llama_index import SimpleDirectoryReader,VectorStoreIndex, LLMPredictor,PromptHelper
from langchain import OpenAI
import os
from IPython.display import Markdown,display
from dotenv import load_dotenv
load_dotenv


# Function to convert PDF to text
def convert_pdf_to_text(pdf_path, output_directory):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()

            text_file_name = os.path.join(output_directory, f'page_{page_num + 1}.txt')
            with open(text_file_name, 'w', encoding='utf-8') as text_file:
                text_file.write(page_text)

# Function to convert DOCX to text
def convert_docx_to_text(docx_path, output_directory):
    doc = Document(docx_path)
    for i, paragraph in enumerate(doc.paragraphs):
        text_file_name = os.path.join(output_directory, f'paragraph_{i + 1}.txt')
        with open(text_file_name, 'w', encoding='utf-8') as text_file:
            text_file.write(paragraph.text)

# Main function
def main():
    user_input_file = input("Enter the path to your PDF or DOCX file: ")
    output_directory = 'text_files'
    os.makedirs(output_directory, exist_ok=True)

    file_extension = os.path.splitext(user_input_file)[-1].lower()

    if file_extension == '.pdf':
        convert_pdf_to_text(user_input_file, output_directory)
    elif file_extension == '.docx':
        convert_docx_to_text(user_input_file, output_directory)
    else:
        print("Unsupported file format. Please provide a PDF or DOCX file.")

def construct_index(directory_path):
  #max input size
  max_input_size=4096
  num_outputs=256
  max_chunk_overlap=0.3
  chunk_size_limit=600

  #defining LLM
  llm_predictor=LLMPredictor(llm=OpenAI(temperature=0.5, model_name='text-davinci-003',max_tokens=num_outputs))
  
  prompt_helper=PromptHelper(max_input_size,num_outputs,max_chunk_overlap,chunk_size_limit=chunk_size_limit)
  
  documents=SimpleDirectoryReader(directory_path).load_data()
  
  index=VectorStoreIndex(documents,llm_predictor=llm_predictor, prompt_helper=prompt_helper)
  
  index.save_to_disk(index.json)
  
  return index

def ask_ai():
  index=VectorStoreIndex.load_from_disk('index.json')
  while True:
    query=input('Ask Me a Question...')
    response=index.query(query,response_mode='compact')
    display(Markdown(f'Response: <b>(response.response</b>)'))

if __name__ == '__main__':
  main()
  #os.environ['OPENAI_API_KEY']=input("Paste Your API key Here.....")
  construct_index(r'path\Desktop\Priyabrata Moharana_Tanfund\text_files')
  ask_ai()