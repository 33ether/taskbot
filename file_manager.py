import os
import time

class FileManager:
    def __init__(self,base_dir):
        """Initialize the base directory from where to work"""
        self.base_dir = base_dir
        self.ensure_dir(self.base_dir)

    def ensure_dir(self, path):
        """See if dir exits and create dir if not"""
        if not os.path.exists(path):
            os.mkdir(path)

    #dirs is a tuple containg the path in terms of subdirs like path1/path2 will be in path1,path2
    def add_file(self,content,*dirs):
        """Add file to a dirs"""
        path = self.base_dir
        if len(dirs) > 0:
            parent_dir = self.base_dir
            for dir in dirs:
                path = os.path.join(parent_dir,dir)
                self.ensure_dir(path)
                parent_dir = path
        file_path = os.path.join(path, f"{time.time()}")
        with open(file_path,'w') as file:
            file.write(content)

    def list_files(self,*dirs):
        """List dirs/files in dirs path""" 
        path = self.make_path(*dirs)
        if os.path.exists(path):
            return sorted(os.listdir(path))
        else:
            return []

    def read_file(self,filename,*dirs):
        """Read the file contents"""
        path = self.make_path(*dirs)
        file_path = os.path.join(path,filename)
        if os.path.exists(file_path):
            with open(file_path,'r') as file:
                return file.read()

    def del_file(self,filename,*dirs):
       """Delete a file"""
       path = self.make_path(*dirs)
       file_path = os.path.join(path,filename)
       if os.path.exists(file_path):
           os.remove(file_path)

    def make_path(self,*dirs):
        """Make os module compatible path"""

        path = self.base_dir
        if len(dirs) > 0:
            parent_dir = self.base_dir
            for dir in dirs:
                path = os.path.join(parent_dir,dir)
                parent_dir = path
            
        return path





