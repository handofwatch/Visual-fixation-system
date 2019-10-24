import os

root = "C:\sspm\semantic-segmentation-pytorch-master\data\ADEChallengeData2016\\annotations\\validation"
delete = "_seg"
for file in os.listdir(root):
    pos = file.find(delete)
    #print(pos)
    if(pos!=-1):
        newName = file[0:pos]
        newName += ".png"
        os.rename(os.path.join(root,file), os.path.join(root, newName))