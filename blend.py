from Frame import Frame

background = Frame()
overlay = Frame()

background.load_from_path("image1.jpg")
overlay.load_from_path("image2.jpg")

background.overlay_transparent(overlay.frame, x=300, y=200)