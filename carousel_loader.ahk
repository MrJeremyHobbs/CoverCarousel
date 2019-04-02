;------------------------------------------------------------------------------
; This is loader script that opens FSViewer (which has the default "daily" folder 
; as its starting folder) and begins slideshow.
;------------------------------------------------------------------------------

;------------------------------------------------------------------------------
; Start cover script
; This script queries the Alma set against ContentCafe for high-quality cover images
;------------------------------------------------------------------------------

run nbl.py
sleep 2000

;------------------------------------------------------------------------------
; Start Slideshow
; NOTE: change this folder path as needed.
;------------------------------------------------------------------------------

run .\FSViewer64\FSViewer.exe
sleep 1000
send s
sleep 1000
send {enter}