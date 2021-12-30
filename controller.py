# -*- coding: utf-8 -*-

# python imports
from math import degrees
from time import time
import numpy as np
import time

# pyfuzzy imports
from fuzzy.storage.fcl.Reader import Reader



class FuzzyController:

    def __init__(self, fcl_path):
        self.system = Reader().load_from_file(fcl_path)


    def _make_input(self, world):
        return dict(
            cp = world.x,
            cv = world.v,
            pa = degrees(world.theta),
            pv = degrees(world.omega)
        )


    def _make_output(self):
        return dict(
            force = 0.
        )


    def decide(self, world):
        output = self._make_output()
        self.system.calculate(self._make_input(world), output)

        force = self.calculate_force(self._make_input(world))
        print(output['force'],force)
        if force==0:
            print(self._make_input(world))
        # time.sleep(3)
        return force

    def calculate_force(self ,data):
        pa_set_list , pv_set_list = self.fuzzification(data)
        max_left_fast,max_left_slow,stop,max_right_slow,max_right_fast = self.inference(pa_set_list , pv_set_list)
        tmp =self.defuzzify(max_left_fast,max_left_slow,stop,max_right_slow,max_right_fast)
        # print(tmp)
        # exit()
        return tmp
        
    def fuzzification(self,data):
        pa = data['pa']
        pv = data['pv']

        # print(pa)
        if pa < 0:
            pa = pa + 360
        # pa =  10
        # print(pa)
        # print(pv)


        if 0<=pa and pa<=30:
            up_more_right = 0.033 * pa
            # print(up_more_right)
        elif 30<pa and pa<=60:
            up_more_right= -0.033 * pa + 2
        else:
            up_more_right = 0

        if 30<=pa<=60:
            up_right = 0.033 * pa - 1
        elif 60<pa<=90:
            up_right= -0.033 * pa + 3
        else:
            up_right = 0

        if 60<=pa<=90:
            up = 0.033 * pa - 2
        elif 90<pa<=120:
            up = -0.033 * pa + 4
        else:
            up = 0

        
        if 90<=pa<=120:
            up_left = 0.033 * pa - 3
        elif 120<pa<=150:
            up_left= -0.033 * pa + 5
        else:
            up_left = 0

        if 120<=pa<=150:
            up_more_left = 0.033 * pa - 4
        elif 150<pa<=180:
            up_more_left= -0.033 * pa + 6
        else:
            up_more_left = 0

        if 180<=pa<=210:
            down_more_left = (0.033 * pa - 6)
        elif 210<pa<=240:
            down_more_left= (-0.033 * pa + 8)
        else:
            down_more_left = 0

        if 210<=pa<=240:
            down_left = abs (0.033 * pa - 7)
            # print('down_left iffffff'+down_left)
        elif 240<pa<=270:
            down_left= abs( -0.033 * pa + 9)
            # print('down_left eliiiiiiif',down_left)
        # elif pa==270:
        #     down_left=0
        else:
            down_left = 0

        if 240<=pa<=270:
            down = (0.033 * pa -8)
            # print('inside down if ')
            # print (down)
        elif 270<pa<=300:
            down= (-0.033 * pa + 10)
            # print('inside down elif ')
        else:
            down = 0
            # print('inside down else ')
        
        if 270<pa<=300:
            down_right = (0.033 * pa - 9)
        elif 300<pa<=330:
            down_right= (-0.033 * pa + 11)
        else:
            down_right = 0
        
        
        if 300<=pa<=330:
            down_more_right = (0.033 * pa - 10)
        elif 330<pa<=360:
            down_more_right= (-0.033 * pa + 12)
        else:
            down_more_right = 0


        
        #print(up_more_right,up_right,up,up_left,up_more_left,down_more_left,down_left,down,down_right,down_more_right)
        if pv<-200:
            pv=-199
        if pv>200:
            pv=199


        if -200<=pv<=-100:
            cw_fast_pv = (-0.01 * pv) - 1
        else:
            cw_fast_pv = 0
        
        if -200<=pv<=-100:
            cw_slow_pv = (0.01 * pv) + 2
        elif -100<pv<=0:
            cw_slow_pv = (-0.01*pv) 
        else:
            cw_slow_pv = 0
        
        if -100<=pv<=0:
            stop_pv = (0.01 * pv) + 1
        elif 0<pv<=100:
            stop_pv = (-0.01 *pv) + 1
        else:
            stop_pv = 0

        
        if 0<=pv<=100:
            ccw_slow_pv = 0.01 * pv 
        elif 100<pv<=200:
            ccw_slow_pv = -0.01 *pv + 2
        else:
            ccw_slow_pv = 0
        
        if 100<=pv<=200:
            ccw_fast_pv = 0.01 * pv - 1
        else:
            ccw_fast_pv = 0

        # print(cw_fast_pv,cw_slow_pv,stop_pv,ccw_slow_pv,ccw_fast_pv)
        #self.inference([up_more_right,up_right,up,up_left,up_more_left,down_more_left,down_left,down,down_right,down_more_right],[cw_fast_pv,cw_slow_pv,stop_pv,ccw_slow_pv,ccw_fast_pv])
        # exit()
        return [up_more_right,up_right,up,up_left,up_more_left,down_more_left,down_left,down,down_right,down_more_right],[cw_fast_pv,cw_slow_pv,stop_pv,ccw_slow_pv,ccw_fast_pv]

    def inference(self,pa_list,pv_list ):
        for i in range(len(pa_list)):
            if pa_list[i]<0:
                pa_list[i]=abs(0)
            if pa_list[i]>1:
                pa_list[i]=1
        for j in range (len(pv_list)):
            if pv_list[j]<0:
                pv_list[j]=abs(0)
            if pv_list[j]>1:
                pv_list[j]=1
        # print(pa_list,pv_list)
        # time.sleep(3)
        up_more_right=pa_list[0]
        up_right=pa_list[1]
        up=pa_list[2]
        up_left=pa_list[3]
        up_more_left=pa_list[4]
        down_more_left=pa_list[5]
        down_left=pa_list[6]
        down=pa_list[7]
        down_right=pa_list[8]
        down_more_right=pa_list[9]
        cw_fast=pv_list[0]
        cw_slow=pv_list[1]
        stop_pv=pv_list[2]
        ccw_slow=pv_list[3]
        ccw_fast=pv_list[4]

        force = 0
        left_fast = []
        left_slow = []
        stop = []
        right_slow = []
        right_fast = []
        # RULE 0:
		# 	IF
		# 		(pa IS up AND pv IS stop)
		# 		OR (pa IS up_right AND pv IS ccw_slow)
		# 		OR (pa IS up_left AND pv IS cw_slow)
		# 	THEN force IS stop;
        stop.append(max(min(up,stop_pv),min(up_right,ccw_slow),min(up_left,cw_slow)))
        #RULE 1: IF (pa IS up_more_right) AND (pv IS ccw_slow) THEN force IS right_fast;
        right_fast.append(min(up_more_right,ccw_slow))
        #RULE 2: IF (pa IS up_more_right) AND (pv IS cw_slow) THEN force IS right_fast;
        right_fast.append(min(up_more_right,cw_slow))
        #RULE 3: IF (pa IS up_more_left) AND (pv IS cw_slow) THEN force IS left_fast;
        left_fast.append(min(up_more_left,cw_slow))
        #RULE 4: IF (pa IS up_more_left) AND (pv IS ccw_slow) THEN force IS left_fast;
        left_fast.append(min(up_more_left,ccw_slow))
        #RULE 5: IF (pa IS up_more_right) AND (pv IS ccw_fast) THEN force IS left_slow;
        left_slow.append(min(up_more_right,ccw_fast))
        #RULE 6: IF (pa IS up_more_right) AND (pv IS cw_fast) THEN force IS right_fast;
        right_fast.append(min(up_more_right,cw_fast))
        #RULE 7: IF (pa IS up_more_left) AND (pv IS cw_fast) THEN force IS right_slow;
        right_slow.append(min(up_more_left,cw_fast))
		#RULE 8: IF (pa IS up_more_left) AND (pv IS ccw_fast) THEN force IS left_fast;
        left_fast.append(min(up_more_left,ccw_fast))
        #RULE 9: IF (pa IS down_more_right) AND (pv IS ccw_slow) THEN force IS right_fast;
        right_fast.append(min(down_more_right,ccw_slow))
		#RULE 10: IF (pa IS down_more_right) AND (pv IS cw_slow) THEN force IS stop;
        stop.append(min(down_more_right,cw_slow))
		#RULE 11: IF (pa IS down_more_left) AND (pv IS cw_slow) THEN force IS left_fast;
        left_fast.append(min(down_more_left,cw_slow))
		#RULE 12: IF (pa IS down_more_left) AND (pv IS ccw_slow) THEN force IS stop;
        stop.append(min(down_more_left,ccw_slow))
		#RULE 13: IF (pa IS down_more_right) AND (pv IS ccw_fast) THEN force IS stop;
        stop.append(min(down_more_right,ccw_fast))
		#RULE 14: IF (pa IS down_more_right) AND (pv IS cw_fast) THEN force IS stop;
        stop.append(min(down_more_right,cw_fast))
		#RULE 15: IF (pa IS down_more_left) AND (pv IS cw_fast) THEN force IS stop;
        stop.append(min(down_more_left,cw_fast))
		#RULE 16: IF (pa IS down_more_left) AND (pv IS ccw_fast) THEN force IS stop;
        stop.append(min(down_more_left,ccw_fast))
        # RULE 17: IF (pa IS down_right) AND (pv IS ccw_slow) THEN force IS right_fast;
        right_fast.append(min(down_right,ccw_slow))
		# RULE 18: IF (pa IS down_right) AND (pv IS cw_slow) THEN force IS right_fast;
        right_fast.append(min(down_right,cw_slow))
		# RULE 19: IF (pa IS down_left) AND (pv IS cw_slow) THEN force IS left_fast;
        left_fast.append(min(down_left,cw_slow))
		# RULE 20: IF (pa IS down_left) AND (pv IS ccw_slow) THEN force IS left_fast;
        left_fast.append(min(down_left,ccw_slow))
		# RULE 21: IF (pa IS down_right) AND (pv IS ccw_fast) THEN force IS stop;
        stop.append(min(down_right,ccw_fast))
		# RULE 22: IF (pa IS down_right) AND (pv IS cw_fast) THEN force IS right_slow;
        right_slow.append(min(down_right,cw_fast))
		# RULE 23: IF (pa IS down_left) AND (pv IS cw_fast) THEN force IS stop;
        stop.append(min(down_left,cw_fast))
		# RULE 24: IF (pa IS down_left) AND (pv IS ccw_fast) THEN force IS left_slow;
        left_slow.append(min(down_left,ccw_fast))
		# RULE 25: IF (pa IS up_right) AND (pv IS ccw_slow) THEN force IS right_slow;
        right_slow.append(min(up_right,ccw_slow))
		# RULE 26: IF (pa IS up_right) AND (pv IS cw_slow) THEN force IS right_fast;
        right_fast.append(min(up_right,cw_slow))
		# RULE 27: IF (pa IS up_right) AND (pv IS stop) THEN force IS right_fast;
        right_fast.append(min(up_right,stop_pv))
		# RULE 28: IF (pa IS up_left) AND (pv IS cw_slow) THEN force IS left_slow;
        left_slow.append(min(up_left,cw_slow))
		# RULE 29: IF (pa IS up_left) AND (pv IS ccw_slow) THEN force IS left_fast;
        left_fast.append(min(up_left,ccw_slow))
		# RULE 30: IF (pa IS up_left) AND (pv IS stop) THEN force IS left_fast;
        left_fast.append(min(up_left,stop_pv))
		# RULE 31: IF (pa IS up_right) AND (pv IS ccw_fast) THEN force IS left_fast;
        left_fast.append(min(up_right,ccw_fast))
		# RULE 32: IF (pa IS up_right) AND (pv IS cw_fast) THEN force IS right_fast;
        right_fast.append(min(up_right,cw_fast))
		# RULE 33: IF (pa IS up_left) AND (pv IS cw_fast) THEN force IS right_fast;
        right_fast.append(min(up_left,cw_fast))
		# RULE 34: IF (pa IS up_left) AND (pv IS ccw_fast) THEN force IS left_fast;
        left_fast.append(min(up_left,ccw_fast))
		# RULE 35: IF (pa IS down) AND (pv IS stop) THEN force IS right_fast;
        right_fast.append(min(down,stop_pv))
		# RULE 36: IF (pa IS down) AND (pv IS cw_fast) THEN force IS stop;
        stop.append(min(down,cw_fast))
		# RULE 37: IF (pa IS down) AND (pv IS ccw_fast) THEN force IS stop;
        stop.append(min(down,ccw_fast))
		# RULE 38: IF (pa IS up) AND (pv IS ccw_slow) THEN force IS left_slow;
        left_slow.append(min(up,ccw_slow))
		# RULE 39: IF (pa IS up) AND (pv IS ccw_fast) THEN force IS left_fast;
        left_fast.append(min(up,ccw_fast))
		# RULE 40: IF (pa IS up) AND (pv IS cw_slow) THEN force IS right_slow;
        right_slow.append(min(up,cw_slow))
		# RULE 41: IF (pa IS up) AND (pv IS cw_fast) THEN force IS right_fast;
        right_fast.append(min(up,cw_fast))
		# RULE 42: IF (pa IS up) AND (pv IS stop) THEN force IS stop;
        stop.append(min(up,stop_pv))





         
        # print(up_more_right,up_right,up,up_left,up_more_left,down_more_left,down_left,down,down_right,down_more_right)
        # print(cw_fast,cw_slow,stop_pv,ccw_slow,ccw_fast)
        max_left_fast = max(left_fast)
        max_left_slow = max(left_slow)
        max_stop = max(stop)
        max_right_slow=max(right_slow)
        max_right_fast=max(right_fast)

        # print(max_left_fast,max_left_slow,max_stop,max_right_slow,max_right_fast)
        # exit()

        return max_left_fast,max_left_slow,max_stop,max_right_slow,max_right_fast

    def defuzzify(self,max_left_fast,max_left_slow,max_stop,max_right_slow,max_right_fast):
        # print(max_left_fast,max_left_slow,max_stop,max_right_slow,max_right_fast)
        forces = []
        points=np.linspace(-100,100,5000)
        # print(points)
        # exit()
        dx=points[1]-points[0]
        sum = 0
        sum2= 0

        for point in points:
            # print(point)

            left_fast = self.left_fast_membership(point)
            # print(left_fast)
            if left_fast>max_left_fast:
                left_fast=max_left_fast
            # print(left_fast)
            # exit()

            

            left_slow = self.left_slow_membership(point)
            # print(left_slow)
            if left_slow>max_left_slow:
                left_slow=max_left_slow

            stop = self.stop_membership(point)
            # print(stop)
            if stop>max_stop:
                stop=max_stop

            right_slow=self.right_slow_membership(point)
            # print(right_slow)
            if right_slow>max_right_slow:
                right_slow=max_right_slow

            right_fast=self.right_fast_membership(point)
            # print(right_fast)
            if right_fast>max_right_fast:
                right_fast=max_right_fast
            # print(right_fast)
            y = max(left_fast,left_slow,stop,right_slow,right_fast)
            forces.append(y)
            # print(left_fast,left_slow,stop,right_slow,right_fast)
            # exit()
            sum+=y*dx
            sum2+=y*point*dx
        # print(points[1],forces[1])
        # exit()

           
        return sum2/sum if sum!=0 else 0


    def left_fast_membership(self,x):
        if x>=-100 and x<=-80:
            y =0.05*x+5
        elif x>-80 and x<=-60:
            y =-0.05*x-3
        else:
            y = 0
        return abs(y) if y>0 else 0

    def left_slow_membership(self,x):
        if x>=-80 and x<=-60:
            y =0.05*x+4
        elif x>-60 and x<=0:
            y =-0.016*x 
        else:
            y = 0
        # print(y)
        return abs(y) if y>0 else 0

    def stop_membership(self,x):
        if x>=-60 and x<=0:
            y =0.016*x + 1
        elif x>0 and x<=60:
            y =-0.016 *x + 1
        else:
            y = 0
        # print(y)    
        return abs(y) if y>0 else 0
    def right_slow_membership(self,x):
        if x>=0 and x<=60:
            y =0.016*x 
        elif x>60 and x<=80:
            y =-0.05 *x + 4
        else:
            y = 0
        # print(y)
        return abs(y) if y>0 else 0
    def right_fast_membership(self,x):
        if x>=60 and x<=80:
            y =0.05*x -3
        elif x>80 and x<=100:
            y =-0.05 *x + 5
        else:
            y = 0
        # print(y)
        
        return abs(y) if y>0 else 0 


    

