# import os
# import glob
# import pandas as pd
# import xml.etree.ElementTree as ET

# def xml_to_csv(path):
#     xml_lst = []
#     for xml_file in glob.glob(path + '/*.xml'):
#         tree = ET.parse(xml_file)
#         root = tree.getroot()
#         for m in root.findall('object'):
#             if(m[0].text == "coin"):
#                 continue
#             value = (root.find('filename').text,
#                     int(root.find('size')[0].text),
#                     int(root.find('size')[1].text),
#                     m[0].text,
#                     int(m[4][0].text),
#                     int(m[4][1].text),
#                     int(m[4][2].text),
#                     int(m[4][3].text)
#                     )

#             xml_lst.append(value)
#     column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
#     xml_df = pd.DataFrame(xml_lst, columns=column_name)
#     return xml_df


# def main():
#     image_path = os.path.join('/Users/kohseukim/ECUSTFD-resized-', 'annotations')
#     xml_df = xml_to_csv(image_path)
#     print(xml_df.shape)
#     print(xml_df.head)
#     xml_df.to_csv('/Users/kohseukim/ECUSTFD-resized-/test.csv', index=None, header=True)
#     print('Successfully converted xml to csv.')


# main()

import os
import shutil

with open('dataset/test.txt', 'r') as r:
    for line in sorted(r):
        if not os.path.exists('dataset/test'):
            os.makedirs('dataset/test')
        line = line.rstrip()
        filename = os.path.basename(line)
        shutil.copyfile(os.path.join('dataset/JPEGImages', line), os.path.join('dataset/test', filename))
