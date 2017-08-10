import pickle
import scipy.interpolate
import scipy.misc
class UltrasoundData:
    def __init__(self, filename):
        with open(filename, "rb") as file:
            self.rawImages, self.rawAngles = pickle.load(file)
            
        self.alpha, self.beta, self.gamma, self.otime = [
            np.array([o[name] for o in self.rawAngles]) for name in ("alpha", "beta", "gamma", "time")
        ]
        
        
        self.getAlpha = scipy.interpolate.interp1d(self.otime, self.alpha, assume_sorted=True)
        self.getBeta = scipy.interpolate.interp1d(self.otime, self.beta, assume_sorted=True)
        self.getGamma = scipy.interpolate.interp1d(self.otime, self.gamma, assume_sorted=True)
    def rotation(self, time):
        c = 2 * np.pi / 360
        #ALPHA IS NEGATIVE HERE, AS FAR AS I CAN TELL BUG IN SPEC
        return angletomatrix(-self.getAlpha(time) * c, self.getBeta(time) * c, self.getGamma(time) * c)
    
    def makeData(self):
        self.monoImages = np.sum(self.rawImages[1], 3).astype(np.float)
        self.rMatrices = np.array([self.rotation(time) for time in self.rawImages[0]])
        
        self.angles = np.arctan2(self.rMatrices[:,2,0 ], self.rMatrices[:, 2, 1])
        
        self.angles = np.concatenate([self.angles, -self.angles])
        
        

        self.data = np.array([scipy.misc.imresize(arr, (100, 100)) for arr in self.monoImages]).reshape(-1, 100, 100, 1) / 255
        
        self.data = np.concatenate([self.data, np.flip(self.data, 1)])
        
        self.classes = 3 * self.angles / np.pi

        
def angletomatrix(alpha, beta, gamma):
    """
    Returns a matrix that transforms from world coordinates to device coordinates
    """
    
    cA = np.cos(alpha)
    cB = np.cos(beta)
    cC = np.cos(gamma)
    sA = np.sin(alpha)
    sB = np.sin(beta)
    sC = np.sin(gamma)
    
    M1 = np.matrix([[cC,   0,  sC],
                    [0,    1,   0],
                    [-sC,  0,  cC]])
    
    M2 = np.matrix([[1,    0,   0],
                    [0,   cB, -sB],
                    [0,   sB,  cB]])
    
    M3 = np.matrix([[cA, -sA,   0],
                    [sA,  cA,   0],
                    [0,    0,   1]])
 
    return np.array((M1 * M2 * M3))
        
        


udata = UltrasoundData("../../ultrasoundHacks/August8SpineInWaterNoDetritus2.pickle")
udata.makeData()