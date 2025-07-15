# imageToContour
Convert images to contours generated with the fast marching method

This method uses the pykonal library to generate a map of travel times that can be processed as a contour plot, where the travel time for each pixel is influenced by velocities that are controlled by the brightness of the pixels in an input image

Getting the libraries working in Thonny was really annoying, in particular the pykonal library seems to need specific versions of Numpy that were not the default. This was solved by uninstalling the Numpy library and then upgrading to a suitable version (range of allowed versions was found in the error messages). For approximate steps see comments at the top of the file

Note: I know basically nothing about Python, some of the conversions of arrays etc. in the code are probably very, very ugly because I don't know any better - fix them if you feel like having a go
