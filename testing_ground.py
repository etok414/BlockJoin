import os


def main():
    base_folder = os.path.dirname(__file__)
    folder = 'graphics'
    path = os.path.join(base_folder, folder)
    filelist = os.listdir(path)

    for item in filelist:
        if item[-4:].lower() == '.png':
            print(item[:-4])


if __name__ == '__main__':
    main()
