"""
\file static.py

"""



import vot as pyvot


def static():
    options = pyvot.trax.TraxServerOptions('test', 'v1', pyvot.trax.TRAX_REGION_RECTANGLE, pyvot.trax.TRAX_IMAGE_PATH)
    with pyvot.VOT(options,True) as vot:
        initRegion, initImgPath  = vot.initialize()
        while True:
            imgPath = vot.frame()
            if not imgPath:
                break
            vot.report(initRegion)
            
    return 0       

if __name__ == '__main__':
    static()


