"""
\file static.py

@brief Example of tracker integration. Static tracker 

@author Alessio Dore

@date 2016

"""

import vot
import time

def static():  
    options = vot.trax.TraxServerOptions('static', 'v1', vot.trax.TRAX_REGION_RECTANGLE, vot.trax.TRAX_IMAGE_PATH)   
    with vot.VOT(options, True) as pyvot: 
        initRegion, initImgPath = pyvot.vot_initialize()            
        while True:                
            imgPath = pyvot.frame()
            if not imgPath:
                break
            pyvot.report(initRegion)
            # @fixme: the evaluation breaks if it runs too fast
            time.sleep(0.01)
    return 0       

if __name__ == '__main__':
    static()


