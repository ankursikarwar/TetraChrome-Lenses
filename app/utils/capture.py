import os 

def image_capture_and_save(HighResolution = True):
    print("Capture requested")
    if (HighResolution == True):
        os.system('sh /app/utils/high_res_capture.sh')
    if (HighResolution == False):
        os.system('sh /app/utils/low_res_capture.sh')
    if (len(os.listdir('./data/capture')) == 0):
        return False
    else:
        print('Capture Successful')
        return True
