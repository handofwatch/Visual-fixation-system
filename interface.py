import test
import os
import extract_frame

def analysis(path):
    os.system("python -u test.py \
    --imgs %s  \
    --cfg config/ade20k-resnet101-upernet.yaml \
    TEST.result ./ \
    TEST.suffix _epoch_40.pth"%(path))

def analysis_for_video(path):
    result_path = os.path.join(os.path.dirname(path), "images")
    extract_frame.extract_frame(path, result_path)
    analysis(result_path)

analysis_for_video("C:\\test\\test_video2.mp4")