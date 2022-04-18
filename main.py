#bibliotecas necesárias são pims, jpype1 e dar run uma vez no comando pims.bioformats.download_jar(version='6.5')


#todo: ver a unidade de medida do pixelm size
#todo: melhorar a leitura e armazenamento sequencial de .zvi's
    #todo: ver como acessar a metadata em ReaderSequence

import pims
import pandas as pd
import matplotlib.pyplot as plt





if __name__ == '__main__':
    columns = ["img", "PlaneExposureTime", "PixelsPhysicalSizeX", "PixelsPhysicalSizeY"]
    zviDataFrame = pd.DataFrame(columns=columns)

    for id in range(1, 6):
        path = f'/home/luca/PycharmProjects/pythonProject/vziFiles/sampleFile{id}.zvi'
        read = pims.bioformats.BioformatsReader(path, meta=True)
        meta = read.metadata
        zviDataFrame.loc[id-1] = [read[0],
                                  meta.PlaneExposureTime(0, 0),
                                  meta.PixelsPhysicalSizeX(0),
                                  meta.PixelsPhysicalSizeY(0)]
        plt.imshow(read[0])
        plt.show()
    print(zviDataFrame)


    # print(reader.metadata.PlaneExposureTime(0, 0))
    # print(meta.PixelsPhysicalSizeX(0))
    # print(meta.PixelsPhysicalSizeY(0))
    # print(meta.PixelsPhysicalSizeZ(0))
    # print(meta.LightPathEmissionFilterRefCount(0, 0))
    # print(meta.LightSourceCount(0))
    # print(meta.ImageDescription(0))
    # print(meta.ImageName(0))
    # print(meta.ImageInstrumentRef(0))
    # print(meta.DetectorType(0, 0))

