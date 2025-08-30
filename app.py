import streamlit as st
import numpy as np
import time
import matplotlib.pyplot as plt

import mandelbrot


def mandelbrot_py(width: int, height: int, max_iter: int = 1_000):
    out = np.zeros((height, width), dtype=np.int32)

    for y in range(height):
        for x in range(width):
            # map pixel to complex-plane coordinate
            cx = (x - width / 2.0) * 4.0 / width
            cy = (y - height / 2.0) * 4.0 / height

            zx = zy = 0.0  # z = 0 + 0i
            for i in range(max_iter):
                tmp = zx * zx - zy * zy + cx  # z = z² + c
                zy = 2.0 * zx * zy + cy
                zx = tmp
                if zx * zx + zy * zy > 4.0:  # divergence test
                    out[y, x] = i
                    break
    return out


# Streamlit UI
st.title("Mandelbrot Speed Benchmark  (Python vs Cython)")

cols = st.columns(3)
width = cols[0].slider("Width", 100, 1_000, 400, 50)
height = cols[1].slider("Height", 100, 1_000, 300, 50)
max_iter = cols[2].slider("Max iterations", 100, 2_000, 600, 100)

if st.button("Run benchmark"):
    with st.empty():
        st.info("⏳ Computing…")

        # Python run
        t0 = time.time()
        py_img = mandelbrot_py(width, height, max_iter)
        py_time = time.time() - t0

        # Cython run
        t0 = time.time()
        cy_img = mandelbrot.mandelbrot(width, height, max_iter)
        cy_time = time.time() - t0

        # Results
        st.success(
            f"Pure-Python: **{py_time:.3f}s**   |   "
            f"Cython: **{cy_time:=.3f}s**  → "
            f"**{py_time / cy_time:,.1f}x faster**"
        )

    # Plot images
    colormap = "nipy_spectral"
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].imshow(py_img, cmap=colormap)
    axes[0].set_title("Python")
    axes[0].axis("off")
    axes[1].imshow(cy_img, cmap=colormap)
    axes[1].set_title("Cython")
    axes[1].axis("off")
    st.pyplot(fig)
