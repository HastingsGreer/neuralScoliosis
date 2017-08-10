import numpy as np
def loadFile(name):
    imageType = itk.Image[itk.F, 3]
    
    readerType = itk.ImageFileReader[imageType]
    
    reader = readerType.New()
    
    reader.SetFileName(name)
    
    im = reader.GetOutput()
    
    reader.Update()
    return np.array(itk.PyBuffer[imageType].GetArrayFromImage(im))
    
ct = loadFile("C:/Users/hasti/AppData/Local/Temp/Slicer/RemoteIO/CT-chest.nrrd")
horizSpace = .762
vertSpace = 2.5