from manimlib.imports import *
from sanim import *

class Tables(Scene):
    def construct(self):
        tabledict={
            TextMobject("Income Statement"):[TextMobject("Revenue"),TextMobject("Costs"),TextMobject("Depre"),TextMobject("Lease costs.")],
            TexMobject("TexMobject Input"):[TexMobject(r"e^{\iota\pi}+1 = 0"),TexMobject(r"Tex: \alpha\theta\epsilon")],
            "Raw String Input":["Defaults","to","TextMobject."],
            Text("Text input",font="Lucida Grande"):[Text("Text",font="Alys Script Bold"),Text("is",font="serif"),Text("Supported",font="serif")],

        }

        x1 = TexMobject(r'1000').scale(0.7)
        y1 = TexMobject(r'500').scale(0.7)
        m1 = TexMobject(r'200').scale(0.7)
        table=Table(tabledict=tabledict,buff_length=0.3,line_color=GRAY,raw_string_color=BLUE)
        table.scale(0.5)

        self.play(Write(table),run_time=2)

        self.play(Write(table.add_record(record=x1,field_num=0)))

        self.play(table.adjust_lines())

        self.play(Uncreate(table.remove_record(field_num=1,record_num=0)))

        self.play(table.adjust_positions())

        self.play(Write(table.add_field(DecimalNumber(3.14))))

        self.play(table.adjust_lines())

        self.play(
            table.get_record(0,2).set_color,BLUE,
            table.get_field(0).set_color,GREEN,

        )

        self.play(table.scale,0.75,
        table.shift,LEFT)


        self.wait(1)
