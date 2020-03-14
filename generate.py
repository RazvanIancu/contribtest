# generate site from static pages, loosely inspired by Jekyll
# run like this:
#   ./generate.py test/source output
# the generated `output` should be the same as `test/expected_output`

import os
import logging
import jinja2
import sys
import json

log = logging.getLogger(__name__)

'''
	Function that lists all the .rst files from the folder_path.
'''
def list_files(folder_path):

	for name in os.listdir(folder_path):

		# Splitting the base and the extension
		base, ext = os.path.splitext(name)

		# We want to keep just the ".rst"
		if ext != '.rst':
			continue

		yield os.path.join(folder_path, name)

'''
	Reads the content of file_path and extract the data
	from the json and the content.
'''
def read_file(file_path):
	f = open(file_path, 'r')
	raw_metadata = ""
	
	for line in f:
			# Comparing line without spaces with ---
		if line.strip() == '---':
			if raw_metadata:
				# Loading the json from the metadata
				jsondata = json.loads(raw_metadata)
			else:
				jsondata = None
			break
		raw_metadata += line

	content = ""
		
	for line in f:
		content += line
	
	content = content.strip()
	
	f.close()
	return jsondata, content

'''
	Write the html to the output_file.
'''
def write_output(output_file, html):
	with open(output_file, "w") as f:
		f.write(html)

'''
	Checks if the output folder does exist if not
	the function creates it.
'''
def generate_folder(name):
	if not os.path.exists(name):
		try:
			os.makedirs(name)
		except:
			print('Can not create output folder')
			sys.exit()

'''
	Generating the output file using jinja2.
	Reading all the .rst, extracting the template name,
	loading the template using jinja_env, rendering it
	and creating the .html file.
'''
def generate_site(input_folder, output_folder):
	log.info("Generating site from %r", input_folder)
	
	jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(input_folder + 'layout'),
		trim_blocks=True, lstrip_blocks=True)

	# For each ".rst"
	for file_path in list_files(input_folder):
		
		metadata, content = read_file(file_path)
		
		if metadata is None:
			continue
		
		# Extract the template name from metadata layout
		template_name = metadata['layout']

		# Load the template
		template = jinja_env.get_template(template_name)

		data = dict(metadata, content=content)
	
		# Rendering the date using the template
		html = template.render(data)

		# Creating the new file .html
		file_name = os.path.basename(file_path)
		new_file, old_ext = os.path.splitext(file_name)
		file = os.path.join(output_folder, new_file + ".html")
		
		write_output(file, html)
		log.info("Writing %r with template %r", new_file, template_name)

'''
	Generating the output folder in case it does not exist
	and calling the function that generate the site.
'''
def main(input_folder, output_folder):
	generate_folder(output_folder)
	generate_site(input_folder, output_folder)

'''
	Calling the main function and checking the command line
	parameters.
'''
if __name__ == '__main__':
	logging.basicConfig()
	
	if len(sys.argv) != 3:
		print("Invalid use of command. Example: ./generate.py test/source/ output ")
		sys.exit()

	main(sys.argv[1], sys.argv[2])
