from __future__ import absolute_import, print_function, division

import warnings

import numpy as np
from matplotlib.pyplot import Locator
import astropy.units as u

# from . import wcs_util
from . import angle_util as au
from . import scalar_util as su
# from . import math_util
from .decorators import auto_refresh


class Ticks(object):

    @auto_refresh
    def __init__(self, axes, x, y, parameters):
        self._ax = axes
        self.x = x
        self.y = y
        self._wcs = self._ax.wcs
        self.x_unit = self._wcs.wcs.cunit[self.x]
        self.y_unit = self._wcs.wcs.cunit[self.y]

        # Save plotting parameters (required for @auto_refresh)
        self._parameters = parameters

        # Set tick positions
        self.x_visible_axes = 'b'
        self.y_visible_axes = 'l'

    @auto_refresh
    def set_xspacing(self, spacing):
        '''
        Set the x-axis tick spacing, in degrees. To set the tick spacing to be
        automatically determined, set this to 'auto'.
        '''

        if spacing == 'auto':
            self._ax.coords[self.x].set_ticks(spacing=None)
        else:
            coord_type = self._ax.coords[self.x].coord_type
            x_format = self._ax.coords[self.x]._formatter_locator.format
            if coord_type in ['longitude', 'latitude']:
                try:
                    # TODO: Test this
                    if (x_format is not None):
                        au._check_format_spacing_consistency(x_format, au.Angle(degrees=spacing, latitude=coord_type == 'latitude'))
                except au.InconsistentSpacing:
                    warnings.warn("WARNING: Requested tick spacing format cannot be shown by current label format. The tick spacing will not be changed.")
                    return
                self._ax.coords[self.x].set_ticks(spacing=spacing * u.degree)
            else:
                try:
                    su._check_format_spacing_consistency(x_formatxformat, spacing)
                except au.InconsistentSpacing:
                    warnings.warn("WARNING: Requested tick spacing format cannot be shown by current label format. The tick spacing will not be changed.")
                    return
                self._ax.coords[self.x].set_ticks(spacing=spacing * self.x_unit)

        # TODO: implement
        # if hasattr(self._parent, 'grid'):
        #     self._parent.grid._update()

    @auto_refresh
    def set_yspacing(self, spacing):
        '''
        Set the y-axis tick spacing, in degrees. To set the tick spacing to be
        automatically determined, set this to 'auto'.
        '''

        if spacing == 'auto':
            self._ax.coords[self.y].set_ticks(spacing=None)
        else:
            coord_type = self._ax.coords[self.y].coord_type
            y_format = self._ax.coords[self.y]._formatter_locator.format

            if coord_type in ['longitude', 'latitude']:
                try:
                    # TODO: Test this
                    au._check_format_spacing_consistency(y_format, au.Angle(degrees=spacing, latitude=coord_type == 'latitude'))
                except au.InconsistentSpacing:
                    warnings.warn("WARNING: Requested tick spacing format cannot be shown by current label format. The tick spacing will not be changed.")
                    return
                self._ax.coords[self.y].set_ticks(spacing=spacing * u.degree)
            else:
                try:
                    # TODO: Test
                    su._check_format_spacing_consistency(y_format, spacing)
                except au.InconsistentSpacing:
                    warnings.warn("WARNING: Requested tick spacing format cannot be shown by current label format. The tick spacing will not be changed.")
                    return
                self._ax.coords[self.y].set_ticks(spacing=spacing * self.y_unit)

        # TODO: implement
        # if hasattr(self._parent, 'grid'):
        #     self._parent.grid._update()

    @auto_refresh
    def set_color(self, color):
        '''
        Set the color of the ticks
        '''
        self._ax.coords[self.x].set_ticks(color=color)
        self._ax.coords[self.y].set_ticks(color=color)

    @auto_refresh
    def set_length(self, length, minor_factor=0.5):
        '''
        Set the length of the ticks (in points)
        '''
        self._ax.coords[self.x].set_ticks(size=length)
        self._ax.coords[self.y].set_ticks(size=length)

        # TODO: Add this once minor ticks are implemented in WCSAxes
        # Minor ticks
        # for line in self._ax1.xaxis.get_minorticklines():
        #     line.set_markersize(length * minor_factor)
        # for line in self._ax1.yaxis.get_minorticklines():
        #     line.set_markersize(length * minor_factor)
        # for line in self._ax2.xaxis.get_minorticklines():
        #     line.set_markersize(length * minor_factor)
        # for line in self._ax2.yaxis.get_minorticklines():
        #     line.set_markersize(length * minor_factor)

    @auto_refresh
    def set_linewidth(self, linewidth):
        '''
        Set the linewidth of the ticks (in points)
        '''
        self._ax.coords[self.x].set_ticks(width=linewidth)
        self._ax.coords[self.y].set_ticks(width=linewidth)

    @auto_refresh
    def set_minor_frequency(self, xfrequency, yfrequency=None):
        '''
        Set the number of subticks per major tick. Set to one to hide minor
        ticks.
        If not yfrequency given, frequency is the same in both axis.
        Otherwise, xfrequency represents the frequency in the xaxis and
        yfrequency the one in the yaxis.
        '''

        if yfrequency is None:
            yfrequency = xfrequency

        try:
            self._ax.coords[self.x].display_minor_ticks(True)
            self._ax.coords[self.y].display_minor_ticks(True)
            # TODO: Possibly check for integer values of frequency
            self._ax.coords[self.x].set_minor_frequency(xfrequency)
            self._ax.coords[self.y].set_minor_frequency(yfrequency)
        except:
            pass

    @auto_refresh
    def show(self):
        """
        Show the x- and y-axis ticks
        """
        self.show_x()
        self.show_y()

    @auto_refresh
    def hide(self):
        """
        Hide the x- and y-axis ticks
        """
        self.hide_x()
        self.hide_y()

    @auto_refresh
    def show_x(self):
        """
        Show the x-axis ticks
        """
        self._ax.coords[self.x].set_ticks_position('all')

    @auto_refresh
    def hide_x(self):
        """
        Hide the x-axis ticks
        """
        self._ax.coords[self.x].set_ticks_position('')

    @auto_refresh
    def show_y(self):
        """
        Show the y-axis ticks
        """
        self._ax.coords[self.y].set_ticks_position('all')

    @auto_refresh
    def hide_y(self):
        """
        Hide the y-axis ticks
        """
        self._ax.coords[self.y].set_ticks_position('')
