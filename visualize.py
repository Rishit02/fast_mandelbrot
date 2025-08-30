import matplotlib.pyplot as plt
import mandelbrot                         # compiled extension

img = mandelbrot.mandelbrot(800, 600, 1000)
plt.imshow(img, cmap="twilight_shifted")
plt.colorbar()
plt.title("Mandelbrot - Cython speed")
plt.show()
