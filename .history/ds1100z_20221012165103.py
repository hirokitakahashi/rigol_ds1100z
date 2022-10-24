# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 12:59:10 2022

@author: HIROKI-TAKAHASHI
"""

import pyvisa as pv
import numpy as np


def open_first_device():
    scope = DS1100Z()
    rsc = scope.get_resources()
    scope.open(rsc[0])
    return scope


class DS1100Z:
    def __init__(self, resource_name=""):
        self.rm = pv.ResourceManager()
        if resource_name:
            self.open(resource_name)

    def get_resources(self):
        rsc = self.rm.list_resources()
        self.resources = rsc
        print(rsc)
        return rsc

    def open(self, resource_name=""):
        if resource_name == "":
            print("No resource name given!")
            self.inst = None
        else:
            self.inst = self.rm.open_resource(resource_name)

    def close(self):
        if self.rm:
            self.rm.close()
        if self.inst:
            self.inst.close()

    def encode_ch_str(self, ch_num):
        if ch_num >= 1 and ch_num <= 4:
            ch_str = ":CHAN{:d}".format(ch_num)
            return ch_str
        else:
            raise Exception("Channel number out of range!")

    def run(self):
        if self.inst:
            self.inst.write(":RUN")

    def stop(self):
        if self.inst:
            self.inst.write(":STOP")

    def single(self):
        if self.inst:
            self.inst.write(":SING")

    # Timebase functions
    def inquire_time_settings(self, display=True):
        if self.inst:
            delay_ena = self.inst.query(":TIM:DEL:ENA?")
            delay_ofs = self.inst.query(":TIM:DEL:OFFS?")
            delay_scl = self.inst.query(":TIM:DEL:SCAL?")
            main_ofs = self.inst.query(":TIM:MAIN:OFFS?")
            main_scl = self.inst.query(":TIM:MIAN:SCAL?")
            time_mode = self.inst.query(":TIM:MODE?")
            if display:
                print(
                    "Delay enabled: "
                    + delay_ena
                    + "Delay offset: "
                    + delay_ofs
                    + "Delay scale: "
                    + delay_scl
                    + "Main offset: "
                    + main_ofs
                    + "Main scl: "
                    + main_scl
                    + "Time mode: "
                    + time_mode
                )
        else:
            print("Instrument not open!")
            return

    def get_time_scale(self):
        if self.inst:
            tscl = self.inst.query(":TIM:MAIN:SCAL?")
            return float(tscl)
        else:
            print("Instrument not open!")
            return

    def set_time_scale(self, tscl):
        if self.inst:
            self.inst.write(":TIM:MAIN:SCAL {:g}".format(tscl))
        else:
            print("Instrument not open!")
            return

    def get_time_offset(self):
        if self.inst:
            tofs = self.inst.query(":TIM:MAIN:OFFS?")
            return float(tofs)
        else:
            print("Instrument not open!")
            return

    def set_time_offset(self, tofs):
        if self.inst:
            self.inst.write(":TIM:MAIN:OFFS {:g}".format(tofs))
        else:
            print("Instrument not open!")
            return

    # Channel settings functions
    def inquire_ch_settings(self, ch_num, display=True):
        ch_str = self.encode_ch_str(ch_num)
        if self.inst:
            cpl = self.inst.query(ch_str + ":COUP?")
            disp = self.inst.query(ch_str + ":DISP?")
            inv = self.inst.query(ch_str + ":INV?")
            ofs = self.inst.query(ch_str + ":OFFS?")
            rng = self.inst.query(ch_str + ":RANG?")
            tcal = self.inst.query(ch_str + ":TCAL?")
            scl = self.inst.query(ch_str + ":SCAL?")
            prb = self.inst.query(ch_str + ":PROB?")
            unt = self.inst.query(ch_str + ":UNIT?")
            vrn = self.inst.query(ch_str + ":VERN?")
            if display:
                print(
                    "Coupling: "
                    + cpl
                    + "Display: "
                    + disp
                    + "Inverted: "
                    + inv
                    + "Offset: "
                    + ofs
                    + "Range: "
                    + rng
                    + "TCal: "
                    + tcal
                    + "Scale: "
                    + scl
                    + "Probe: "
                    + prb
                    + "Unit: "
                    + unt
                    + "Vernier: "
                    + vrn
                )
        else:
            print("Instrument not open!")
            return

    def get_ch_scale(self, ch_num):
        ch_str = self.encode_ch_str(ch_num)
        if self.inst:
            cmd = ":SCAL?"
            scl = self.inst.query(ch_str + cmd)
            return float(scl)

    def set_ch_scale(self, ch_num, scl):
        ch_str = self.encode_ch_str(ch_num)
        if self.inst:
            cmd = ":SCAL {:g}".format(scl)
            self.inst.write(ch_str + cmd)
        else:
            print("Instrument not open!")
            return

    def get_ch_offset(self, ch_num):
        ch_str = self.encode_ch_str(ch_num)
        if self.inst:
            cmd = ":OFFS?"
            ofs = self.inst.query(ch_str + cmd)
            return float(ofs)

    def set_ch_offset(self, ch_num, ofs):
        ch_str = self.encode_ch_str(ch_num)
        if self.inst:
            cmd = ":OFFS {:g}".format(ofs)
            self.inst.write(ch_str + cmd)
        else:
            print("Instrument not open!")
            return

    def get_ch_invert(self, ch_num):
        ch_str = self.encode_ch_str(ch_num)
        if self.inst:
            cmd = ":INV?"
            inv = self.inst.query(ch_str + cmd)
            return bool(inv)

    def set_ch_invert(self, ch_num, inv):
        ch_str = self.encode_ch_str(ch_num)
        if self.inst:
            if inv:
                cmd = ":INV ON"
            else:
                cmd = ":INV OFF"
            self.inst.write(ch_str + cmd)
        else:
            print("Instrument not open!")
            return

    def get_ch_probe(self, ch_num):
        ch_str = self.encode_ch_str(ch_num)
        if self.inst:
            cmd = ":PROB?"
            prb = self.inst.query(ch_str + cmd)
            return float(prb)

    def set_ch_probe(self, ch_num, prb):
        ch_str = self.encode_ch_str(ch_num)
        prb_values = [
            0.01,
            0.02,
            0.05,
            0.1,
            0.2,
            0.5,
            1,
            2,
            5,
            10,
            20,
            50,
            100,
            200,
            500,
            1000,
        ]
        if prb in prb_values:
            cmd = ":PROB {:g}".format(prb)
            self.inst.write(ch_str + cmd)
        else:
            print("Instrument not open!")
            return

    # Trigger functions
    def inquire_trig_settings(self, display=True):
        if self.inst:
            trig_mode = self.inst.query(":TRIG:MODE?")
            trig_cpl = self.inst.query(":TRIG:COUP?")
            trig_stat = self.inst.query(":TRIG:STAT?")
            trig_swp = self.inst.query(":TRIG:SWE?")
            trig_hld = self.inst.query(":TRIG:HOLD?")
            trig_nrj = self.inst.query(":TRIG:NREJ?")
            trig_src = self.inst.query(":TRIG:EDG:SOUR?")
            trig_slp = self.inst.query(":TRIG:EDG:SLOP?")
            trig_lvl = self.inst.query(":TRIG:EDG:LEV?")
            if display:
                print(
                    "Trigger mode: "
                    + trig_mode
                    + "Trigger coupling: "
                    + trig_cpl
                    + "Trigger status: "
                    + trig_stat
                    + "Trigger sweep: "
                    + trig_swp
                    + "Trigger holdoff: "
                    + trig_hld
                    + "Trigger noise reject: "
                    + trig_nrj
                    + "Trigger source: "
                    + trig_src
                    + "Trigger slope: "
                    + trig_slp
                    + "Trigger level: "
                    + trig_lvl
                )
        else:
            print("Instrument not open!")
            return

    def get_trig_status(self):
        if self.inst:
            trig_stat = self.inst.query(":TRIG:STAT?")
            return trig_stat.strip()
        else:
            print("Instrument not open!")
            return

    def get_trig_mode(self):
        if self.inst:
            trig_mode = self.inst.query(":TRIG:MODE?")
            return trig_mode.strip()
        else:
            print("Instrument not open!")
            return

    def set_trig_mode(self, trig_mode):
        trig_mode_values = [
            "EDGE",
            "PULS",
            "RUNT",
            "WIND",
            "NEDG",
            "SLOP",
            "VID",
            "PATT",
            "DEL",
            "TIM",
            "DUR",
            "SHOL",
            "RS232",
            "IIC",
            "SPI",
        ]
        if self.inst:
            if trig_mode in trig_mode_values:
                self.inst.write(":TRIG:MODE " + trig_mode)
            else:
                print("Invalid trigger mode value!")
                return
        else:
            print("Instrument not open!")
            return

    def get_trig_sweep(self):
        if self.inst:
            trig_swp = self.inst.query(":TRIG:SWE?")
            return trig_swp.strip()
        else:
            print("Instrument not open!")
            return

    def set_trig_sweep(self, trig_swp):
        trig_swp_values = ["AUTO", "NORM", "SING"]
        if self.inst:
            if trig_swp in trig_swp_values:
                self.inst.write(":TRIG:SWE " + trig_swp)
            else:
                print("Invalid trigger sweep value!")
                return
        else:
            print("Instrument not open!")
            return

    def get_trig_source(self):
        if self.inst:
            trig_src = self.inst.query(":TRIG:EDG:SOUR?")
            return trig_src.strip()
        else:
            print("Instrument not open!")
            return

    def set_trig_source(self, src):
        trig_src_values = [
            "D0",
            "D1",
            "D2",
            "D3",
            "D4",
            "D5",
            "D6",
            "D7",
            "D8",
            "D9",
            "D10",
            "D11",
            "D12",
            "D13",
            "D14",
            "D15",
            "CHAN1",
            "CHAN2",
            "CHAN3",
            "CHAN4",
            "AC",
        ]
        if self.inst:
            if src in trig_src_values:
                self.inst.write(":TRIG:EDG:SOUR " + src)
            if src in [1, 2, 3, 4]:
                # src is a channel number
                self.inst.write(":TRIG:EDG:SOUR " + "CHAN{:d}".format(src))
            else:
                print("Invalid trigger source value!")
                return
        else:
            print("Instrument not open!")
            return

    def get_trig_slope(self):
        if self.inst:
            trig_slp = self.inst.query(":TRIG:EDG:SLOP?")
            return trig_slp.strip()
        else:
            print("Instrument not open!")
            return

    def set_trig_slope(self, slp):
        trig_slp_values = ["POS", "NEG", "RFAL"]
        if self.inst:
            if slp in trig_slp_values:
                self.inst.write(":TRIG:EDG:SLOP " + slp)
            else:
                print("Invalid trigger slope value!")
                return
        else:
            print("Instrument not open!")
            return

    def get_trig_level(self):
        if self.inst:
            trig_lvl = self.inst.query(":TRIG:EDG:LEV?")
            return float(trig_lvl)
        else:
            print("Instrument not open!")
            return

    def set_trig_level(self, lvl):
        if self.inst:
            src_dict = {"CHAN1": 1, "CHAN2": 2, "CHAN3": 3, "CHAN4": 4}
            src = self.get_trig_source()
            vscale = self.get_ch_scale(src_dict[src])
            voffset = self.get_ch_offset(src_dict[src])
            llim = -5 * vscale - voffset
            ulim = 5 * vscale + voffset
            if lvl < llim or lvl > ulim:
                print("Warning: Trigger level out of range.")
            self.inst.write("TRIG:EDG:LEV {:g}".format(lvl))
        else:
            print("Instrument not open!")
            return

    # Waveform data
    def get_waveform(self, ch_num):
        if self.inst:
            src_list = ["CHAN1", "CHAN2", "CHAN3", "CHAN4"]
            src_ch = src_list[ch_num - 1]
            xinc = float(self.inst.query(":WAV:XINC?"))
            xorg = float(self.inst.query(":WAV:XOR?"))
            yinc = float(self.inst.query(":WAV:YINC?"))
            yorg = float(self.inst.query(":WAV:YOR?"))
            yref = 127
            self.inst.write(":WAV:SOUR " + src_ch)
            self.inst.write(":WAV:MODE NORM")  # get waveform on display
            self.inst.write(":WAV:FORM BYTE")
            yraw = self.inst.query_binary_values(
                ":WAV:DATA?", datatype="b", container=np.array
            )
            x = np.arange(0, len(yraw)) * xinc + xorg
            y = (yraw - yref - yorg) * yinc
            return x, y


if __name__ == "__main__":
    scope = DS1100Z()
    rsc = scope.get_resources()
    scope.open(rsc[0])
    scope.close()
