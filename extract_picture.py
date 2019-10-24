import os
import shutil
root = "C:\sspm\semantic-segmentation-pytorch-master\data\ADEChallengeData2016\images\\validation"
annotation = "C:\sspm\semantic-segmentation-pytorch-master\data\ADEChallengeData2016\\annotations\\validation"

for root2, dirs, files in os.walk(root):
    for file in files:
        path = os.path.join(root2, file)
        if("png" in file):
            shutil.move(path, annotation)
        else:
            shutil.move(path, root)
for dir in os.listdir(root):
    path = os.path.join(root, dir)
    if(os.path.isdir(path)):
        shutil.rmtree(path)