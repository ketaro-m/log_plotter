#!/usr/bin/env python
import numpy
import struct
import math
import sys

try:
    import pyqtgraph
except:
    print "please install pyqtgraph. see http://www.pyqtgraph.org/"
    sys.exit(1)

class PlotMethod(object):
    urata_len = 16
    # color_list = pyqtgraph.functions.Colors.keys()
    # default color set on gnuplot 5.0
    color_list = ["9400D3", "009E73", "56B4E9", "E69F00", "F0E442", "0072B2", "E51E10", "0000FF"]
    linetypes = {
        "color": color_list * 2,
        "style": [pyqtgraph.QtCore.Qt.SolidLine] * len(color_list) + [pyqtgraph.QtCore.Qt.DotLine] * len(color_list)
        # "style": [pyqtgraph.QtCore.Qt.SolidLine] + [pyqtgraph.QtCore.Qt.DotLine] + [pyqtgraph.QtCore.Qt.DashLine] + [pyqtgraph.QtCore.Qt.DashDotLine]
    }


    @staticmethod
    def __plot_urata_servo(plot_item, times, data_dict, logs, log_cols, cur_col, key, i, offset1, offset2=1):
        plot_item.plot(times, data_dict[logs[0]][:, (PlotMethod.urata_len+1) * log_cols[0] + (offset1+offset2)],
                       pen=pyqtgraph.mkPen(PlotMethod.linetypes["color"][i], width=1.5, style=PlotMethod.linetypes["style"][i]), name=key)

    @staticmethod
    def plot_servostate(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        def RePack(x):
            val = struct.unpack('i', struct.pack('f', float(x)))[0]
            #calib = (val & 0x01)
            #servo = (val & 0x02) >> 1
            #power = (val & 0x04) >> 2
            state = (val & 0x0007fff8) >> 3
            #temp  = (val & 0xff000000) >> 24
            return state
        vfr = numpy.vectorize(RePack)
        plot_item.plot(times, vfr(data_dict[logs[0]][:, (PlotMethod.urata_len+1) * log_cols[0] + (0+0)]),
                       pen=pyqtgraph.mkPen('r', width=1.5, style=PlotMethod.linetypes["style"][i]), name=key)

    @staticmethod
    def plot_commnormal(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        PlotMethod.__plot_urata_servo(plot_item, times, data_dict, logs, log_cols, cur_col, key, i, 13)

    @staticmethod
    def plot_12V(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        PlotMethod.__plot_urata_servo(plot_item, times, data_dict, logs, log_cols, cur_col, key, i, 9)

    @staticmethod
    def plot_80V(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        PlotMethod.__plot_urata_servo(plot_item, times, data_dict, logs, log_cols, cur_col, key, i, 2)

    @staticmethod
    def plot_current(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        PlotMethod.__plot_urata_servo(plot_item, times, data_dict, logs, log_cols, cur_col, key, i, 1)

    @staticmethod
    def plot_motor_temp(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        PlotMethod.__plot_urata_servo(plot_item, times, data_dict, logs, log_cols, cur_col, key, i, 0)

    @staticmethod
    def plot_motor_outer_temp(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        PlotMethod.__plot_urata_servo(plot_item, times, data_dict, logs, log_cols, cur_col, key, i, 7)

    @staticmethod
    def plot_pgain(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        PlotMethod.__plot_urata_servo(plot_item, times, data_dict, logs, log_cols, cur_col, key, i, 10)

    @staticmethod
    def plot_dgain(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        PlotMethod.__plot_urata_servo(plot_item, times, data_dict, logs, log_cols, cur_col, key, i, 11)

    @staticmethod
    def plot_abs_enc(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        plot_item.plot(times, [math.degrees(x) for x in data_dict[logs[0]][:, (PlotMethod.urata_len+1) * log_cols[0] + (6+1)]],
                       pen=pyqtgraph.mkPen('g', width=1.5, style=PlotMethod.linetypes["style"][i]), name=key)

    @staticmethod
    def plot_rh_q_st_q(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        plot_item.plot(times, [math.degrees(x) for x in (data_dict[logs[1]][:, log_cols[1]] - data_dict[logs[0]][:, log_cols[0]])],
                       pen=pyqtgraph.mkPen('r', width=1.5, style=PlotMethod.linetypes["style"][i]), name=key)

    @staticmethod
    def plot_rad2deg(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        data_rad=data_dict[logs[0]][:, log_cols[0]]
        data_deg=[math.degrees(x) for x in data_rad]
        plot_item.plot(times, data_deg,pen=pyqtgraph.mkPen(PlotMethod.linetypes["color"][i], width=1.5, style=PlotMethod.linetypes["style"][i]), name=key)

    @staticmethod
    def plot_watt(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        joint_vel=data_dict[logs[0]][:, log_cols[0]]
        joint_tau=data_dict[logs[1]][:, log_cols[1]]
        watt=joint_vel*joint_tau
        plot_item.plot(times, watt,pen=pyqtgraph.mkPen(PlotMethod.linetypes["color"][i], width=1.5, style=PlotMethod.linetypes["style"][i]), name=key, fillLevel=0, fillBrush=PlotMethod.linetypes["color"][i])

    @staticmethod
    def plot_diff(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        data_minuend = data_dict[logs[0]][:, log_cols[0]]
        data_subtrahend = data_dict[logs[1]][:, log_cols[1]]
        data = data_minuend - data_subtrahend
        plot_item.plot(times, data, pen=pyqtgraph.mkPen(PlotMethod.linetypes["color"][i], width=1.5, style=PlotMethod.linetypes["style"][i]), name=key)

    @staticmethod
    def plot_rad2deg_diff(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        plot_item.plot(times, [math.degrees(x) for x in (data_dict[logs[1]][:, log_cols[1]] - data_dict[logs[0]][:, log_cols[0]])],
                       pen=pyqtgraph.mkPen('r', width=1.5, style=PlotMethod.linetypes["style"][i]), name=key)

    @staticmethod
    def plot_comp(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        plot_item.plot(times, data_dict[logs[0]][:, log_cols[0]],
                       pen=pyqtgraph.mkPen(PlotMethod.linetypes["color"][i], width=1.5, style=PlotMethod.linetypes["style"][i]), name=key)
        if log_cols[0] % 6 < 3: # position
            plot_item.setYRange(-0.025, +0.025) # compensation limit
        else: # rotation
            plot_item.setYRange(math.radians(-10), math.radians(+10)) # compensation limit

    @staticmethod
    def plot_COP(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        offset = log_cols[0]*6
        arg = logs[min(len(logs)-1,cur_col)]
        f_z = data_dict[arg][:, offset+2]
        tau_x = data_dict[arg][:, offset+3]
        tau_y = data_dict[arg][:, offset+4]
        plot_item.plot(times, -tau_y/f_z, pen=pyqtgraph.mkPen(PlotMethod.color_list[2*i], width=1.5, style=PlotMethod.linetypes["style"][i]), name=key)
        plot_item.plot(times,  tau_x/f_z, pen=pyqtgraph.mkPen(PlotMethod.color_list[2*i+1], width=1.5, style=PlotMethod.linetypes["style"][i]), name=key)

    @staticmethod
    def plot_inverse(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        plot_item.plot(times, -data_dict[logs[0]][:, log_cols[0]], pen=pyqtgraph.mkPen(PlotMethod.linetypes["color"][i], width=1.5, style=PlotMethod.linetypes["style"][i]), name=key)

    @staticmethod
    def plot_time(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        plot_item.plot(times, numpy.append([0], numpy.diff(times)), pen=pyqtgraph.mkPen(PlotMethod.linetypes["color"][i], width=1.5, style=PlotMethod.linetypes["style"][i]), name=key)

    @staticmethod
    def normal(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        plot_item.plot(times, data_dict[logs[0]][:, log_cols[0]], pen=pyqtgraph.mkPen(PlotMethod.linetypes["color"][i], width=1.5, style=PlotMethod.linetypes["style"][i]), name=key)

    @staticmethod
    def plot_add(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        data_summand = data_dict[logs[0]][:, log_cols[0]]
        data_addend = data_dict[logs[1]][:, log_cols[1]]
        data = data_summand + data_addend
        plot_item.plot(times, data, pen=pyqtgraph.mkPen(PlotMethod.linetypes["color"][i], width=1.5, style=PlotMethod.linetypes["style"][i]), name=key)

    @staticmethod
    def plot_add_const(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        data_summand = data_dict[logs[0]][:, log_cols[0]]
        data_addend = -0.045873
        data = data_summand + data_addend
        plot_item.plot(times, data, pen=pyqtgraph.mkPen(PlotMethod.linetypes["color"][i], width=1.5, style=PlotMethod.linetypes["style"][i]), name=key)

    @staticmethod
    def plot_cp(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        cogx = data_dict[logs[0]][:, log_cols[0]] # cog x
        height = data_dict[logs[1]][:, log_cols[1]] # cog height
        vel = data_dict[logs[2]][:, log_cols[2]]    # cog velocity
        g = 9.80665
        omega = numpy.sqrt(g / height)
        data = vel / omega + cogx
        plot_item.plot(times, data, pen=pyqtgraph.mkPen(PlotMethod.linetypes["color"][i], width=1.5, style=PlotMethod.linetypes["style"][i]), name=key)

    @staticmethod
    def plot_cp_add_const(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        cogx = data_dict[logs[0]][:, log_cols[0]] # cog x
        height = data_dict[logs[1]][:, log_cols[1]] # cog height
        vel = data_dict[logs[2]][:, log_cols[2]]    # cog velocity
        g = 9.80665
        omega = numpy.sqrt(g / height)
        data_addend = -0.0184
        data = vel / omega + cogx + data_addend
        plot_item.plot(times, data, pen=pyqtgraph.mkPen(PlotMethod.linetypes["color"][i], width=1.5, style=PlotMethod.linetypes["style"][i]), name=key)

    @staticmethod
    def plot_cp_diff(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        actcogx = data_dict[logs[0]][:, log_cols[0]] # cog x
        refcogx = data_dict[logs[3]][:, log_cols[3]] # cog x
        actheight = data_dict[logs[1]][:, log_cols[1]] # cog height
        refheight = data_dict[logs[4]][:, log_cols[4]] # cog height
        actvel = data_dict[logs[2]][:, log_cols[2]]    # cog velocity
        refvel = data_dict[logs[5]][:, log_cols[5]]    # cog velocity
        g = 9.80665
        actomega = numpy.sqrt(g / actheight)
        refomega = numpy.sqrt(g / refheight)
        data = (actvel / actomega + actcogx)  - (refvel / refomega + refcogx)
        plot_item.plot(times, data, pen=pyqtgraph.mkPen(PlotMethod.linetypes["color"][i], width=1.5, style=PlotMethod.linetypes["style"][i]), name=key)

    @staticmethod
    def plot_cog_with_sbp(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        M = 130.442
        g = 9.80665
        cogx = data_dict[logs[0]][:, log_cols[0]]
        cog_offset = data_dict[logs[0]][0, log_cols[0]]
        rleg_posx = data_dict[logs[1]][:, log_cols[1]] / 1000.0
        lleg_posx = data_dict[logs[2]][:, log_cols[2]] / 1000.0
        rleg_forcez = data_dict[logs[3]][:, log_cols[3]]
        lleg_forcez = data_dict[logs[4]][:, log_cols[4]]
        data = cogx + cogx - (M * g * cogx - rleg_posx * rleg_forcez - lleg_posx * lleg_forcez) / (M * g - rleg_forcez - lleg_forcez) - cog_offset
        plot_item.plot(times, data, pen=pyqtgraph.mkPen(PlotMethod.linetypes["color"][i], width=1.5, style=PlotMethod.linetypes["style"][i]), name=key)

    @staticmethod
    def plot_sbp_cog_offset(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        M = 130.442
        g = 9.80665
        cogx = data_dict[logs[0]][:, log_cols[0]]
        rleg_posx = data_dict[logs[1]][:, log_cols[1]] / 1000.0
        lleg_posx = data_dict[logs[2]][:, log_cols[2]] / 1000.0
        rleg_forcez = data_dict[logs[3]][:, log_cols[3]]
        lleg_forcez = data_dict[logs[4]][:, log_cols[4]]
        data = cogx - (M * g * cogx - rleg_posx * rleg_forcez - lleg_posx * lleg_forcez) / (M * g - rleg_forcez - lleg_forcez)
        plot_item.plot(times, data, pen=pyqtgraph.mkPen(PlotMethod.linetypes["color"][i], width=1.5, style=PlotMethod.linetypes["style"][i]), name=key)

    @staticmethod
    def plot_with_offset(plot_item, times, data_dict, logs, log_cols, cur_col, key, i):
        offset = data_dict[logs[0]][0, log_cols[0]]
        data = data_dict[logs[0]][:, log_cols[0]] - offset
        plot_item.plot(times, data, pen=pyqtgraph.mkPen(PlotMethod.linetypes["color"][i], width=1.5, style=PlotMethod.linetypes["style"][i]), name=key)
