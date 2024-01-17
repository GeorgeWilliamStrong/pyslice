import numpy as np
from IPython.display import HTML
from IPython.display import display
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl

mpl.rcParams['animation.embed_limit'] = 2**128
plt.rcParams.update({'font.size': 9.5})


__all__ = ['static_plot', 'slicer', 'render']


def static_plot(volume, slices=None, vmin=None, vmax=None, **kwargs):
    """
    Utility function to plot a 3D volume through the x, y, and z planes.

    Parameters
    ----------
    volume : ndarray
        3D volume.
    slices : tuple of int, optional
        Specification of the slices to plot from each axis. Defaults to middle
        slices through the volume.
    vmin : float, optional
        Minimum value to use in color scale. Defaults to None.
    vmax : float, optional
        Maximum value to use in color scale. Defaults to None.
    **kwargs : additional keyword arguments
        cmap : str, optional
            Matplotlib colormap name. Defaults to 'Spectral_r'.
        size : tuple, optional
            Figure size. Defaults to (10, 6).
        grid : bool, optional
            Whether to display a grid on each subplot. Defaults to True.
        interpolation : str, optional
            Interpolation method for imshow. Defaults to 'bilinear'.
        cbar_scale : float, optional
            Scales the size of the colorbar. Defaults to 0.4.

    Returns
    -------

    """
    cmap = kwargs.pop('cmap', 'plasma')
    size = kwargs.pop('size', (10, 6))
    grid = kwargs.pop('grid', True)
    interpolation = kwargs.pop('interpolation', 'bilinear')
    cbar_scale = kwargs.pop('cbar_scale', 0.4)

    if slices is None:
        slices = (volume.shape[0]//2, volume.shape[1]//2, volume.shape[2]//2)

    if vmin is None:
        vmin = volume.min()
    if vmax is None:
        vmax = volume.max()

    fig, axes = plt.subplots(1, 3, figsize=size, constrained_layout=True)
    im1 = axes[0].imshow(_get_slice(volume, slices[0], 0), cmap=cmap,
                         interpolation=interpolation, vmin=vmin, vmax=vmax)
    axes[1].imshow(_get_slice(volume, slices[1], 1), cmap=cmap,
                   interpolation=interpolation, vmin=vmin, vmax=vmax)
    axes[2].imshow(_get_slice(volume, slices[2], 2), cmap=cmap,
                   interpolation=interpolation, vmin=vmin, vmax=vmax)

    for ax in axes:
        ax.tick_params(axis='both', direction='in')
        if grid:
            ax.grid(True, color='lightgrey', linewidth=0.5, alpha=0.5)

    fig.colorbar(im1, ax=axes.ravel().tolist(), shrink=cbar_scale)
    plt.show()


def slicer(volumes, axis=0, animate=False, vmin=None, vmax=None, **kwargs):
    """
    Create a slice viewer for 3D volumes.

    Parameters
    ----------
    volumes : list or array
        List of 3D volumes to be visualized.
    axis : int
        The axis along which slicing is performed (0 for x, 1 for y, 2 for z).
        Default is 0.
    animate : bool, optional
        If True, create an animated view; if False, create an interactive view
        that can be controlled using the {j, k} keys. Default is False.
    vmin : float or list, optional
        Minimum intensity value(s) for the color scale. Default is None.
    vmax : float or list, optional
        Maximum intensity value(s) for the color scale. Default is None.
    **kwargs : additional keyword arguments
        size : tuple of int, optional
            Figure size, specified as a (width, height) tuple.
            Default is (12, 4).
        nrows : int, optional
            Number of rows in the subplot grid. Default is 1.
        interpolation : str, optional
            Interpolation method for displaying slices. Default is 'bilinear'.
        grid : bool, optional
            If True, display grid lines. Default is True.
        interval : int, optional
            Time delay between frames in milliseconds (for animations).
            Default is 50.
        blit : bool, optional
            If True, use blitting for animations. Default is True.
        spacing : int, optional
            Spacing between slices (for animations). Default is 1 for
            animations, 3 for static views.
        cmap : str or list, optional
            Colormap(s) to be used for visualization. Default is 'viridis'.
        title : str or list, optional
            Title(s) for the subplots. Default is 'Volume {n}' where
            n is the volume number.

    Returns
    -------
    ani : matplotlib.animation.ArtistAnimation or None
        Returns an animation if animate is True, otherwise returns None.

    Notes
    -----

    The animate option returns a matplotlib.animation.ArtistAnimation object
    rather than displaying a plot. To display, you can make use of the
    render() function.
    """
    # If single input is given, configure as a list
    if not isinstance(volumes, list):
        volumes = [volumes]

    # Configure plot settings
    size = kwargs.pop('size', (12, 4))
    nrows = kwargs.pop('nrows', 1)
    nvols = len(volumes)
    ncols = nvols//nrows
    grid = kwargs.pop('grid', True)
    interpolation = kwargs.pop('interpolation', 'bilinear')
    if animate:
        interval = kwargs.pop('interval', 50)
        blit = kwargs.pop('blit', True)
        spacing = kwargs.pop('spacing', 1)
    else:
        spacing = kwargs.pop('spacing', 3)
    d_volumes = []
    for vol in volumes:
        if axis == 0:
            d_volumes.append(vol[::spacing])
        elif axis == 1:
            d_volumes.append(vol[:, ::spacing])
        elif axis == 2:
            d_volumes.append(vol[:, :, ::spacing])

    # Colorscale constraints
    if vmin is None:
        vmin = [vol.min() for vol in volumes]
    elif type(vmin) is not list:
        vmin = [vmin for i in range(nvols)]
    for i in range(nvols):
        if vmin[i] is None:
            vmin[i] = volumes[i].min()

    if vmax is None:
        vmax = [vol.max() for vol in volumes]
    elif type(vmax) is not list:
        vmax = [vmax for i in range(nvols)]
    for i in range(nvols):
        if vmax[i] is None:
            vmax[i] = volumes[i].max()

    # Set default colormaps
    cmap = kwargs.pop('cmap', None)
    if cmap is None:
        cmap = ['plasma' for i in range(nvols)]
    elif type(cmap) is not list:
        cmap = [cmap for i in range(nvols)]
    for i in range(nvols):
        if cmap[i] is None:
            cmap[i] = 'plasma'

    # Additional plot settings
    title = kwargs.pop('title', None)
    if title is None:
        title = [f'Volume {i+1}' for i in range(nvols)]
    elif type(title) is not list:
        title = [title for i in range(nvols)]
    for i in range(nvols):
        if title[i] is None:
            title[i] = f'Volume {i+1}'

    # Create the plot axes
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=size,
                             sharex=True, sharey=True, constrained_layout=True)
    if nrows == 1:
        if ncols == 1:
            axes = np.array([[axes]])
        else:
            axes = axes[None]

    if animate:
        ims_full = []
        for i in range(0, d_volumes[0].shape[axis]):
            ims = []
            for row in range(nrows):
                for col in range(ncols):
                    idx = row * ncols + col
                    ax = axes[row, col]
                    ims.append(ax.imshow(_get_slice(d_volumes[idx], i, axis),
                                         animated=True, vmin=vmin[idx],
                                         vmax=vmax[idx], cmap=cmap[idx],
                                         interpolation=interpolation))
                    ax.tick_params(axis='both', direction='in')
                    title_i = ax.text(0.5, 1.05, f'{title[idx]}, Slice {i*spacing}, Axis {axis}',
                                      size=plt.rcParams["axes.titlesize"],
                                      ha="center", transform=ax.transAxes)
                    ims.append(title_i)
                    if grid:
                        ax.grid(True, color='lightgrey', linewidth=0.5,
                                alpha=0.5)
            ims_full.append(ims)

        # Create matplotlib animation object
        ani = animation.ArtistAnimation(fig, ims_full, interval=interval,
                                        blit=blit)
        plt.close()

        return ani

    else:
        _remove_keymap_conflicts({'j', 'k'})
        for row in range(nrows):
            for col in range(ncols):
                idx = row * ncols + col
                if idx < nvols:
                    ax = axes[row, col]
                    ax.volume = d_volumes[idx]
                    ax.index = d_volumes[idx].shape[axis] // 2
                    ax.spacing = spacing
                    ax.slicing_axis = axis
                    ax._title = title[idx]
                    ax.imshow(_get_slice(d_volumes[idx], ax.index, ax.slicing_axis),
                              vmin=vmin[idx], vmax=vmax[idx], cmap=cmap[idx],
                              interpolation=interpolation)
                    ax.set_title(f'{ax._title}, Slice {ax.index*ax.spacing}, Axis {ax.slicing_axis}')
                    ax.tick_params(axis='both', direction='in')
                    if grid:
                        ax.grid(True, color='lightgrey', linewidth=0.5,
                                alpha=0.5)

        # Calls _process_key() to update plot upon key_press_event
        fig.canvas.mpl_connect('key_press_event',
                               lambda event: _process_key(event, axes))
        plt.show()

def render(ani, html5_video=False):
    """
    Render and display the animation.

    This function renders and displays the animation using either HTML5 video
    or JavaScript based on the specified format.

    Parameters
    ----------
    ani : matplotlib.animation.ArtistAnimation
        Matplotlib ArtistAnimation object representing the animation.
    html5_video : bool, optional
        If True, the animation is displayed using HTML5 video format.
        If False, the animation is displayed using JavaScript.
        Defaults to False.

    Returns
    -------

    """
    if html5_video is True:
        display(HTML(ani.to_html5_video()))
    else:
        display(HTML(ani.to_jshtml()))


def _get_slice(volume, index, axis):
    """
    Extracts a 2D slice from a 3D volume along a specified axis.

    Parameters
    ----------
    volume : ndarray
        3D array representing a volume.
    index : int
        Index of the slice along the specified axis.
    axis : int
        Axis along which the slice is taken (0 for x-axis, 1 for y-axis,
        2 for z-axis).

    Returns
    -------
    ndarray
        2D slice extracted from the 3D volume along the specified axis.

    """
    if axis == 0:
        return volume[index, :, :]
    elif axis == 1:
        return volume[:, index, :]
    elif axis == 2:
        return volume[:, :, index]


def _remove_keymap_conflicts(new_keys_set):
    """
    Remove keymap conflicts from Matplotlib configuration.

    This function removes conflicting keymap entries from the Matplotlib
    configuration. It is used to prevent interference with custom key
    bindings in interactive applications.

    Parameters
    ----------
    new_keys_set : set
        Set of new keys to avoid conflicts. Keymap entries containing
        these keys will be removed.

    Returns
    -------

    """
    for prop in plt.rcParams:
        if prop.startswith('keymap.'):
            keys = plt.rcParams[prop]
            remove_list = set(keys) & new_keys_set
            for key in remove_list:
                keys.remove(key)


def _process_key(event, axs):
    """
    Process key events for navigating through slices in multi-volume viewer.

    Parameters
    ----------
    event : mpl_event
        Matplotlib key press event.
    axs : np.ndarray
        Array of matplotlib Axes representing subplots.

    Returns
    -------

    """
    for row in axs:
        for ax in row:
            if event.key == 'j':
                _previous_slice(ax)
            elif event.key == 'k':
                _next_slice(ax)
    event.canvas.draw()


def _previous_slice(ax):
    """
    Display the previous slice in a volume on a specific axis.

    Parameters
    ----------
    ax : mpl_axes
        Matplotlib Axes representing a subplot.

    Returns
    -------

    """
    volume = ax.volume
    ax.index = (ax.index - 1) % volume.shape[ax.slicing_axis]
    ax.images[0].set_array(_get_slice(volume, ax.index, ax.slicing_axis))
    ax.set_title(f'{ax._title}, Slice {ax.index*ax.spacing}, Axis {ax.slicing_axis}')


def _next_slice(ax):
    """
    Display the next slice in a volume on a specific axis.

    Parameters
    ----------
    ax : mpl_axes
        Matplotlib Axes representing a subplot.

    Returns
    -------

    """
    volume = ax.volume
    ax.index = (ax.index + 1) % volume.shape[ax.slicing_axis]
    ax.images[0].set_array(_get_slice(volume, ax.index, ax.slicing_axis))
    ax.set_title(f'{ax._title}, Slice {ax.index*ax.spacing}, Axis {ax.slicing_axis}')
