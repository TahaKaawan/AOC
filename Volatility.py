from calendar import c
from itertools import groupby
from re import X
from tkinter.constants import CENTER, GROOVE
from tokenize import group
from PyQt5.QtGui import qBlue
from manim_tutorial_P37 import RiemannRectangles
from manimlib.imports import *
from matplotlib.pyplot import arrow, axes, text, xlabel
from numpy.core.defchararray import add, center
from numpy.core.fromnumeric import size
from numpy.distutils.misc_util import yellow_text
from numpy.lib.financial import rate
from NumberCreature import *
from numpy.lib.function_base import diff
from numpy.lib.index_tricks import fill_diagonal
from sanim import *
import os
import pyclbr
from scipy.sparse import construct
from tornado.locale import get

def get_path_pending(path,proportion,dx=0.001):
    if proportion < 1:
        coord_i = path.point_from_proportion(proportion)
        coord_f = path.point_from_proportion(proportion+dx)
    else:
        coord_i = path.point_from_proportion(proportion-dx)
        coord_f = path.point_from_proportion(proportion)
    line = Line(coord_i,coord_f)
    angle = line.get_angle()
    return angle

class ShiftAndRotateAlongPath(Animation):
    CONFIG = {
        "run_time": 5,
        "rate_func": smooth,
        "dx":0.4
    }
    def __init__(self, mobject, path,**kwargs):
        assert(isinstance(mobject, Mobject))
        digest_config(self, kwargs)
        self.mobject = mobject
        self.path = path

    def interpolate_mobject(self, alpha):
        self.mobject.become(self.starting_mobject)
        self.mobject.move_to(
            self.path.point_from_proportion(alpha)
        )
        angle = get_path_pending(self.path,alpha,self.dx)
        self.mobject.rotate(
            angle,
            about_point=self.mobject.get_center(),
        )
class MoveAlongPathWithAngle2(Scene):
    def construct(self):
        path = Line(LEFT*5, RIGHT*5, stroke_opatity=0.5)
        path.points[1] += UP * 10
        path.points[2] += DOWN * 15
        start_angle = get_path_pending(path, 0)

        triangle = Dot()
        triangle.move_to(path.get_start())
       # triangle.rotate(- PI / 4)

        self.add(triangle,path)
        self.play(
                ShiftAndRotateAlongPath(triangle,path),
                run_time=4
            )
        self.wait(2)

        path2 = Line(LEFT*1, RIGHT*1, stroke_opatity=0.3)
        path2.points[1] += UP * 10
        path2.points[2] += DOWN * 8
        start_angle = get_path_pending(path2, 0)
        
        triangle2 = Dot()
        triangle2.move_to(path2.get_start())

        self.play(
                ShiftAndRotateAlongPath(triangle2,path2),
                run_time=4
            )


# playing around with functions that could give a good picture of what volatility looks like 
class stock_vol_comparison(GraphScene):
        CONFIG = {
        "y_max" : 8,
        "y_min" : 0,
        "x_max" : 7,
        "x_min" : 0,
        "y_tick_frequency" : 1,
        "x_tick_frequency" : 0.5,
        "axes_color" : BLUE,
    }
        def construct(self):
            self.setup_axes()
            graph = self.get_graph(lambda x : 4*np.sin(x)+4, color = RED)
            graph2 = self.get_graph(lambda x : 2+0.2*x, color =GREEN)

            time = TextMobject("Time")
            stock_price = TextMobject("Stock Price")

            # axis labels 
            stock_price.to_corner(LEFT+UP)
            time.to_corner(RIGHT+DOWN*2)
            
            for t in time,stock_price:
                self.play(FadeIn(t))
            # first graph 
            self.play(
            ShowCreation(graph),
            run_time = 5
        )
           # graph labels 
            high_vol = TextMobject("Volatile stock")
            low_vol = TextMobject("Low volatility stock")

            high_vol.set_color(RED)
            high_vol.scale(0.9)
            self.play(FadeIn(high_vol))
            self.wait(2)

            # 2nd graph 
            self.play(
            ShowCreation(graph2),
            run_time = 5
        )
            low_vol.set_color(GREEN)
            low_vol.scale(0.9)
            
            self.play(
            AnimationGroup(
                Transform(high_vol,low_vol),
                lag_ratio=1.2))

            self.wait()
    
            self.play(FadeOut(Group(*self.get_mobjects())))
            
           #  MathTex("{\sigma{", "T", "}}","\sigma \times \sqrt{","T","}")
            formula=TexMobject("{\sigma{", "T", "=}}","\sigma \ times","{\sqrt{", "T", " }}")
            formula.set_color_by_tex(
            "T", YELLOW) 
            formula.set_color_by_tex("sigma",RED)
            self.play(Write(formula))
            self.wait(1)
            definition = TexMobject("\sigma", "\\text{ denotes }", "\\text{ standard deviation }",".")
            definition.set_color_by_tex_to_color_map({
            "sigma": RED,
            "standard deviation":RED
        })            
            self.play(Succession(Transform(formula,definition)))
            self.wait(2)
            self.clear(definition)
            self.play(ApplyMethod(definition.to_corner,UP))
            self.wait(1)
            palabras_ale = TextMobject("its a measures of how much a stock price deviates from its average for a given period")
            Ale = Alex()
            Ale.scale(0.8)
            Ale.to_corner(LEFT+DOWN)
        
            self.play(NumberCreatureSays(
            Ale, palabras_ale, 
            bubble_kwargs = {"height" : 4, "width" : 7}, # increaesed width from 6 to 7
            target_mode="speaking"))
            self.wait(1)
            Ale.blink
            self.wait()

from math import * 
# Normal distribution of stock returns
class normald(GraphScene):
        CONFIG = {
        "y_max" : 8,
        "y_min" : 0,
        "x_max" : 7,
        "x_min" : 0,
        "y_tick_frequency" : 1,
        "x_tick_frequency" : 0.5,
        "axes_color" : BLUE,
    }
        def construct(self):
            self.setup_axes()

            def normdist(self):
                 a = 1 
                 b =0 
                 x = np.random.randint(12, size=(5))
                 f2 = np.vectorize(x)
                 y = 1/(a* np.sqrt(2*np.pi))
                 z = np.power(f2-b,2)
                 d = (2*a)**2 
                 y2= math.exp((-z)/d)
                 return y*y2 
           
            normt = self.get_graph(normdist, color = GREEN)

            self.play(
            ShowCreation(normt),
            run_time = 5)

class GraphAreaPlot(GraphScene):
    def __init__(self, **kwargs):
        GraphScene.__init__(
            self,
            x_min=0,
            x_max=7,
            y_min=0,
            y_max=6,
            x_labeled_nums=[0,2,3],
            **kwargs)

    def construct(self):
        self.setup_axes()
        curve1 = self.get_graph( lambda x,a,b: np.array([
                x,
                a,b,
                1/(a* np.sqrt(2*np.pi))*np.exp^-(((x-b)^2)/2*a^2)
            ]),a_min=-2,a_max=2,y_min=-2,y_max=2,checkerboard_colors=[BLUE_D, BLUE_E],
            resolution=(15, 32)).scale(1)

        line1 = self.get_vertical_line_to_graph(2, curve1, DashedLine, color=YELLOW)
        line2 = self.get_vertical_line_to_graph(3, curve1, DashedLine, color=YELLOW)
        area1 = self.get_area(curve1, 0.01, 4)


        for t in curve1,line1,line2,area1:
            self.play(ShowCreation(t))


class Pause(Animation):
    def __init__(self, duration):
        super().__init__(Mobject(), run_time=duration)
      # class to pause animations 
        
class numberlinevol(Scene):
    def construct(self):
        number_line=NumberLine(x_min=-6,x_max=6)
        # triangle for high standard deviation 
        triangle=RegularPolygon(3,start_angle=-PI/2)\
                   .scale(0.2)\
                   .next_to(number_line.get_left(),UP,buff=SMALL_BUFF)
        numbers= VGroup(*[
        TexMobject(fr"{i} \%")
                .next_to(number_line.get_tick(i),DOWN)  for i in range(-6,8)]
            )

        self.add(number_line)
        self.play(ShowCreation(triangle))
        self.wait(0.3)

    
        t_label = TexMobject("\\text{ High }", " \sigma").to_corner(UR)
        t_label.set_color_by_tex("\sigma",YELLOW)
        t_label.shift(LEFT)
        t_value = DecimalNumber(-5)
        t_value.next_to(t_label,aligned_edge=DOWN)      
        self.wait()
        
        t_value.add_updater(lambda d: d.set_value(triangle.get_center()[0]))

        self.add(t_label,t_value)

        
        self.play(*[AnimationGroup(
                        # Animation(Mobject(),run_time=i+1), # <- This is a pause
                        FadeIn(numbers[i]),
                    )for i in range(12)],
            )
        self.play(
                    ApplyMethod(triangle.shift,RIGHT*12,rate_func=there_and_back,run_time=4))
                    

        self.remove(triangle,t_value)

         # triangle for low standard deviation 

        number_line2=NumberLine(x_min=-3,x_max=3)
        t_value1 = DecimalNumber(-3)
       

        numbers2= VGroup(*[
        TexMobject(fr"{i} \%")
                .next_to(number_line.get_tick(i),DOWN)  for i in range(-3,4)]
            )

        self.play(
            Succession(
                Transform(number_line,number_line2),Transform(numbers,numbers2),lag_ratio=1.2
            ))

        triangle1=RegularPolygon(3,start_angle=-PI/2)\
                   .scale(0.2)\
                   .next_to(number_line.get_left(),UP,buff=SMALL_BUFF)

        t_value1.add_updater(lambda d: d.set_value(triangle1.get_center()[0]))
        t_label2 = TexMobject("\\text{ low }", " \sigma").to_corner(UR)
        t_label2.set_color_by_tex("\sigma",YELLOW)
        t_label2.shift(LEFT)
        t_value1.next_to(t_label2,aligned_edge=DOWN)      

        self.add(t_value1)

        
        self.play(
            Succession(
                Transform(t_label,t_label2)))

        self.play(
                    ApplyMethod(triangle1.shift,RIGHT*6,rate_func=there_and_back,run_time=4))
        self.wait()

class appl(Scene):
    def construct(self):
        number_line=NumberLine(x_min=-6,x_max=6)
        # triangle for GME 
        triangle=RegularPolygon(3,start_angle=-PI/2)\
                   .scale(0.2)\
                   .next_to(number_line.get_left(),UP,buff=SMALL_BUFF)
        numbers= VGroup(*[
        TexMobject(fr"{i} \%")
                .next_to(number_line.get_tick(i),DOWN)  for i in range(-6,8)]
            )

        # GME std and mean returns for the last year 
        gme = BulletedList("\\text{ $\sigma$ = 5\\% }","\\text{ average price = 10}").to_corner(LEFT+UP)
        gme.scale(0.7)

        gme1 = TexMobject("\\text{ GameStop }")
        gme1.set_color(RED)
        gme1.to_edge(UP)
        self.play(Write(gme1))

        framebox2 = SurroundingRectangle(gme, buff = .1)
        self.play(
           ShowCreation(framebox2))
        
        self.play(FadeInFrom(gme,LEFT))
       

        self.add(number_line)
        self.play(ShowCreation(triangle))
        self.wait(0.3)

    
        t_label = TexMobject("\\text{ High }", " \sigma").to_corner(UR)
        t_label.set_color_by_tex("\sigma",YELLOW)
        t_label.shift(LEFT)
        t_value = DecimalNumber(-5)
        t_value.next_to(t_label,aligned_edge=DOWN)      
        self.wait()
        
        t_value.add_updater(lambda d: d.set_value(triangle.get_center()[0]))

        self.add(t_label,t_value)

        
        self.play(*[AnimationGroup(
                        # Animation(Mobject(),run_time=i+1), # <- This is a pause
                        FadeIn(numbers[i]),
                    )for i in range(12)],
            )
        self.play(
                    ApplyMethod(triangle.shift,RIGHT*12,rate_func=there_and_back,run_time=4))
                    

        self.remove(triangle,t_value)

         # triangle for APPL  

        number_line2=NumberLine(x_min=-3,x_max=3)
        t_value1 = DecimalNumber(-3)
       

        numbers2= VGroup(*[
        TexMobject(fr"{i} \%")
                .next_to(number_line.get_tick(i),DOWN)  for i in range(-3,4)]
            )

        appl = BulletedList("\\text{ $\sigma$ = 2\\% }","\\text{ average price = \\$200 }").to_corner(LEFT+UP)
        appl.scale(0.7)

        framebox3 = SurroundingRectangle(appl, buff = .1)
        self.play(Succession(
           Transform(framebox2,framebox3)))
        
        self.play(Succession(
           Transform(gme,appl)))
        
        appl1 = TexMobject("\\text{ Apple }")
        appl1.set_color(RED)
        appl1.to_edge(UP)
        self.play(
            Succession(
                Transform(gme1,appl1)))
        
        self.play(
            Succession(
                Transform(number_line,number_line2),Transform(numbers,numbers2),lag_ratio=1.2
            ))

        triangle1=RegularPolygon(3,start_angle=-PI/2)\
                   .scale(0.2)\
                   .next_to(number_line.get_left(),UP,buff=SMALL_BUFF)

        t_value1.add_updater(lambda d: d.set_value(triangle1.get_center()[0]))
        t_label2 = TexMobject("\\text{ low }", " \sigma").to_corner(UR)
        t_label2.set_color_by_tex("\sigma",YELLOW)
        t_label2.shift(LEFT)
        t_value1.next_to(t_label2,aligned_edge=DOWN)      

        self.add(t_value1)

        
        self.play(
            Succession(
                Transform(t_label,t_label2)))

        self.play(
                    ApplyMethod(triangle1.shift,RIGHT*6,rate_func=there_and_back,run_time=4))
        self.wait()

        self.play(FadeOut(Group(*self.get_mobjects())))

        ending = TexMobject("\\text{Reducing volatility can be acheived by }"
        , "\\text{diversifying }","\\text{ your portfolio}")

        ending.set_color_by_tex("diversifying",YELLOW)

        self.play(Write(ending),run_time =3)

class robbie_taha(Scene):
    def construct(self):
    
        Ale = Alex(mode= "plain").to_corner(LEFT+DOWN*2)
         
        summary = BulletedList("\\text{Basic OOP skills }"
        , "\\text{Intermediate data analysis skills }","\\text{find something at the intersection of credit and data science}")
        
        summary.set_color_by_tex_to_color_map({"Basic OOP skills ":BLUE,"Intermediate data analysis skills":RED,
        "find something at the intersection of credit and data science":GREEN})

        summary.to_corner(LEFT+UP)
        self.play(Write(summary), run_time = 5)  
        self.play(ShowCreation(Ale))      
        self.wait(1)

        self.play(Ale.change_mode, "shruggie")

        self.wait(2)
        self.play(Blink(Ale))
