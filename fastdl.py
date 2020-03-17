import bz2
import os
from shutil import copyfileobj, copyfile
from sys import argv
from time import time


gameRootFolder = "./csgo"
fastdlRootFolder = "./www/fastdl"

gameFolders = [
	("maps", [".bsp", ".nav"]),
	("materials", [".vmt", ".vtf", ".raw"]),
	("models", [".mdl", ".vtx", ".vvd", ".phy"]),
	("particles", [".pcf"]),
	("sound", [".mp3", ".wav"])
]

ETCconstant = 9.5e-08
TotalFilesUpdated = 0
TotalFilesChanged = 0
TotalFilesRemoved = 0
IsFullCheck = False
cmpReadSize = 128000


def bz2Compress(rootfile, fdfile):
	print("Compressing {}, ETC: {:.2f} seconds...".format(rootfile, os.path.getsize(rootfile) * ETCconstant))
	with open(rootfile, "rb") as inp, bz2.BZ2File(fdfile, "wb", compresslevel = 1) as out:
		copyfileobj(inp, out)


def filesEqual(rootfile, fdfile, bz2format = False):
	prevtime = time()
	if bz2format:
		with open(rootfile, "rb") as inp, bz2.BZ2File(fdfile, "rb") as out:
			while True:
				p1 = inp.read(cmpReadSize)
				p2 = out.read(cmpReadSize)
				if p1 != p2:
					print("BZ2 File {} compared for {:.2f} seconds".format(rootfile, time() - prevtime))
					return False
				if not p1:
					print("BZ2 File {} compared for {:.2f} seconds".format(rootfile, time() - prevtime))
					return True
	else:
		with open(rootfile, "rb") as inp, open(fdfile, "rb") as out:
			while True:
				p1 = inp.read(cmpReadSize)
				p2 = out.read(cmpReadSize)
				if p1 != p2:
					print("File {} compared for {:.2f} seconds".format(rootfile, time() - prevtime))
					return False
				if not p1:
					print("File {} compared for {:.2f} seconds".format(rootfile, time() - prevtime))
					return True


def addToFastdl(rootfile, fdfile, copy = False):
	global TotalFilesUpdated, TotalFilesChanged, TotalFilesRemoved
	if not os.path.exists(fdfile):
		TotalFilesUpdated += 1
		print("Adding {} to fastdl...".format(rootfile))
		if copy:
			copyfile(rootfile, fdfile)
		else:
			bz2Compress(rootfile, fdfile)
	elif IsFullCheck:
		if copy:
			if os.path.getsize(fdfile) != os.path.getsize(rootfile) or not filesEqual(rootfile, fdfile):
				TotalFilesChanged += 1
				print("Found changed file {}, replacing...".format(rootfile))
				copyfile(rootfile, fdfile)
		else:
			if not filesEqual(rootfile, fdfile, True):
				TotalFilesChanged += 1
				print("Found changed file {}, replacing...".format(rootfile))
				bz2Compress(rootfile, fdfile)


def main():
	global TotalFilesUpdated, TotalFilesChanged, TotalFilesRemoved

	if not os.path.exists(gameRootFolder):
		print("Game root folder wasn't found!")
		return
	if not os.path.exists(fastdlRootFolder):
		print("Fastdl folder wasn't found!")
		return

	timestart = time()
	try:
		for expfolder, exts in gameFolders:
			for dirpath, dirnames, filenames in os.walk(os.path.join(gameRootFolder, expfolder)):
				for file in filenames:
					if os.path.splitext(file)[1] in exts:
						fulldir = os.path.join(fastdlRootFolder, os.path.relpath(dirpath, gameRootFolder))
						if not os.path.exists(fulldir):
							print("Directory {} wasn't found on fastdl path, creating...".format(fulldir))
							os.makedirs(fulldir)

						rootfile = os.path.join(dirpath, file)
						#special case for files bigger then 150mb
						if os.path.getsize(rootfile) < (150 * 1024 * 1024):
							addToFastdl(rootfile, os.path.join(fulldir, "{}.bz2".format(file)))
						else:
							addToFastdl(rootfile, os.path.join(fulldir, file), True)

			for dirpath, dirnames, filenames in os.walk(os.path.join(fastdlRootFolder, expfolder)):
				for file in filenames:
					if os.path.splitext(file)[1] == ".bz2":
						filename = os.path.splitext(file)[0]
					else:
						filename = file

					if not os.path.exists(os.path.join(gameRootFolder, os.path.relpath(dirpath, fastdlRootFolder), filename)):
						TotalFilesRemoved += 1
						print("Found removed file {}, deleting...".format(os.path.join(gameRootFolder, os.path.relpath(dirpath, fastdlRootFolder), filename)))
						os.remove(os.path.join(dirpath, file))

			for dirpath, dirnames, filenames in os.walk(os.path.join(fastdlRootFolder, expfolder), topdown = False):
				if not os.listdir(dirpath):
					print("Found empty directory {} on fastdl, removing...".format(dirpath))
					os.rmdir(dirpath)
	except Exception as e:
		print(e)

	print("Fastdl was updated successfully. (Took {:.2f} seconds to complete)".format(time() - timestart))
	print("Was added {} entries.".format(TotalFilesUpdated))
	print("Was changed {} entries.".format(TotalFilesChanged))
	print("Was removed {} entries.".format(TotalFilesRemoved))


if __name__ == "__main__":
	if len(argv) >= 2 and argv[1] == "full":
		IsFullCheck = True
	main()
