import os
import subprocess
from django.http import HttpResponse, JsonResponse
import datetime
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import sys
import shutil

def home(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


@csrf_exempt
def restore_photo(request):
    myfile = request.FILES["image"]
    fs = FileSystemStorage("gfpgan/inputs/upload")
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    print(uploaded_file_url)
    print(os.listdir('gfpgan/inputs/upload'))
    inference()
    return JsonResponse({"img_src": uploaded_file_url})


def run_cmd(command):
    try:
        print(command)
        subprocess.call(command, shell=True)
    except KeyboardInterrupt:
        print("Process interrupted")
        sys.exit(1)


def inference():
    INPUT_DIR = "inputs/upload"
    OUTPUT_DIR = "results"
    oldFolder = os.getcwd()
    os.chdir('gfpgan')
    print(os.listdir('inputs/upload'))
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    run_cmd("python inference_gfpgan.py -s 2 -i " + INPUT_DIR + " -o " + OUTPUT_DIR)
    print(os.listdir('results'))
    shutil.rmtree(INPUT_DIR, ignore_errors=True)
    os.chdir(oldFolder)
    return os.path.join(OUTPUT_DIR, "1_out.jpg")
