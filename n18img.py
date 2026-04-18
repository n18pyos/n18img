import numpy as np
from PIL import Image
import argparse
import random
import os

cavc = True
trace = True
info = "n18-img - программа для разнообразной работы с изображениями"

def array_img(img_for_array):
	array_img = np.array(img_for_array)
	return array_img

def start_module(args, pipe=False):
	argt = args.split(" ")[1:]
	pars = argparse.ArgumentParser()
	pars.add_argument("-f", "--file", help="указывает файл для работы")
	pars.add_argument("-o", "--output", help="указывает выходной файл")
	pars.add_argument("-rp", "--raw-print", help="выводит сырые пиксели изображения", action="store_true")
	pars.add_argument("-rm", "--random-merge", help="добавляет рандомное смешивание", type=str, nargs=3)
	pars.add_argument("-ii", "--image-info", help="выводит информацию о системе", action="store_true")
	pars.add_argument("-pp", "--python-portable", action="store_true")
	pars.add_argument("-s", "--show", help="открывает изображение", action="store_true")
	pars.add_argument("-ext", "--extension", type=str, default="png", help="указывает расширение файла")
	try:
		arg = pars.parse_args(argt)
	except SystemExit:
		return
	except Exception as exc:
		raise Exception(exc)
	if not arg.file and not pipe:
		print("введите файл для работы\n")
		raise Exception ("file for work is None")
	elif not arg.file and pipe:
		temp_file = pipe.split("\n")
		tmp = ""
		for i in temp_file:
			tmp = tmp + i + "\n"
		arg.file = tmp
	img = Image.open(arg.file)
	if arg.output:
		output = arg.output
	else:
		output = arg.file + ".n18img"
	if arg.raw_print:
		for i in array_img(img):
			for _i in i:
				print(" ".join(str(i_) for i_ in _i))
	if arg.image_info:
		print(f"формат: {img.format}")
		print(f"размер: {img.size}")
		print(f"режим: {img.mode}")
		print(f"размер массива: {array_img(img).shape}")
	if arg.python_portable:
		with open(output, "w") as ppwriter:
			with open(arg.file, "rb") as ppreader:
				text_for_pp = ppreader.read()
			_file = arg.file[:arg.file.rfind(".")]
			ppwriter.write("import argparse\n")
			ppwriter.write("text = ")
			ppwriter.write(repr(text_for_pp) + "\n")
			ppwriter.write("pars = argparse.ArgumentParser()\npars.add_argument('-o', '--output', help='указывает выходной файл')\narg = pars.parse_args()\nif not arg.output:\n	arg.output = ")
			ppwriter.write(f"{repr(_file)}" + "\n")
			ppwriter.write("with open(arg.output, 'wb') as outwriter:\n	outwriter.write(text)")
	if arg.random_merge:
		try:
			os.remove(output)
		except:
			pass
		if arg.random_merge[0] == "random" and arg.random_merge[1] == "random":
			smesh = random.randint(30, 70)
		else:
			smesh = random.randint(int(arg.random_merge[0]), int(arg.random_merge[1]))
		kimg = array_img(img)
		for u, val1 in enumerate(kimg):
			for o, val2 in enumerate(val1):
				for j, val3 in enumerate(val2):
					if int(val3) + smesh > 255:
						if str(arg.random_merge[2]).lower() == "true":
							kimg[u][o][j] = int(kimg[u][o][j])-int(kimg[u][o][j])/2
						elif int(val3) - smesh < 0:
							kimg[u][o][j] = int(val3) - 255/2**2
						else:
							kimg[u][o][j] = int(val3) - smesh
					else:
						kimg[u][o][j] = int(val3) + smesh
			print("row ", u, " is finished")
		fimg = Image.fromarray(kimg)
		if arg.output:
			output = arg.output + "." + arg.extension
		else:
			output = arg.file + "." + arg.extension
		fimg.save(output)
		if not arg.output:
			fn = output[:output.rfind(".")]
			fn = fn + ".n18img"
		else:
			fn = output[:output.rfind(".")]
		os.rename(output, fn)
	if arg.show:
		img.show()
