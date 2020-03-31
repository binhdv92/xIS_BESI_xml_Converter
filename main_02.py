# In[] Import library
import xml.etree.ElementTree as ET
import pandas as pd
import argparse
import os

# In[] Argument
parser=argparse.ArgumentParser(description="This use for convert the xIS-Besi-xml-Format to the csv table format")
parser.add_argument('-k','--key_search',default="CoffeeLake6p2_IIS01_sealant-vi")

args=parser.parse_args()
print(args.__dict__)

# In[] list down all 'xml' files
temp_listdir=os.listdir()
temp_listdir_02=[]
for i in temp_listdir:
    if ".xml" in i:
        temp_listdir_02.append(i)

df=pd.DataFrame(columns=['id','lane','posX','posY','angle','tool'])
for file_name in temp_listdir_02:
    
    dummy_file=file_name[:-4] + '.binhdv92'
    start_root_tag="<root>"
    end__root_tag="</root>"
    
    # In[] This cell will add the root tag and save to "dummy_file"
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        write_obj.write(start_root_tag + '\n')
        for line in read_obj:
            write_obj.write(line)
        write_obj.write('\n' + end__root_tag + '\n')
    
    # In[] This cell will reading the xml file
    tree = ET.parse(dummy_file)
    root = tree.getroot()
    
    temp_id=''
    temp_lane=''
    temp_posX=''
    temp_posY=''
    temp_angle=''
    df1=pd.DataFrame(columns=['id','lane','posX','posY','angle','tool'])
    temptemp=f"inspectionResult/[@searchId='{args.key_search}']"
    print('binhdv92--------------------'+temptemp)
    for i,temp_unitData in enumerate(root.findall('trayData/unitData')):
        temp_id     = temp_unitData.attrib['id']
        temp_lane   = temp_unitData.attrib['lane']
        temp_posX   = temp_unitData.findall(str(temptemp))[0].attrib['posX']
        temp_posY   = temp_unitData.findall(str(temptemp))[0].attrib['posY']
        temp_angle  = temp_unitData.findall(str(temptemp))[0].attrib['angle']
        df2         = pd.DataFrame([[temp_id,temp_lane,temp_posX,temp_posY,temp_angle,file_name]],columns=['id','lane','posX','posY','angle','tool'])
        df1          = df1.append(df2,ignore_index=True)
    os.remove(dummy_file)
    df=df.append(df1)

# In[] save to csv
df.to_csv("result.csv",sep=',',index=False, header=True)
