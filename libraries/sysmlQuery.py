from sysmlGPT import sysmlGPT
from jupyterBook import JupyterBook
import os
import json
import argparse

parser = argparse.ArgumentParser(
                    prog='SysMLQueryTool',
                    description='Sends text query to GPT and dumps SysMLv2 results.',
                    epilog='Text at the bottom of help')

parser.add_argument('-i', '--in_filename')
parser.add_argument('-d', '--img_dir', required = False)   
parser.add_argument('-o', '--out_filename')

args = parser.parse_args()

def read_text_file(file_path):
    # Open the file in read mode and read line by line
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def list_image_paths(directory):
    # Supported image file extensions
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
    image_paths = []
    
    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(image_extensions):
                # Append the absolute path to the image
                image_paths.append(os.path.join(root, file))
    
    return image_paths

# Example usage
text_file_path = f'{argsin_filename}'
if args.img_dir:
    # ../prompts
    image_directory = f'{args.img_dir}'
    image_paths = list_image_paths(image_directory)

lines = read_text_file(text_file_path)

sysml = sysmlGPT('Default')
jpnb = JupyterBook() 
i = 1
outDict = {}
for line in lines:
    try:
        #print(line)
        
        code = sysml.extract_code_blocks(sysml.run(line, None))
        if len(code) == 0:
            pass
        else:
            pind = code.find("package")
            bind = code.find("{", pind)
            name = code[pind + len("package"):bind].strip()
            viz = f'%viz --view=tree {name}'
            errors = jpnb.runCode(code, viz)
            codeWorks = errors[0]['outputs'][0].keys()
            if 'name' in codeWorks:
                e = errors[0]['outputs'][0]['name'] + " " + errors[0]['outputs'][0]['text']
            else:
                e = errors[0]['outputs'][0]['data']
            #e = errors[0]['outputs'][0]['name'] + " " + errors[0]['outputs'][0]['text']
            outDict[f'Run{i}'] = {'Syntax Score': 0, 'Errors': e, 'Code': code, 'ImgFile': "", 'Prompt': line}
            outDict[f'Run{i}']['Syntax Score'] = str(round(1.0 - float(len(e.splitlines())) / float(len(code.splitlines())), 2) * 100) + "%"
            if len(errors) > 1:
                keys = errors[1]['outputs'][0]['data'].keys()
                if 'image/svg+xml' in keys:
                    svg_content = errors[1]['outputs'][0]['data']['image/svg+xml']

                #print(svg_content)

                    cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), write_to=f'output/output{i}.png')
                    outDict[f'Run{i}']['ImgFile'] = f'output/output{i}.png'
            run = outDict[f'Run{i}']
            print(f"Saving Data: {run}")
        
    except Exception as ex:
        print(ex)
    i += 1

    
    
    
'''
for line in image_paths:
    try:
        #print(line)
        
        code = sysml.extract_code_blocks(sysml.run(line, None))
        if len(code) == 0:
            pass
        else:
            pind = code.find("package")
            bind = code.find("{", pind)
            name = code[pind + len("package"):bind].strip()
            viz = f'%viz --view=tree {name}'
            errors = jpnb.runCode(code, viz)
            codeWorks = errors[0]['outputs'][0].keys()
            if 'name' in codeWorks:
                e = errors[0]['outputs'][0]['name'] + " " + errors[0]['outputs'][0]['text']
            else:
                e = errors[0]['outputs'][0]['data']
            #e = errors[0]['outputs'][0]['name'] + " " + errors[0]['outputs'][0]['text']
            outDict[f'Run{i}'] = {'Syntax Score': 0, 'Errors': e, 'Code': code, 'ImgFile': "", 'Prompt': line}
            score = float(len(code.splitlines())) / float(len(e.splitlines()))
            if score >= .35:
                outDict[f'Run{i}']['Syntax Score'] = 0
            elif score < .35 and score >= .25:
                outDict[f'Run{i}']['Syntax Score'] = .33
            elif score < .25 and score >= .5:
                outDict[f'Run{i}']['Syntax Score'] = .67
            else:
                outDict[f'Run{i}']['Syntax Score'] = 1
            if len(errors) > 1:
                keys = errors[1]['outputs'][0]['data'].keys()
                if 'image/svg+xml' in keys:
                    svg_content = errors[1]['outputs'][0]['data']['image/svg+xml']

                #print(svg_content)

                    cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), write_to=f'output/output{i}.png')
                    outDict[f'Run{i}']['ImgFile'] = f'output/output{i}.png'
            run = outDict[f'Run{i}']
            print(f"Saving Data: {run}")
        
    except Exception as ex:
        print(ex)
    i += 1'''


with open(f'output/{args.out_filename}', 'w') as fp:
    i = 1
    for i in outDict:
        fp.write(f" ----- TEST {i} -----\n")
        fp.write("Prompt: " + outDict[i]['Prompt'] + "\n")
        fp.write("Code: " + outDict[i]['Code']+ "\n")
        fp.write("Errors: " + str(outDict[i]['Errors']) + "\n")
        fp.write("Syntax Score: " + str(outDict[i]['Syntax Score'])+ "\n")
        fp.write("Image File: " + outDict[i]['ImgFile']+ "\n")

    
