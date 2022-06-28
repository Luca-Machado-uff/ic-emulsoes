# bibliotecas necesárias são pims, jpype1 e dar run uma vez no comando pims.bioformats.download_jar(version='6.5')


import os
import shutil
import pims
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2


# todo ver a biblitoeca kornea

def install_jar_file():
    pims.bioformats.download_jar(version='6.5')


def read_convert_zvi_file(origin_folder, destination_folder, dataFrameName):
    columns = ["imgFileName", "PlaneExposureTime", "PixelsPhysicalSizeX", "PixelsPhysicalSizeY", ]
    zviDataFrame = pd.DataFrame(columns=columns)
    if not os.path.isdir(destination_folder):
        os.mkdir(destination_folder)

    cont = 0
    # max = 0
    # todo: ver .sys "regex"
    for File in os.listdir(origin_folder):
        if File.endswith(".xlsx"):
            range_values = pd.read_excel(f'{origin_folder}/{File}')
            print(range_values.iloc[2, 0])
        if File.endswith(".zvi"):
            fileName = f'{os.path.basename(File)}.png'
            read = pims.bioformats.BioformatsReader(f'{origin_folder}/{File}', meta=True)
            meta = read.metadata
            img = read[0]
            lower = img.min()
            upper = img.max()
            # todo salvar com max e min do arquivo original no dataframe, bem como metadatos
            readConverted = ((img - lower) / (upper - lower) * 255).clip(0, 255).astype(np.uint8)
            zviDataFrame.loc[cont] = "-"
            zviDataFrame.iloc[cont, 0:4] = [fileName,
                                          meta.PlaneExposureTime(0, 0),
                                          meta.PixelsPhysicalSizeX(0),
                                          meta.PixelsPhysicalSizeY(0)]
            for i in range(2, (len(range_values.index))):
                zviDataFrame.loc[cont, str(range_values.iloc[i, 0])] = range_values.iloc[i, 1]
            cv2.imwrite(fileName, readConverted)
            # Overwrite files if they already exist in destination folder
            if os.path.exists(f"{destination_folder}/{fileName}"):
                os.remove(f"{destination_folder}/{fileName}")
            # Move files to destination folder
            shutil.move(f"./{fileName}", f"{destination_folder}")
            plt.imshow(readConverted)
            plt.show()
            cont += 1
            print(f"máximo: {read[0].max()} Mínimo:{read[0].min()} file:{fileName}")
    zviDataFrame.to_excel(f'./{destination_folder}/{dataFrameName}.xlsx')
    zviDataFrame.to_csv(f'./{destination_folder}/{dataFrameName}.csv')

def test():
    df = pd.read_excel("/home/luca/PycharmProjects/pythonProject/Filtered water on oil/óleo em água.xlsx")
    print(df.iloc[:, 5:])



if __name__ == '__main__':
   # read_convert_zvi_file("/home/luca/Desktop/Uff/IC/Emulsões água em óleo", "./Filtered water on oil", "óleo em água")
   # read_convert_zvi_file("/home/luca/Desktop/Uff/IC/Emulsões óleo em água", "./Filtered oil on water", "água em óleo")
   test()