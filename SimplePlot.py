# Copyright (C) 2022 Nikolas Koesling <nikolas@koesling.info>

import matplotlib.pyplot as plt
import os


##
# @brief check if a file can be written
#
# @param f filepath as string
#
def check_file_writable(f):
    if not isinstance(f, str):
        raise RuntimeError(f"{type(f)} is not a valid filename type")
    # end if

    if os.path.exists(f):
        if os.path.isfile(f):
            return os.access(f, os.W_OK)
        else:
            return False
        # end if
    else:
        parent = os.path.dirname(f)
        if not parent:
            parent = '.'
        # end if
        return os.access(parent, os.W_OK)
    # end if
# end def check_file_writable


##
# @brief wrapper to create simple plots with pyplot
#
class SimplePlot:
    ##
    # @brief
    # initialize SimplePlot instance
    #
    # @details
    # Uses the following default settings:
    #   - No axis labels
    #   - Y axis starting at 0, upper limit determined by the input data
    #   - X axis limit depending on the input data
    #   - 1200 dpi when saving as image
    #   - no grid
    #   - linear x and y axis
    #
    # @param title Plot title, default: no title
    #
    def __init__(self, title=None):
        if title is not None:
            try:
                title = f"{title}"
            except Exception as e:
                raise RuntimeError(f"Unable to convert title (type {type(title)}) to string: {e}")
            # end try
        # end if

        self.__dpi = 1200
        self.__x_data = None
        self.__y_data = []
        self.__x_label = None
        self.__y_label = None
        self.__title = title
        self.__legend = []
        self.__y_limits = (0.0, None)
        self.__x_limits = (None, None)
        self.__log_x = False
        self.__log_y = False
        self.__grid = None
    # end def __init__

    ##
    # @brief set output dpi
    #
    # @param dpi DPI value to set (>0)
    #
    def set_dpi(self, dpi):
        dpi = float(dpi)
        if dpi <= 0.0:
            raise RuntimeError(f"Negative dpi value ({dpi}) not allowed.")
        self.__dpi = dpi
    # end def set_dpi

    ##
    # @brief enable grid
    #
    # @param color grid color (set to None to disable grid)
    #              see https://matplotlib.org/stable/gallery/color/named_colors.html for possible colors
    # @param style grid line style
    #
    def set_grid(self, color='darkgray', style='--'):
        if color is None:
            self.__grid = None
        else:
            self.__grid = (color, style)
    # end def set_grid

    ##
    # @brief set the X label of the plot
    #
    def set_x_label(self, label):
        if label is not None and not isinstance(label, str):
            try:
                label = f"{label}"
            except Exception as e:
                raise RuntimeError(f"Unable to convert label (type {type(label)}) to string: {e}")
            # end try
        # end if

        self.__x_label = label
    # end set_x_label

    ##
    # @brief set the Y label of the plot
    #
    def set_y_label(self, label):
        if label is not None and not isinstance(label, str):
            try:
                label = f"{label}"
            except Exception as e:
                raise RuntimeError(f"Unable to convert label (type {type(label)}) to string: {e}")
            # end try
        # end if

        self.__y_label = label
    # end set_x_label

    ##
    # @brief set the X limits of the plot
    #
    # @details
    # set the value to None to let pyplot generate the limits based on the input data.
    # Not allowed if logarithmic scale is enabled
    #
    # @param xmin lower limit
    # @param xmax upper limit
    #
    def set_x_limits(self, xmin=None, xmax=None):
        if self.__log_x:
            raise RuntimeError("Limits not allowed for logarithmic axes.")

        if xmin is not None:
            xmin = float(xmin)
        if xmax is not None:
            xmax = float(xmax)
        self.__y_limits = (xmin, xmax)
    # end def set_x_limits

    ##
    # @brief set the Y limits of the plot
    #
    # @details
    # set the value to None to let pyplot generate the limits based on the input data.
    # Not allowed if logarithmic scale is enabled
    #
    # @param ymin lower limit
    # @param ymax upper limit
    #
    def set_y_limits(self, ymin=0.0, ymax=None):
        if self.__log_y:
            raise RuntimeError("Limits not allowed for logarithmic axes.")

        if ymin is not None:
            ymin = float(ymin)
        if ymax is not None:
            ymax = float(ymax)
        self.__y_limits = (ymin, ymax)
    # end def set_y_limits

    def save(self, filename):
        pass
    # end def save

    ##
    # @brief set the x-axis values
    #
    # @details
    # An already set x data set will be overwritten!
    # If there are already y_data sets added, the x data set must have the same length as the y data sets.
    # If at least one value is beyond the set limits, the limit will be removed.
    #
    # @param x_data the new x data set
    #
    def set_x_data(self, x_data):
        if type(x_data) is not list and type(x_data) is not tuple:
            raise RuntimeError(f"x_data is neither list nor tuple, but {type(x_data)}")

        if len(x_data) <= 0:
            raise RuntimeError(f"x_data is empty")

        if len(self.__y_data) > 0:
            if len(x_data) != len(self.__y_data[0]):
                raise RuntimeError(f"Each y data set must be of the same length as the x data set: "
                                  f"{len(self.__y_data[0])} != {len(x_data)}")

        if self.__x_limits[0] is not None:
            m = min(x_data)
            if m < self.__x_limits[0]:
                self.__x_limits = (None, self.__x_limits[1])

        if self.__x_limits[1] is not None:
            m = max(x_data)
            if m > self.__x_limits[0]:
                self.__x_limits = (self.__x_limits[0], None)

        self.__x_data = x_data
    # end def set_x_data

    ##
    # @brief adds a new y data set
    #
    # @details
    # If at least one value is beyond the set limits, the limit will be removed.
    #
    # #param y_data the y data set to add
    #
    def add_y_data(self, y_data, label=None):
        if type(y_data) is not list and type(y_data) is not tuple:
            raise RuntimeError(f"y_data entry is neither list nor tuple, but {type(y_data)}")

        if self.__x_data is not None:
            if len(y_data) != len(self.__x_data):
                raise RuntimeError(f"Each y data set must be of the same length as the x data set: "
                                   f"{len(y_data)} != {len(self.__x_data)}")
        elif len(self.__y_data) > 0:
            if len(y_data) != len(self.__y_data[0]):
                raise RuntimeError(f"All y data sets must have the same length: {len(y_data)} != {len(self.__y_data[0])}")

        if label is not None:
            label = f"{label}"

        if self.__y_limits[0] is not None:
            m = min(y_data)
            if m < self.__y_limits[0]:
                self.__y_limits = (None, self.__y_limits[1])

        if self.__y_limits[1] is not None:
            m = max(y_data)
            if m > self.__y_limits[0]:
                self.__y_limits = (self.__y_limits[0], None)

        self.__legend.append(label)
        self.__y_data.append(y_data)
    # end def add_y_data

    ##
    # @brief adds multiple new y data sets
    #
    def add_y_sets(self, y_list, y_labels=None):
        if type(y_list) is not list and type(y_list) is not tuple:
            raise RuntimeError(f"y_list entry is neither list nor tuple, but {type(y_list)}")

        if y_labels is not None:
            if type(y_labels) is not list and type(y_labels) is not tuple:
                raise RuntimeError(f"y_labels entry is neither list nor tuple, but {type(y_labels)}")

            if len(y_labels) != len(y_list):
                raise RuntimeError(f"There must be one label per y data set: {len(y_labels)} != {len(y_list)}")
        # end if

        for i in range(len(y_list)):
            label = None
            if y_labels is not None:
                label = y_labels[i]

            self.add_y_data(y_list[i], label)
        # end for
    # end def add_y_sets

    ##
    # @brief enable/disable log scale
    #
    # @details
    # Removes all axis limits if enabled
    #
    def set_log_scale(self, x=False, y=False):
        x = bool(x)
        y = bool(y)
        self.__log_x = x
        self.__log_y = y

        if x:
            self.__x_limits = (None, None)
        if y:
            self.__y_limits = (None, None)
    # end def set_log_scale

    ##
    # @brief creates the plot
    #
    # @details
    # The plot is either saved as an image file or displayed.
    #
    # @param filename path of the file to save the plot. The plot will be displayed if set to None
    #
    def create(self, filename=None):
        if self.__x_data is None:
            raise RuntimeError("No x data set")
        # end if

        if self.__y_data is None:
            raise RuntimeError("No y data set")
        # end if

        if filename is not None and not check_file_writable(filename):
            raise RuntimeError(f"File '{filename}' can't be created/written")
        # end if

        use_legend = any(elem is not None for elem in self.__legend)
        for i in range(len(self.__legend)):
            if self.__legend[i] is None:
                self.__legend[i] = ''
            # end if
        # end for

        lines = []
        fig, ax = plt.subplots()

        for i in range(len(self.__y_data)):
            l, = ax.plot(self.__x_data, self.__y_data[i], label=self.__legend[i])
            lines.append(l)
        # end for

        if use_legend:
            ax.legend(handles=lines)
        # end if

        if not self.__log_x:
            ax.set_xlim(self.__x_limits)
        else:
            ax.set_xscale('log')
        # end if

        if not self.__log_y:
            ax.set_ylim(self.__y_limits)
        else:
            ax.set_yscale('log')
        # end if

        if self.__x_label is not None:
            ax.set_xlabel(self.__x_label)
        # end if

        if self.__y_label is not None:
            ax.set_ylabel(self.__y_label)
        # end if

        if self.__title is not None:
            ax.set_title(self.__title)
        # end if

        if self.__grid is not None:
            ax.grid(color=self.__grid[0], linestyle=self.__grid[1])
        # end if

        if filename is not None:
            plt.savefig(filename, dpi=self.__dpi)
        else:
            plt.show()
        # end if
    # end def create

# end class SimplePlot
