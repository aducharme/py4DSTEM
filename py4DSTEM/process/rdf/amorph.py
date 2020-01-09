import numpy as np
import matplotlib.pyplot as plt
import py4DSTEM
import scipy.io as sio
from py4DSTEM.process.utils import print_progress_bar
from py4DSTEM.process.utils import polar_elliptical_transform
from py4DSTEM.process.utils.ellipticalCoords import *
import matplotlib
from tqdm import tqdm

matplotlib.rcParams["figure.dpi"] = 100
plt.ion()


def fit_stack(datacube, init_coefs, mask=None):
    """
    This will fit an ellipse using the polar elliptical transform code to all the diffraction patterns. It will take in a datacube and return a coefficient array which can then be used to map strain, fit the centers, etc.

    Accepts:
        datacute    - a datacube of diffraction data
        init_coefs  - an initial starting guess for the fit
        mask        - a mask, either 2D or 4D, for either one mask for the whole stack, or one per pattern. 
    Returns:
        coef_cube  - an array of coefficients of the fit
    """
    coefs_array = np.zeros([i for i in datacube.data.shape[0:2]] + [len(init_coefs)])
    for i in tqdm(range(datacube.R_Nx)):
        for j in range(datacube.R_Ny):
            if len(mask.shape)==2:
                mask_current = mask
            elif len(mask.shape==4):
                mask_current = mask[i,j,:,:]

            coefs = fit_double_sided_gaussian(datacube[i,j,:,:], init_coefs, mask=mask_current)
            coefs_array[i, j] = coefs

    return coefs_array


def calculate_coef_strain(coef_cube, A_ref=None, B_ref=None, C_ref=None):
    """
    This function will calculate the strains from a 3D matrix output by fit_stack

    Coefs order:
        I0          the intensity of the first gaussian function
        I1          the intensity of the Janus gaussian
        sigma0      std of first gaussian
        sigma1      inner std of Janus gaussian
        sigma2      outer std of Janus gaussian
        c_bkgd      a constant offset
        R           center of the Janus gaussian
        x0,y0       the origin
        A,B,C       Ax^2 + Bxy + Cy^2 = 1

    Accepts:
        coef_cube   - output from fit_stack
        A_ref       - reference radius ~0 strain (coef[10]). Default is none, and then will use median value
        B_ref       - reference B value (coef[8]), from perhaps mean image
        C_ref       - reference C value (coef[9]), from perhaps mean image
    Returns:
        exx         - strain in the major axis direction
        eyy         - strain in the minor axis direction
        exy         - shear

    """
    if A_ref is None:
        A_ref = 1
    if C_ref is None:
        C_ref = 1
    if B_ref is None:
        B_ref = 0
    A = coef_cube[:, :, 10]
    B = coef_cube[:, :, 11]
    C = coef_cube[:, :, 12]

    exx = 1 / 2 * (A - A_ref)
    eyy = 1 / 2 * (C - C_ref)  # TODO - make sure this is ok to do
    exy = 1 / 2 * (B - B_ref)  # TODO - make sure this is ok to do

    return exx, eyy, exy


def plot_strains(strains, cmap="RdBu_r", vmin=None, vmax=None):
    """
    This function will plot strains with a unified color scale.

    Accepts:
        strains             - a collection of 3 arrays in the format (exx, eyy, exy)
        cmap, vmin, vmax    - imshow parameters
    """
    if vmin is None:
        vmin = np.min(strains)
    if vmax is None:
        vmax = np.max(strains)

    plt.figure(88, figsize=(9, 5.8))
    plt.clf()
    f, (ax1, ax2, ax3) = plt.subplots(1, 3, num=88)
    ax1.imshow(strains[0], cmap=cmap, vmin=vmin, vmax=vmax)
    ax1.tick_params(
        axis="both",
        which="both",
        bottom=False,
        top=False,
        left=False,
        right=False,
        labelbottom=False,
        labelleft=False,
    )
    ax1.set_title(r"$\epsilon_{AA}$")

    ax2.imshow(strains[1], cmap=cmap, vmin=vmin, vmax=vmax)
    ax2.tick_params(
        axis="both",
        which="both",
        bottom=False,
        top=False,
        left=False,
        right=False,
        labelbottom=False,
        labelleft=False,
    )
    ax2.set_title(r"$\epsilon_{CC}$")

    im = ax3.imshow(strains[2], cmap=cmap, vmin=vmin, vmax=vmax)
    ax3.tick_params(
        axis="both",
        which="both",
        bottom=False,
        top=False,
        left=False,
        right=False,
        labelbottom=False,
        labelleft=False,
    )
    ax3.set_title(r"$\epsilon_{B}$")

    cbar_ax = f.add_axes([0.125, 0.25, 0.775, 0.05])
    f.colorbar(im, cax=cbar_ax, orientation="horizontal")

    return


def compare_coef_cube(dp, coefs, mask=None, power=0.3):
    """
    This function will compare the fit to individual diffraction patterns. It is essentially a helper function to quickly build the right object.

    Accepts:
        dp      - a 2D diffraction pattern
        coefs   - coefs from coef_cube, corresponding to the diffraction pattern
        power   - the power to which the comparison is taken
    Returns:
        None
    """
    dp = polar_elliptical_transform(dp, mask=mask)
    dp.compare_coefs_two_sided_gaussian(coefs, power=power)
    return


def convert_stack_polar(datacube, coef_cube):
    """
    This function will take the coef_cube from fit_stack and apply it to the image stack, to return polar transformed images.

    Accepts:
        datacube    - data in datacube format
        coef_cube  - coefs from fit_stack

    Returns:
        datacube_polar - polar transformed datacube
    """

    return datacube_polar


def compute_polar_stack_symmetries(datacube_polar):
    """
    This function will take in a datacube of polar-transformed diffraction patterns, and do the autocorrelation, before taking the fourier transform along the theta direction, such that symmetries can be measured. They will be plotted by a different function

    Accepts:
        datacube_polar  - diffraction pattern cube that has been polar transformed

    Returns:
        datacube_symmetries - the normalized fft along the theta direction of the autocorrelated patterns in datacube_polar
    """

    return datacube_symmetries


def plot_symmetries(datacube_symmetries, sym_order):
    """
    This function will take in a datacube from compute_polar_stack_symmetries and plot a specific symmetry order. 

    Accepts:
        datacube_symmetries - result of compute_polar_stack_symmetries, the stack of fft'd autocorrelated diffraction patterns
        sym_order           - symmetry order desired to plot
    Returns:
        None
    """

    return None
