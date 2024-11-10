from django.shortcuts import render
from django.http import FileResponse, HttpResponse
import urllib.parse
import os
import pwd
import shutil
import tempfile
import datetime

def get_username():
    return os.environ.get('USER') or pwd.getpwuid(os.getuid()).pw_name

def get_user_home():
    return os.path.expanduser('~')

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

def is_path_allowed(path):
    """Check if the path is within user's home directory"""
    user_home = get_user_home()
    real_path = os.path.realpath(path)
    real_home = os.path.realpath(user_home)
    return real_path.startswith(real_home)

def index(request):
    # Get user's home directory
    user_home = get_user_home()
    
    # Get the base path from the request or default to user's home directory
    current_path = request.GET.get('path', user_home)
    show_hidden = request.GET.get('hidden', 'false') == 'true'
    
    # Security check to prevent directory traversal
    if not is_path_allowed(current_path):
        current_path = user_home
    
    # Get directory contents
    try:
        items = os.listdir(current_path)
        contents = []
        
        # Add parent directory if we're not at home
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
        
        # Add all directories and files
        for item in items:
            # Skip hidden files if show_hidden is False
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
                
        # Sort directories first, then files
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
            # Create zip file for directory
            zip_path = create_zip(filepath)
            if zip_path:
                response = FileResponse(
                    open(zip_path, 'rb'),
                    as_attachment=True,
                    filename=os.path.basename(zip_path)
                )
                # Clean up the temporary zip file after sending
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