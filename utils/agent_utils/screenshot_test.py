from PIL import ImageGrab

def capture_screenshot_with_pillow():
    screenshot = ImageGrab.grab()
    screenshot.save("/home/kali/local_screenshot_pillow.png")

