import RPi.GPIO as gpio
import time
import app.ocr as ocr
import app.tts as tts
import app.face as face
import app.vision as vision


def main():
	print('\n\nSETUP COMPLETED\n\n')
	gpio.setwarnings(False)
	gpio.setmode(gpio.BCM)
	gpio.setup(17, gpio.IN)
	gpio.setup(18, gpio.IN)
	gpio.setup(27, gpio.IN)
	gpio.setup(22, gpio.IN)
	gpio.setup(2,gpio.OUT)
	s1_prev = True
	s2_prev = True
	s3_prev = True
	s4_prev = True

	while True:
		try:
			s1_curr = gpio.input(17)
			s2_curr = gpio.input(18)
			s3_curr = gpio.input(27)
			s4_curr = gpio.input(22)

			if (s1_prev and (not s1_curr)): 
			    print("Image Captioning Triggered\n\n")
			    vision.caption_image()

			if (s2_prev and (not s2_curr)): 
			    print("Face Recognition Triggered\n\n")
			    face.face_recognition()

			if (s3_prev and (not s3_curr)): 
			    print("Emotion Recognition Triggered\n\n")
			    face.emotion_recognition()

			if (s4_prev and (not s4_curr)): 
			    print("Text Reading Triggered\n\n")
			    ocr.ocr()

			s1_prev = s1_curr
			s2_prev = s2_curr
			s3_prev = s3_curr
			s4_prev = s4_curr
			time.sleep(0.05)
		except Exception:
			print (Exception)
			print("Sorry for the error. Restarting Program")


if __name__ == "__main__":
	main()
