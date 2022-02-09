import subprocess
from os import listdir
import promptlib
from word_cloud_generator import WordCloudCreator


workdir = promptlib.Files().dir()

input_files = listdir(workdir)
input_files = filter(lambda current: type(current) is str and str(current).endswith('.json'), input_files)
cloud_creator = WordCloudCreator(image_width=1170, image_height=2532)

for filename in input_files:
    cloud_creator.run(workdir, filename)
subprocess.Popen(f'explorer "{workdir}"')

