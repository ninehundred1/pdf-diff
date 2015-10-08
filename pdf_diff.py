from subprocess import Popen, call
from PIL import ImageChops, Image


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
		'sOutputFile={} {}'.format(new_filename, filename)])

diff = ImageChops.add(Image.open(image1), Image.open(image2))
diff.save('diff.png')