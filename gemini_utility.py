import os
import json
import google.generativeai as genai

from PIL import Image

working_directory=os.path.dirname(os.path.abspath(__file__))

config_file_path=f"{working_directory}/config.json"
# print(config_file_path)
config_data=json.load(open(config_file_path))

GOOGLE_API_KEY=config_data["GOOGLE_API_KEY"]

genai.configure(api_key=GOOGLE_API_KEY)

def load_gemini_pro_model():
    gemini_pro_model=genai.GenerativeModel("gemini-pro")
    return gemini_pro_model

def load_gemini_pro_vision_model(prompt, image):
    gemini_pro_vision_model=genai.GenerativeModel("gemini-pro-vision")
    response=gemini_pro_vision_model.generate_content([prompt, image])
    result=response.text
    return result

# image=Image.open('test.jpg')
#
# prompt="Write a short caption for this image"
#
# output=load_gemini_pro_vision_model(prompt, image)
# print(output)



def load_embedding_model_response(text):
    embedding_model="models/embedding-001"
    embedding=genai.embed_content(model=embedding_model,
                                  content=text,
                                  task_type="retrieval_document")
    embedding_list=embedding["embedding"]
    return embedding_list

# output=load_embedding_model_response("Who is Thanos")
# print(output)




def gemini_pro_response(user_prompt):
    gemini_pro_model = genai.GenerativeModel("gemini-pro")
    response = gemini_pro_model.generate_content(user_prompt)
    result = response.text
    return result
