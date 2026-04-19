from PIL import Image
import numpy as np
import argparse
import matplotlib.pyplot as plt
import os
import pickle

info = "n18img-gen3d - генерирует 3d проекцию фото"
cavc = True
trace = True

def array_img(for3d):
	array3d = np.array(for3d)
	return array3d

def start_module(argt, pipe=False):
	args = argt.split(" ")[1:]
	pars = argparse.ArgumentParser()
	pars.add_argument("-f", "--file", help="указывает файл для работы программы", type=str)
	pars.add_argument("-o", "--output", help="указывает выходной файл")
	pars.add_argument("-c", "--color", default="black", type=str)
	pars.add_argument("-ext", "--extension", type=str, default="png", help="указывает расширение выходного файла")
	pars.add_argument("-r", "--raw", action="store_true", help='возвращает pickle файл с которым можно работать позже вместо фоток')
	pars.add_argument("-s", "--size", type=int, nargs=2, help="указывает размер фото")
	pars.add_argument("-d", "--dpi", type=int, default=300, help="указывает качество исходного фото")
	pars.add_argument("-ps", "--point-size", type=float, default=4, help="указывает размер точек")
	try:
		arg = pars.parse_args(args)
	except SystemExit:
		return
	except Exception as exc:
		raise Exception(exc)
	if not arg.file:
		print("файл для работы не обнаружен")
		return
	if not arg.output:
		output = arg.file + "." + "img3d"
	else:
		output = arg.output
	img = Image.open(arg.file)
	img = img.convert("RGB")
	ys = []
	xs = []
	zs = []
	color = []
	ki = 0
	for i, val1 in enumerate(array_img(img)):
		ki += 1
		for u, val2 in enumerate(val1):
			y = i + 1
			x = u + 1
			clr1, clr2, clr3 = val2
			xs.append(x)
			ys.append(y)
			z = int(int(clr1) + int(clr2) + int(clr3))
			zs.append(z)
			col = (clr1/255, clr2/255, clr3/255)
			color.append(col)
		if ki % 10 == 0:
			print("row ", ki, " is finished")
	if not arg.size:
		fig = plt.figure(figsize=(18, 8))
	else:
		fig = plt.figure(figsize=(arg.size[0], arg.size[1]))
	ax = fig.add_subplot(111, projection="3d")
	ax.scatter(xs, zs, ys, c=color, marker="s", s=arg.point_size, rasterized=None, edgecolors="none")
	ax.invert_zaxis()
	ax.set_facecolor(arg.color)
	ax.set_title(f'3d {arg.file}')
	if not arg.raw:
		output = output + "." + arg.extension
		plt.savefig(output, dpi=arg.dpi)
		ax.view_init(azim=-90, elev=0)
		plt.savefig(output[:output.rfind(".")] + ".fwd" + "." + arg.extension, dpi=arg.dpi)
		plt.close(fig)
		fn = output[:output.rfind(".")]
		fvn = output[:output.rfind(".")] + ".fwd" + "." + arg.extension
		fvn = fvn[:fvn.rfind(".")]
		os.rename(output[:output.rfind(".")] + ".fwd" + "." + arg.extension, fvn)
		os.rename(output, fn)
		print("saved: ", fn, fvn)
	else:
		with open(output, "wb") as wbwrite:
			pickle.dump(fig, wbwrite)
