import os
import re

def extract_markdown(input_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 递归遍历文件夹
    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith('.txt'):
                input_path = os.path.join(root, filename)
                
                # 计算输出路径，保持相对路径结构
                relative_path = os.path.relpath(input_path, input_folder)
                output_path = os.path.join(output_folder, relative_path.replace('.txt', '.md'))
                
                # 确保输出文件夹的子文件夹存在
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                with open(input_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # 使用正则表达式提取markdown内容
                markdown_content = re.findall(r'```markdown(.*?)```', content, re.DOTALL)

                # 将提取的内容写入到新的md文件中
                with open(output_path, 'w', encoding='utf-8') as file:
                    for md in markdown_content:
                        file.write(md.strip() + '\n\n')

# 使用函数
extract_markdown('split', 'md')