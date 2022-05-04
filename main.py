# bibliotecas necesárias são pims, jpype1 e dar run uma vez no comando pims.bioformats.download_jar(version='6.5')


# todo: ver a unidade de medida do pixelm size
# todo: melhorar a leitura e armazenamento sequencial de .zvi's
# todo: acessar a metadata em ReaderSequence
import os
import shutil

import pims
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import imageio


def readConvertZVIFile(origin_folder, destination_folder):
    columns = ["imgFileName", "PlaneExposureTime", "PixelsPhysicalSizeX", "PixelsPhysicalSizeY"]
    zviDataFrame = pd.DataFrame(columns=columns)
    if not os.path.isdir(destination_folder):
        os.mkdir(destination_folder)

    cont = 1
    for File in os.listdir(origin_folder):
        fileName = f'{os.path.basename(File)}_filtered.png'
        read = pims.bioformats.BioformatsReader(f'{origin_folder}/{File}', meta=True)
        meta = read.metadata
        readConverted = (read[0] * 255 / read[0].max()).clip(0, 255).astype(np.uint8)
        zviDataFrame.loc[cont - 1] = [fileName,
                                      meta.PlaneExposureTime(0, 0),
                                      meta.PixelsPhysicalSizeX(0),
                                      meta.PixelsPhysicalSizeY(0)]
        cv2.imwrite(fileName, readConverted)
        # Overwrite files if they already exist in destination folder
        if os.path.exists(f"{destination_folder}/{fileName}"):
            os.remove(f"{destination_folder}/{fileName}")
        # Move files to destination folder
        shutil.move(f"./{fileName}", f"{destination_folder}")
        plt.imshow(readConverted)
        plt.show()
        cont += 1
    zviDataFrame.to_excel('./dataframe.xlsx')
    zviDataFrame.to_csv('./dataframe.csv')


if __name__ == '__main__':
    readConvertZVIFile("./vziFiles", "./ /Filtered water on oil")
    readConvertZVIFile("./vziFiles", "./ /Filtered oil on water")
