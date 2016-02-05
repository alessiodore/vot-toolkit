"""
\file static.py

"""

import vot

def static():  
    options = vot.trax.TraxServerOptions('static', 'v1', vot.trax.TRAX_REGION_RECTANGLE, vot.trax.TRAX_IMAGE_PATH)   
    with vot.VOT(options, True) as pyvot: 
        #pyvot.trax_server_setup()           
        #msgType, msgArgs = pyvot.trax_server_wait( )          
        
        initRegion, initImgPath = pyvot.vot_initialize()            
        while True:                
            imgPath = pyvot.frame()
            if not imgPath:
                break
            pyvot.report(initRegion)
            
    return 0       

if __name__ == '__main__':
    static()


