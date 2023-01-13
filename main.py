from exif import Image as ExifImage
import os
import pandas as pd
import PySimpleGUI as sg

data = []

def get_exif_data(image_dir):
    for filename in os.listdir(image_dir):
        if filename.endswith('.JPG'):
            image_path = f'{image_dir}/{filename}'
            row = {"file_name": filename}
            with open(image_path, 'rb') as image_file:
                meta_image = ExifImage(image_file)
                for tag in meta_image.list_all():
                    try:
                        row[tag] = getattr(meta_image, tag)
                    except NotImplementedError:
                        row[tag] = "NULL"
                    except AttributeError:
                        row[tag] = "NULL"
                data.append(row)

    df = pd.DataFrame.from_dict(data)
    df.to_csv(image_dir + "/exif_data.csv")

# GUI Config 
sg.theme('DarkAmber')

status = [(''), ('Extracting EXIF From Images, Please Wait...'), ('No Images Selected')]

folder = [[sg.Text('Image Folder'), sg.In(size=(25,1), enable_events=True ,key='image_dir'), sg.FolderBrowse()]]
layout = [[sg.Column(folder, element_justification='c')],[sg.Text(text=status[0], size=(50,1), text_color='white', key='INDICATOR', justification='center')],[sg.Button('Ok'), sg.Button('Cancel')]]    
window = sg.Window('EXIF Data Extractor', layout,resizable=True)   

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'Ok' and values['image_dir'] == '':
        window['INDICATOR'].update(value=status[2])
    elif event == 'Ok' and values['image_dir']:
        window['INDICATOR'].update(value=status[1])
        image_dir = values['image_dir']
        window.perform_long_operation(lambda:get_exif_data(image_dir), 'COMPLETE')
    elif event =='COMPLETE':
        window['INDICATOR'].update(value=status[0])
        sg.popup("Extraction Completed")
        
    if event =='Cancel':
        raise SystemExit 
window.close()