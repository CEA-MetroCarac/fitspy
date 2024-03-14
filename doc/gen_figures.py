"""
Functions to generate figures
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

from fitspy.spectrum import Spectrum
from fitspy.baseline import BaseLine


def logo():
    x = np.arange(100)
    y1 = np.exp(-((x - 30) ** 2) / 150)
    y2 = 0.5 * np.exp(-((x - 65) ** 2) / 200)

    plt.figure()
    plt.tight_layout()
    plt.plot(y1, 'k', lw=6)
    plt.plot(y2, 'k', lw=6)
    plt.plot(y1 + y2, 'k', lw=12)
    plt.axis('off')
    plt.savefig("Fitspy.png", transparent=True, bbox_inches='tight')


def fun(x):
    return np.exp(-0.01 * x) - 0.3


def gen_spectrum():
    x = np.arange(100).astype(float)
    y0 = fun(x)
    y1 = 0.3 * np.exp(-((x - 30) ** 2) / 50)
    y2 = 0.5 * np.exp(-((x - 70) ** 2) / 50)
    y = y0 + y1 + y2

    np.random.seed(0)
    y += 0.1 * np.random.random(y.size)

    spectrum = Spectrum()
    spectrum.x = x
    spectrum.y = y

    return spectrum


def baseline(attached=True):
    spectrum = gen_spectrum()

    bl_x = np.array([10, 50, 90])
    bl_y = fun(bl_x) - np.array([0.02, -.15, 0.05])
    for x, y in zip(bl_x, bl_y):
        spectrum.baseline.add_point(x, y)

    spectrum.baseline.attached = attached

    fig, ax = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
    fig.tight_layout()

    spectrum.plot(ax[0], show_noise_level=False, show_result=False)
    if attached:
        spectrum.baseline.plot(ax[0], x=spectrum.x, y=spectrum.y)
        points_0 = spectrum.baseline.points
        points_1 = spectrum.baseline.attach_points(spectrum.x, spectrum.y)
        for x0, y0, y1 in zip(points_0[0], points_0[1], points_1[1]):
            ax[0].annotate("", xy=(x0, y1), xytext=(x0, y0),
                           arrowprops=dict(arrowstyle="->", color='r', lw=2))
    else:
        spectrum.baseline.plot(ax[0], x=spectrum.x)
    ax[0].axhline(y=0, c='k', ls='dotted')
    ax[0].axis('off')

    spectrum.subtract_baseline()
    model_0 = spectrum.create_peak_model(0, 'Gaussian', x0=30, ampli=.3)
    model_1 = spectrum.create_peak_model(1, 'Gaussian', x0=70, ampli=.5)
    spectrum.peak_models += [model_0, model_1]
    spectrum.fit()

    spectrum.plot(ax[1], show_noise_level=False, show_result=False,
                  show_negative_values=False, show_baseline=False)
    ax[1].axhline(y=0, c='k', ls='dotted')
    ax[1].set_ylim(-0.2, 0.8)
    ax[1].axis('off')

    fig.text(0.45, 0.7, 'Subtract + Fit', fontsize=15)
    fig.patches.append(FancyArrowPatch([0.48, 0.6], [0.58, 0.6],
                                       transform=fig.transFigure,
                                       mutation_scale=60))

    plt.savefig(f"_static/gen_figures_baseline{attached * '_attached'}.png")


def bkg_model():
    spectrum = gen_spectrum()

    fig, ax = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
    fig.tight_layout()

    spectrum.plot(ax[0], show_noise_level=False)
    ax[0].axhline(y=0, c='k', ls='dotted')
    ax[0].axis('off')

    model_0 = spectrum.create_peak_model(0, 'Gaussian', x0=30, ampli=.3)
    model_1 = spectrum.create_peak_model(1, 'Gaussian', x0=70, ampli=.5)
    spectrum.peak_models += [model_0, model_1]
    spectrum.set_bkg_model('Exponential')

    spectrum.fit()

    spectrum.plot(ax[1], show_noise_level=False, show_baseline=False,
                  show_result=False)
    ax[1].plot(spectrum.x, np.zeros_like(spectrum.x), ls='dotted')
    ax[1].axhline(y=0, c='k', ls='dotted')
    ax[1].set_ylim(-0.2, 0.8)
    ax[1].axis('off')

    fig.text(0.5, 0.7, 'Fit', fontsize=15)
    fig.patches.append(FancyArrowPatch([0.48, 0.6], [0.58, 0.6],
                                       transform=fig.transFigure,
                                       mutation_scale=60))

    # plt.savefig("_static/gen_figures_bkg.png")


# logo()
# baseline(attached=False)
# baseline(attached=True)
bkg_model()
plt.show()
