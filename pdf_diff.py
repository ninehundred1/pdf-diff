__author__ = 'Will Wagner'

import os
from datetime import date
from subprocess import call
from PIL import ImageChops, Image
import shutil

def get_unpadded_date():
    """
    Get the date in YYYY_M_D format to match what the excel macro creates for folder names
    """

    day = date.today().strftime('%d')
    month = date.today().strftime('%m')
    year = date.today().strftime('%Y')

    day = day.lstrip("0")
    month = month.lstrip("0")

    return year + '_' + month + '_' + day


class PDFDirectory(object):

    def __init__(self, subfolder, daily_directory=None, most_recent_directory=None, date=get_unpadded_date()):
        """
        A base class for directories of PDFs that will be diffed
        :subfolder: the subfolder name where images are stored in both the daily and most recent directories
        """

        self.date = date
        self.subfolder = subfolder
        self.date_folder = '\\' + self.date + '_Drafts'
        self.daily_directory = daily_directory + self.subfolder + self.date_folder
        self.most_recent_directory = most_recent_directory + self.subfolder + r'\1 Most Recent'

        self.most_recent_images = {}
        self.daily_images = {}
        
        # the image directories are subdirectories of the two directories to be diffed, and they store files so we don't have to regenerate them
        self.most_recent_image_directory = self.most_recent_directory + r'\images'
        self.daily_image_directory = self.daily_directory + r'\images'

        self.diffs_directory = self.daily_directory + r'\diffs'

        self.create_process_folders()

    def create_process_folders(self):
        """ Ensure the folders required to create images and diffs exist, create any missing folder"""

        try:
            os.chdir(self.most_recent_image_directory)
        except WindowsError:
            os.mkdir(self.most_recent_image_directory)

        try:
            os.chdir(self.daily_image_directory)
        except WindowsError:
            os.mkdir(self.daily_image_directory)

        try:
            os.chdir(self.diffs_directory)
        except WindowsError:
            os.mkdir(self.diffs_directory)


    def generate_flat_image(self, filename):
        """ Call Ghostscript to flatten PDF into image"""

        new_filename = filename.replace('.pdf', '.png')

        # call the command 'gswin64c -sDEVICE=png16m -dNOPAUSE -dBATCH -r300 sOutputFile=NEW_FILENAME' 'FILENAME'
        return call([
            'gswin64c',
            '-sDEVICE=png16m',
            '-dNOPAUSE',
            '-dBATCH',
            '-r300',
            '-sOutputFile=images\{}'.format(new_filename),
            filename,
            '-c quit'])

    @staticmethod
    def get_school_name(name):
        """ Isolate school name from other filename elements """
        start = name.find('KIPP_')
        if start == -1:
            start = name.find('KIPP')
        end = name.rfind('_')

        return name[start:end]


    def populate_image_directories(self):
        """ Generate the images from the PDFs"""

        # create dict with formatted names for comparison and actual filename for the imaging operation
        daily_files = {self.get_school_name(filename):filename for filename in os.listdir(self.daily_directory) if '.pdf' in filename}
        daily_images = {self.get_school_name(filename):filename for filename in os.listdir(self.daily_image_directory) if '.png' in filename}

        print(daily_files)
        print(daily_images)

        most_recent_files = {self.get_school_name(filename):filename for filename in os.listdir(self.most_recent_directory) if '.pdf' in filename}
        most_recent_images = {self.get_school_name(filename):filename for filename in os.listdir(self.most_recent_image_directory) if '.png' in filename}

        # generate daily file images
        os.chdir(self.daily_directory)
        for file in daily_files:
            if file not in daily_images:
                filename = daily_files[file]
                self.generate_flat_image(filename)

        # generate master file images
        os.chdir(self.most_recent_directory)
        for file in most_recent_files:
            if file not in most_recent_images:
                self.generate_flat_image(most_recent_files[file])


    def diff_directories(self):
        # get current list of images in most recent and daily directories
        daily_images = {self.get_school_name(filename):filename for filename in os.listdir(self.daily_image_directory) if '.png' in filename}
        most_recent_images = {self.get_school_name(filename):filename for filename in os.listdir(self.most_recent_image_directory) if '.png' in filename}


        for file in daily_images:
            daily_file = Image.open(self.daily_image_directory + '\\' + daily_images[file])
            most_recent_file = Image.open(self.most_recent_image_directory + '\\' + most_recent_images[file])
            try:
                diff = ImageChops.difference(daily_file, most_recent_file)
            except AttributeError as e:
                print("Error diffing image:", e)
                print(daily_file)
                print(most_recent_file)
                exit()
            # if the page isn't blank
            if diff.getbbox() != None:
                diff = ImageChops.invert(diff)
                diff.save(self.diffs_directory + '\\' + file + '.png', format="png")
            print("Diffed", file)

if __name__ == '__main__':

    # schools = PDFDirectory(subfolder=r'\School Pages', 
    #     daily_directory=r'\\sneetch\AISWorkspace\Pipelines\Essential Questions\Report Card\2015-16 RC Project\Output',
    #     most_recent_directory=r'\\sneetch\AISWorkspace\Pipelines\Essential Questions\Report Card\2015-16 RC Project\Output')
    # schools.populate_image_directories()
    # schools.diff_directories()

    regions = PDFDirectory(subfolder=r'\Region Pages', daily_directory=r'\\sneetch\AISWorkspace\Pipelines\Essential Questions\Report Card\2015-16 RC Project\Output',
        most_recent_directory=r'\\sneetch\AISWorkspace\Pipelines\Essential Questions\Report Card\2015-16 RC Project\Output')
    regions.populate_image_directories()
    regions.diff_directories()