import cv2
import filters
from numpy import *
from managers import WindowManager, CaptureManager

class Cameo(object):
    
    def __init__(self):
        self._windowManager = WindowManager('Cameo',
                                            self.onKeypress)
        self._captureManager = CaptureManager(
            cv2.VideoCapture(0), self._windowManager, True)

        self._cameraMatrix = array([[738.134, 0, 367.371], [0, 736.132, 236.552], [0, 0, 1]])
        self._distCoeffs  = array([-0.531157, 0.515348, -0.0166326, -0.00256654, -0.536911])


    def run(self):
        """Run the main loop."""
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
            
            if frame is not None:
                frame = cv2.undistort(frame, self._cameraMatrix, self._distCoeffs)
                frame = filters.GaussianBlurhandle(frame)
                frame = filters.goodFeaturesToTrackHandle(frame)
                # frame = filters.FastDetect(frame)
                # # self._captureManager.frame = filters.combineHighlightandCornerHarrisHanle(frame)
                # cv2.putText(frame, self._captureManager.getfpsEstimateStr(), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                self._captureManager.frame = frame


            self._captureManager.exitFrame()
            self._windowManager.processEvents()
    
    def onKeypress(self, keycode):
        """Handle a keypress.
        
        space  -> Take a screenshot.
        tab    -> Start/stop recording a screencast.
        escape -> Quit.
        
        """
        if keycode == 32: # space
            print  "Space down"
            fileCount = self._captureManager.getSreenShotCount()
            self._captureManager.writeImage("chessboards/chessboard" + fileCount + ".jpg")
        elif keycode == 9: # tab
            if not self._captureManager.isWritingVideo:
                self._captureManager.startWritingVideo(
                    'screencast.avi')
            else:
                self._captureManager.stopWritingVideo()
        elif keycode == 27: # escape
            self._windowManager.destroyWindow()

if __name__=="__main__":
    Cameo().run()
