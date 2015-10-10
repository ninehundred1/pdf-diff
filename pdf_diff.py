from subprocess import Popen, call
from PIL import ImageChops, Image
import os
import date

file1 = 'KIPP_Austin_Public_Schools.pdf'
file2 = 'KIPPAustinPublicSchools_4-3.pdf'

image1 = 'KIPP_Austin_Public_Schools.png'
image2 = 'KIPPAustinPublicSchools_4-3.png'


def format_gs_command(filename):
	new_filename = 'stuff' # filename.replace('.pdf', '')
	return call([
		'gswin64c',
		'-sDEVICE=png16m',
		'-r300',
		'sOutputFile={}'.format(new_filename),
		filename])

if __name__ == '__main__':
	daily_directory = r'\\sneetch\AISWorkspace\pipelines\essential questions\report card\2015-16 report card\output\\' + date.today().strftime('%m-%d-%Y')
	master_directory = r'\\sneetch\AISWorkspace\pipelines\essential questions\report card\2015-16 report card\output\master'

	output_directory = daily_directory + '\diffs'

	os.chdir(daily_directory)
	file_list = os.listdir()

	for file ine file_list:
		master_file = master_directory + '\\' + file
		diff = ImageChops.add(file, master_file))
		diff.save(output_directory + 'diff.png')