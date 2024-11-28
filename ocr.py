import base64
import requests
import os
from pdf2image import convert_from_path

# OpenAI API Key
api_key = ''

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

directory = './split'  # 修改为拆分后的PDF文件目录

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.lower().endswith('.pdf'):
            pdf_path = os.path.join(root, file)
            images = convert_from_path(pdf_path)
            
            for i, image in enumerate(images):
                image_path = f"{os.path.splitext(pdf_path)[0]}_{i}.png"
                image.save(image_path, 'PNG')
                
                base_name = os.path.splitext(image_path)[0]
                txt_file_path = f"{base_name}.txt"
                
                if os.path.exists(txt_file_path):
                    print(f"跳过 {image_path}，因为 {txt_file_path} 已存在。")
                    continue
                
                base64_image = encode_image(image_path)
                print(image_path)
                
                payload = {
                    "model": "gpt-4o",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "请将这张图片上的内容转化成markdown格式返回给我。"
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ]
                }
                
                response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                print(response.json())
                text = response.json()['choices'][0]['message']['content']
                
                with open(txt_file_path, 'w', encoding='utf-8') as fw:
                    fw.write(text)
                
                # 删除临时生成的PNG文件
                os.remove(image_path)