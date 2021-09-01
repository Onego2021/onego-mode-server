import os
import os.path
import json

def search_dir(dir):
    files = os.listdir(dir)
    result = []
    
    for item in files:
        if item.startswith('.ipynb'):
            pass
        elif os.path.isdir(dir+"/"+item) == True: 
            result.append(dir+"/"+item)
    return result
    
def search_json(dir):
    file = os.listdir(dir)
    json_list = [dir+"/"+json_file for json_file in file if(json_file.endswith('.json'))]
    return json_list

def search_jpg(dir):
    file = os.listdir(dir)
    jpg_list = [jpg_file for jpg_file in file if(jpg_file.endswith('.jpg'))]
    return jpg_list
    
if __name__ == '__main__':
    train_img_dir = search_dir("onego_data/Training/image_onego")
    train_label_dir = search_dir("onego_data/Training/label_onego")
    valid_img_dir = search_dir("onego_data/Validation/image_onego")
    valid_label_dir = search_dir("onego_data/Validation/label_onego")
    
    train_str = ""
    valid_str = ""
    
    for i in range(0, len(train_img_dir)):
        img = search_jpg(train_img_dir[i])
        json_files = search_json(train_label_dir[i])
        
        for j in range(0, len(json_files)):
            with open(json_files[j],'r') as f:
                json_data = json.load(f)
            train_str += "{}/{}\t{}\n".format(json_data['image']['file_name'][0:3],json_data['image']['file_name'],json_data['info']['text'])
            
        
    f = open("onego_data/train_gt.txt","w")
    f.write(train_str)
    f.close()
    
    for i in range(0, len(valid_img_dir)):
        img = search_jpg(valid_img_dir[i])
        json_files = search_json(valid_label_dir[i])
        
        for j in range(0, len(json_files)):
            with open(json_files[j],'r') as f:
                json_data = json.load(f)
            valid_str += "{}/{}\t{}\n".format(json_data['image']['file_name'][0:3],json_data['image']['file_name'],json_data['info']['text'])
    
    f = open("onego_data/valid_gt.txt","w")
    f.write(valid_str)
    f.close()
            
    