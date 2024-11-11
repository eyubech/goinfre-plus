from django.shortcuts import render
from django.http import FileResponse, HttpResponse
import urllib.parse
import os
import pwd
import shutil
import tempfile
import datetime
from django.views.decorators.csrf import csrf_exempt


def get_username():
    return os.environ.get('USER') or pwd.getpwuid(os.getuid()).pw_name

def get_user_home():
    return os.path.expanduser('~')

def is_path_allowed(path):
    """Check if the path is within user's home directory"""
    user_home = get_user_home()
    real_path = os.path.realpath(path)
    real_home = os.path.realpath(user_home)
    return real_path.startswith(real_home)

@csrf_exempt
def handle_upload(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            
            current_path = request.POST.get('path', get_user_home())
            
            if not is_path_allowed(current_path):
                return HttpResponse("Access denied", status=403)
            
            try:
                file_path = os.path.join(current_path, uploaded_file.name)
                with open(file_path, 'wb') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                
                return HttpResponse("File uploaded successfully", status=200)
            except Exception as e:
                print(f"Error uploading file: {e}")
                return HttpResponse("Error uploading file", status=500)
        else:
            return HttpResponse("No file uploaded", status=400)
    else:
        return HttpResponse("Method not allowed", status=405)
        
def create_zip(path):
    """Create a zip file of a directory."""
    temp_dir = tempfile.gettempdir()
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_name = f"{os.path.basename(path)}_{timestamp}.zip"
    zip_path = os.path.join(temp_dir, zip_name)
    
    try:
        shutil.make_archive(zip_path[:-4], 'zip', path)
        return zip_path
    except Exception as e:
        print(f"Error creating zip: {e}")
        return None

def index(request):
    user_home = get_user_home()
    
    current_path = request.GET.get('path', user_home)
    show_hidden = request.GET.get('hidden', 'false') == 'true'
    
    if not is_path_allowed(current_path):
        current_path = user_home
    
    try:
        items = os.listdir(current_path)
        contents = []
        
        if current_path != user_home:
            parent_path = os.path.dirname(current_path)
            if is_path_allowed(parent_path):
                contents.append({
                    'name': '..',
                    'path': parent_path,
                    'type': 'directory',
                    'size': '',
                    'is_hidden': False
                })
        
        for item in items:
            if not show_hidden and item.startswith('.'):
                continue
                
            full_path = os.path.join(current_path, item)
            if not is_path_allowed(full_path):
                continue
                
            try:
                is_hidden = item.startswith('.')
                if os.path.isdir(full_path):
                    try:
                        dir_size = sum(os.path.getsize(os.path.join(dirpath,filename)) 
                                     for dirpath, dirnames, filenames in os.walk(full_path)
                                     for filename in filenames)
                    except (PermissionError, OSError):
                        dir_size = 0
                        
                    contents.append({
                        'name': item,
                        'path': full_path,
                        'type': 'directory',
                        'size': dir_size,
                        'is_hidden': is_hidden
                    })
                else:
                    size = os.path.getsize(full_path)
                    contents.append({
                        'name': item,
                        'path': full_path,
                        'type': 'file',
                        'size': size,
                        'is_hidden': is_hidden
                    })
            except (PermissionError, OSError):
                continue
                
        contents.sort(key=lambda x: (x['type'] != 'directory', x['name'].lower()))
        
        context = {
            'contents': contents,
            'current_path': current_path,
            'username': get_username(),
            'show_hidden': show_hidden
        }
        return render(request, 'index.html', context)
    except (PermissionError, OSError):
        return HttpResponse("Access denied or path not found", status=403)

def download_file(request):
    filepath = request.GET.get('filepath')
    if not filepath:
        return HttpResponse("No file specified", status=400)
        
    filepath = urllib.parse.unquote(filepath)
    
    if not is_path_allowed(filepath):
        return HttpResponse("Access denied", status=403)
        
    try:
        if os.path.isdir(filepath):
            zip_path = create_zip(filepath)
            if zip_path:
                response = FileResponse(
                    open(zip_path, 'rb'),
                    as_attachment=True,
                    filename=os.path.basename(zip_path)
                )
                os.unlink(zip_path)
                return response
            else:
                return HttpResponse("Error creating zip file", status=500)
        elif os.path.isfile(filepath):
            return FileResponse(
                open(filepath, 'rb'),
                as_attachment=True,
                filename=os.path.basename(filepath)
            )
        else:
            return HttpResponse("File not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)