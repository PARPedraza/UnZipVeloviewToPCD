#install:
# pip install pypcd
# pip3 install --upgrade git+https://github.com/klintan/pypcd.git
# pip install pprint

# -*- coding: utf-8 -*-
# @package Unzip Files ZIP, Choices Cloud Points CSV, Convert (CSV) to Point Cloud Data (PCD)
# Web Page
# https://github.com/PARPedraza/UnZipVeloviewToPCD.git
# autors: Alfonso Ramírez-Pedraza and José-Joel González-Barbosa

"""
Example:
        $ python Veloview-PCD.py -Process
"""

import pandas as pd
import getopt,os,sys,csv,numpy as np
from pypcd import pypcd
import pprint,zipfile

class VeloviewPCD(object):

    def __init__(self,dir):
        """The constructor Initialize Sentinel Data.
        Args:
            self: The object pointer.
            dir (str): destination directory.
        Returns:
            pointer: The object pointer.
        """
        self.dir=dir
        self.aux = "Aux"
        self.exCSV=".csv"
        self.exZIP=".zip"
        self.exPCD=".pcd"
        self.label1 = "50).csv"
        self.label2 = "05).csv"
        self.label3 = "00).csv"
        self.folder="/FilesPCD"
        self.output = "/output"
        self.FilesOutput = self.dir + self.output
        self.FilesPCD = self.FilesOutput + self.folder

        self.nombreArch="/output"
        #self.root = self.dir + self.folder
        self.NewFolder=self.dir+self.nombreArch

    def readCSV(self, file):
        """Read files cloud points csv.
        Args:
            self: The object pointer.
            file (str): path to files cloud points (csv).
        Returns:
            cloud (str): cloud points (x,y,z,d).
        """
        data = pd.read_csv(file)
        cloud = np.array(data)
        return cloud

    def readPCD(self,file):
        # Lee archivos PCD
        cloud = pypcd.PointCloud.from_path(file)
        pprint.pprint(cloud.get_metadata())
        print(cloud.pc_data)
        return cloud

    def Validate(self, dirFolder):
        """Create folder to save object segmentation.
        Args:
            self: The object pointer.
            dirFolder (str): path and name folder to save object segmentation.
        """
        try:
            os.stat(dirFolder)
        except:
            os.mkdir(dirFolder)

    def findFiles(self,flag,path):
        """Find Files csv or pcd.
        Args:
            self: The object pointer.
            flag (str): process number.
        Returns:
            list_files (str): list files cloud points founded.
        """
        if(flag==1):
            list_files = [f for f in os.listdir(self.dir) if f.endswith(self.exZIP)]
        if(flag==2):
            list_files = [f.path for f in os.scandir(self.NewFolder) if f.is_dir()]
        if(flag==3):
            list_files = [f for f in os.listdir(path) if f.endswith(self.exCSV)]
        return list_files

    def writeData(self, data, name):
        """Write objects.
        Args:
            self: The object pointer.
            noObj (str): number object segmented
            root (str): path and name folder to save object segmentation.
        """
        with open(name, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)

    def writePCD(self,file, cloud):
        """Write Files PCD.
        Args:
            self: The object pointer.
            file (str): name file.
            cloud (array): data cloud point.
        Returns:
            clouds (str): save cloud points founded.
        """
        X = cloud[:, 0]
        Y = cloud[:, 1]
        Z = cloud[:, 2]
        data = np.column_stack((X, Y, Z))
        # Use the pypcd utility function to create a new point cloud from ndarray
        new_cloud = pypcd.make_xyz_point_cloud(data)
        # Store the cloud uncompressed
        fileName = file[:-4] + self.exPCD
        new_cloud.save_pcd(fileName)

    def iniParam(self):
        """Choose process
        Args:
            self: The object pointer.
            flag (str): process number.
        Return:
            files: point cloud PCD
        """
        # Find Files ZIP
        list_Files = Point.findFiles(1,self.aux)
        print("Save PCD Files...")
        #Create Folder save output data and output data PCD
        Point.Validate(self.FilesOutput)
        Point.Validate(self.FilesPCD)
        # UNZIP Files
        for file in list_Files:
            fileroot = self.dir + "/" + file
            ##UnZip Files Funtion
            Point.UnZip(fileroot)
            createFolder=self.FilesOutput+"/"+file[:-4]
            Point.Validate(createFolder)
            #Search Files and copy interes files
            list_FilesCSV = Point.findFiles(3,fileroot[:-4])
            for dat in list_FilesCSV:
                Val1 = dat.find(self.label1)
                Val2 = dat.find(self.label2)
                Val3 = dat.find(self.label3)
                if(Val1>0)or(Val2>0)or(Val3>0):
                    into=fileroot[:-4] +"/" +dat
                    DataCloud = Point.readCSV(into)
                    #Archivo para guardar
                    out=createFolder+"/"+dat
                    self.writeData(DataCloud, out)

        #Save files point cloud data PCD
        for Files in list_Files:
            root_Files = self.FilesOutput+"/"+Files[:-4]
            list_Clouds = Point.findFiles(3, root_Files)
            CreateFolder = self.FilesOutput+self.folder+"/"+Files[:-4]
            Point.Validate(CreateFolder)
            for files in list_Clouds:
                root_Clouds = root_Files + "/" + files
                DataCloud = Point.readCSV(root_Clouds)
                SaveFiles = CreateFolder + "/" + files
                Point.writePCD(SaveFiles, DataCloud)

    def UnZip(self,root_file):
        """Unzip
        Args:
            self: The object pointer.
            root_file (str): path file unzip
        Return:
            folder: point clouds unzip
        """
        with zipfile.ZipFile(root_file, 'r') as zip_ref:
            zip_ref.extractall(self.dir)

    def usage(self):
        print(" Opcions:")
        print("--help (-h)")
        print("-c \t<PathFiles csv>\t <Choices and Convert cloud points csv to pcd>")
        sys.exit()

    def main(self, argv):
        try:
            opts, args = getopt.getopt(argv, "cph", ["Path="])
        except getopt.GetoptError:
            Point.usage()
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                Point.usage()
            elif opt in ("-c", "--Path"):
                Point.iniParam()
            else:
                Point.usage()

if __name__ == "__main__":
    # Variables Input
    dir = os.path.dirname(os.path.abspath(__file__))
    Point = VeloviewPCD(dir)
    Point.main(sys.argv[1:])