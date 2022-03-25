#!/usr/bin/env python
# coding: utf-8

# In[5]:


get_ipython().system('pip install plyfile')


# In[6]:


import os
from os import listdir
from os.path import isfile, join
from argparse import ArgumentParser
from plyfile import PlyData


# In[8]:


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('ply_path')
    parser.add_argument('--obj_path', default=None, required=False)

    args = parser.parse_args()
    return args.ply_path, args.obj_path


# In[9]:


def ply_path_to_obj_path(ply_path):
    return os.path.splitext(ply_path)[0] + '.obj'


# In[11]:


def convert(ply_path, obj_path=None):

    # Converts the given .ply file to an .obj file

    obj_path = obj_path or ply_path_to_obj_path(ply_path)
    ply = PlyData.read(ply_path)
    with open(obj_path, 'w') as f:
        f.write("# OBJ file\n")

        verteces = ply['vertex']

        for v in verteces:
            p = [v['x'], v['y'], v['z']]
            if 'red' in v and 'green' in v and 'blue' in v:
                c = [v['red'] / 256, v['green'] / 256, v['blue'] / 256]
            else:
                c = [0, 0, 0]
            a = p + c
            f.write("v %.6f %.6f %.6f %.6f %.6f %.6f \n" % tuple(a))

        for v in verteces:
            if 'nx' in v and 'ny' in v and 'nz' in v:
                n = (v['nx'], v['ny'], v['nz'])
                f.write("vn %.6f %.6f %.6f\n" % n)

        for v in verteces:
            if 's' in v and 't' in v:
                t = (v['s'], v['t'])
                f.write("vt %.6f %.6f\n" % t)

        if 'face' in ply:
            for i in ply['face']['vertex_indices']:
                f.write("f")
                for j in range(i.size):
                    # ii = [ i[j]+1 ]
                    ii = [i[j] + 1, i[j] + 1, i[j] + 1]
                    # f.write(" %d" % tuple(ii) )
                    f.write(" %d/%d/%d" % tuple(ii))
                f.write("\n")


# In[13]:


# For a Single File

def main():
    ply_path = "D:/point_cloud/4/4-1.ply"
    
    if ".ply" in ply_path:
        obj_path = ply_path_to_obj_path(ply_path)
        print("Converting %s to .obj..." % ply_path)
        convert(ply_path, obj_path)
        print("Conversion finished successfully. Output path: %s" % obj_path)
    else:
        if not "/" in ply_path:
            ply_path = ply_path + "/"
        files = [f for f in listdir(ply_path) if isfile(join(ply_path, f))]
        for f in files:
            if ".ply" in f:
                print("Converting %s to .obj..." % f)
                f = ply_path + f
                obj_path = ply_path_to_obj_path(f)
                convert(f, obj_path)
                print("Conversion finished successfully. Output path: %s" % obj_path)

if __name__ == '__main__':
    main()


# In[19]:


# For the point_cloud File


def main():
    path = "D:/point_cloud"     #Input Path
    out_path = "D:/Obj Files"   #Output Path
    
    for files in os.listdir(path):
        for content in os.listdir(path + "/" + files):
            ply_path = path + "/" + files + "/" + content
            if ".ply" in ply_path:
                obj_path = ply_path_to_obj_path(ply_path)
                #os.mkdir("D:/Obj Files/files")
                #obj_path = out_path + "/" + files + "/"
                print("Converting %s to .obj..." % ply_path)
                convert(ply_path, obj_path)
                print("Conversion finished successfully. Output path: %s" % obj_path)
            
if __name__ == '__main__':
    main()
    
# Execution Killed


# In[ ]:




