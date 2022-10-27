#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2022 gq <gq@laceap1>
#
# Distributed under terms of the MIT license.

"""

"""

import flet
from flet import Page, Text, Row, ElevatedButton,\
    Container, colors, Column, ButtonStyle, Image, Dropdown, dropdown, \
    FilledButton
from flet.buttons import CircleBorder
from control import set_spt1, set_spt2, set_spt3, set_spt4, set_spt5, \
    set_relay, all_relay_off, i2c_relay
from datetime import date
import logging
import sys


today_str = date.today().strftime("%Y-%m-%d")
log_file = today_str +'.log'

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s: %(message)s",
                          datefmt="%Y-%m-%d - %H:%M:%S")
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
fh = logging.FileHandler(log_file, "w")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(ch)
log.addHandler(fh)


option_changed = False
input_sel = -1
ap_sel = -1
output_sel = -1
ap_internal_sel = -1
ap_out_sel = -1
relay_sel = -1
Is_input_selected = False
Is_dev_selected = False
Is_output_selected = False
all_powr_down = True



def main(page: Page):
    # all_relay_off()


    header_img = Image(
        src="imgs/choose_wisely.jpeg",
        width=620,
        height=260,
        fit="fitWidth"
    )

    page.title = "低频全天总功率实验控制系统"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    page_t = Text(page.title, size=70)

    t1 = Text(value="输入：?", size=14)
    t2 = Text(value="放大器: ?", size=14)
    t3 = Text(value="输入：?", size=14)

    def input_changed(e):
        global Is_input_selected, input_sel, option_changed
        t1.value = f"输入：{dd_input.value}"

        option_changed=True

        Is_input_selected = True
        if "RF输入1" in t1.value:
            input_sel = 4
        elif "RF输入2" in t1.value:
            input_sel = 3
        elif "RF输入3" in t1.value:
            input_sel = 2
        elif "RF输入4" in t1.value:
            input_sel = 1

        power_up_button.icon="play_circle"
        power_up_button.text="上电"
        power_up_button.icon_color=colors.GREEN
        page.update()

    def ap_dev_changed(e):
        global Is_dev_selected, ap_sel, ap_out_sel, ap_internal_sel, \
            relay_sel, option_changed
        t2.value=f"放大器：{dd_ap.value}"

        option_changed=True
        Is_dev_selected = True
        if "1#" in t2.value:
            ap_sel = 4
            ap_out_sel = 2
            ap_internal_sel = -1
            if i2c_relay:
                relay_sel = 1
            else:
                relay_sel = 3
        elif "2#" in t2.value:
            ap_sel = 1
            ap_out_sel = 4
            ap_internal_sel = -1
            if i2c_relay:
                relay_sel = 3
            else:
                relay_sel = 1
        elif "3#" in t2.value:
            ap_sel = 3
            ap_out_sel = 1
            ap_internal_sel = 1

            relay_sel = 2
        elif "4#" in t2.value:
            ap_sel = 3
            ap_out_sel = 3
            ap_internal_sel = 4
            relay_sel = 2
        elif "5#" in t2.value:
            ap_sel = 2
            ap_out_sel = -1
            ap_internal_sel = -1

        power_up_button.icon="play_circle"
        power_up_button.text="上电"
        power_up_button.icon_color=colors.GREEN
        page.update()

    def output_changed(e):
        global Is_output_selected, output_sel, option_changed
        t3.value=f"输出：{dd_output.value}"

        option_changed=True
        Is_output_selected = True
        if "输出1" in t3.value:
            output_sel = 4
        elif "输出2" in t3.value:
            output_sel = 3
        else:
            output_sel = -1

        power_up_button.icon="play_circle"
        power_up_button.text="上电"
        power_up_button.icon_color=colors.GREEN
        page.update()

    dd_input = Dropdown(
        on_change=input_changed,
        label="输入选择",
        width=200,
        options=[
            dropdown.Option("RF输入1(带低噪放)"),
            dropdown.Option("RF输入2"),
            dropdown.Option("RF输入3"),
            dropdown.Option("RF输入4(RF+DC)"),
        ],
        autofocus=True

    )

    dd_ap = Dropdown(
        on_change=ap_dev_changed,
        label="放大器选择",
        width=200,
        options=[
            dropdown.Option("1# LACE自制"),
            dropdown.Option("2# LACE定制"),
            dropdown.Option("3# 西电60DB"),
            dropdown.Option("4# 西电80DB"),
            dropdown.Option("5# 矢网R60")
        ],
        autofocus=True
    )

    dd_output = Dropdown(
        on_change=output_changed,
        label="输出选择",
        width=200,
        options=[
            dropdown.Option("输出1"),
            dropdown.Option("输出2(不带滤波)"),
            dropdown.Option("矢网测量无输出"),
        ],
        autofocus=True
    )
    ap_input = Container(content=Column([
        dd_input, t1]),
         bgcolor=colors.GREEN,
         padding=20,
         width=240,
         height=150)

    ap_devs = Container(content=Column(
        [dd_ap, t2]),
         width=240,
         height=150,
         bgcolor=colors.RED,
         padding=20)

    ap_output = Container(content=Column(
        [dd_output, t3]),
         width=240,
         height=150,
         bgcolor=colors.BLUE,
         padding=20)

    status = Text(" ", size=16)
    def power_click(e):
        global all_powr_down, ap_sel, input_sel, ap_internal_sel, \
            ap_out_sel, output_sel, relay_sel

        # active channels
        # input_sel

        log.info(f"input_sel: {input_sel}, ap_sel: {ap_sel} " + \
              f"ap_internal_sel: {ap_internal_sel} " + \
              f"ap_out_sel: {ap_internal_sel} " + \
              f"output_sel: {output_sel}")

        set_spt1(input_sel)

        # set for ap_sel
        set_spt2(ap_sel)
        if ap_out_sel > 0:
            set_spt4(ap_out_sel)

        if ap_internal_sel > 0:
            set_spt3(ap_internal_sel)

        # set for output_sel
        set_spt5(output_sel)

        if (Is_output_selected and Is_input_selected and Is_dev_selected):
            if power_up_button.icon == "pause_circle":
                power_up_button.icon="play_circle"
                power_up_button.text="上电"
                power_up_button.icon_color=colors.GREEN
                all_powr_down = True

                all_relay_off()

                stop_button.text="已断电"
                stop_button.style.bgcolor[""]=colors.GREEN
            else:
                all_powr_down = False
                power_up_button.icon="pause_circle"
                power_up_button.text="断电"
                power_up_button.icon_color=colors.RED

                stop_button.text="全部断电"
                stop_button.style.bgcolor[""]=colors.RED

                set_relay(relay_sel)

            status.value = "You chose wisely"
        else:
            status.value = "You chose poorly, something is missing"

        page.update()

    def stop_all(e):
        global all_powr_down
        if not all_powr_down:
            all_powr_down = True
            power_up_button.icon="play_circle"
            power_up_button.text="上电"
            power_up_button.icon_color=colors.GREEN

            stop_button.text="已断电"
            stop_button.style.bgcolor[""]=colors.GREEN

        page.update()

        all_relay_off()


    power_up_button = FilledButton(text="上电",
                                   icon="play_circle",
                                   icon_color=colors.GREEN,
                                   on_click=power_click,
                                   data=False)
    stop_button = ElevatedButton(
            "已断电",
            style=ButtonStyle(shape=CircleBorder(), padding=30,
                              bgcolor={"":colors.GREEN},
                              color={"":colors.BLACK}),
        on_click=stop_all
        )

    page.add(page_t, header_img, Row([ap_input, ap_devs, ap_output],
                                     alignment="center"),
             Row([power_up_button, stop_button], alignment="center"),
             status
             )



flet.app(port=80, target=main, view=flet.WEB_BROWSER,
         assets_dir="assets")

