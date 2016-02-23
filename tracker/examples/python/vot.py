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
            region: region as trax_region_rect or trax_region_poly object
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
        
        region = trax.trax_region_rect() if self.options.region == trax.TRAX_REGION_RECTANGLE else trax.trax_region_poly()
        region.parseRegionStr(regionStr)
        
        self.trax_server_reply(regionStr)
        
        return region, imgPath


    def report(self, region):
        """
        Report the tracking results to the client
        
        Args:
            region: pass region as trax_region_rect or trax_region_poly     
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
    