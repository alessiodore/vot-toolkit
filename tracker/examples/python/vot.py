"""
\file vot.py

@brief Wrap TraX functions for tracker integration

@author Alessio Dore

@date 2016

"""

import sys

import trax


class VOT(trax.TraxServer):
    """ Extend TraX server wrapping some server functions for tracker integration """
    def __init__(self, options, verbose = False):
        """ Constructor
        
        Args: 
            options: TraX server options 
        """
        self.options = options
        super(VOT, self).__init__(self.options, verbose=verbose)
        
        
    def vot_initialize(self):
        """
        Send configuration message to the client and receive the initialization 
        region and the path of the first image 
        
        Returns:
            region: region as vot_region_rect or vot_region_poly object
            imgPath: path of the first image
        """          
        self.trax_server_setup()    
        import time
        time.sleep(0.5)
        msgType, msgArgs = self.trax_server_wait( )       
        
        
        if msgType in [trax.TRAX_QUIT, trax.TRAX_ERROR]:
            # socket connection will be closed by the destructor using the with statement
            sys.exit(0)
            
        assert(msgType == trax.TRAX_INITIALIZE)
        imgPath, regionStr = msgArgs[0], msgArgs[1]
        # strip quotes from imgPath
        imgPath = imgPath[1:-1] if imgPath[0] == '"' and imgPath[-1] == '"' else imgPath 
        
        region = vot_region_rect() if self.options.region == trax.TRAX_REGION_RECTANGLE else vot_region_poly()
        region.parseRegionStr(regionStr)
        
        self.trax_server_reply(regionStr)
        
        return region, imgPath


    def report(self, region):
        """
        Report the tracking results to the client
        
        Args:
            region: pass region as vot_region_rect or vot_region_poly     
        """
        assert(isinstance(region, vot_region))
        self.trax_server_reply(str(region))
        
    def frame(self):
        """
        Get a frame (image path) from client 
        
        Returns:
            imgPath: absolute path of the image
        """
        msgType, msgArgs = self.trax_server_wait( )
        
        if msgType != trax.TRAX_FRAME or len(msgArgs) != 1:
            return None
        imgPath = msgArgs[0][1:-1] if msgArgs[0][0] == '"' and msgArgs[0][-1] == '"' else msgArgs[0] 
        
        return imgPath
        
    
class vot_region(object):
    """ Base class for vot region """
    def __init__(self):
        pass
        
    def parseRegionStr(self, regionStr):
        """ In derived classes implement method to parse region string """
        return
            
class vot_region_rect(vot_region):
    """ Rectangle region """
    def __init__(self, x=0, y=0, w=0, h=0):
        """ Constructor
        
        Args:
            x: top left x coord of the rectangle region
            y: top left y coord of the rectangle region
            w: width of the rectangle region
            h: height of the rectangle region
        """
        super(vot_region_rect)
        self.regionType = trax.TRAX_REGION_RECTANGLE
        self.x, self.y, self.w, self.h = x, y, w, h

    def __str__(self):
        """ Create string from class to send to client """
        return '{},{},{},{}'.format(self.x, self.y, self.w, self.h)
        
    def parseRegionStr(self, regionStr):
        """ Parse region string to get x, y, w, h """
        self.x, self.y, self.w, self.h = map(float, regionStr.strip('"').split(','))   
            
class vot_region_poly(vot_region):
    """ @todo """
    def __init__(self):
        super(vot_region_rect).__init__(trax.TRAX_REGION_POLYGON)
        self.count = 0
        self.points = list()
        
    def parseRegionStr(self, regionStr):
        """ """
        pass