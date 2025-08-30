# cython: language_level=3
import numpy as np
cimport numpy as np

cpdef np.ndarray[np.int32_t, ndim=2] mandelbrot(
    int width, int height, int maxiter=1_000):
    cdef int x, y, i
    cdef double zx, zy, tmp, cx, cy
    cdef np.ndarray[np.int32_t, ndim=2] out = np.zeros((height, width), dtype=np.int32)

    # core loop
    for y in range(height):
        for x in range(width):
            cx = (x - width  / 2.0) * 4.0 / width
            cy = (y - height / 2.0) * 4.0 / height
            zx = zy = 0.0
            for i in range(maxiter):
                tmp = zx * zx - zy * zy + cx
                zy  = 2.0 * zx * zy + cy
                zx  = tmp
                if zx * zx + zy * zy > 4.0:
                    out[y, x] = i
                    break
    return out