# -*- coding: utf-8 -*-
import numpy as np
import math

'''
/***************************************************************************************
* 悬链线计算用坐标系为以 A （低悬点）为原点， A 与 B' （ B 在与 A 等高的水平面上的投影点）为 X 轴，
* AB 之间的高差 h = HB-HA ， h>=0 。以下为变量命名规则：
*
* T 线上应力，单位截面上作用的张力： N/mm2
* L 线长： m
* H 高度： m
* w 比载，电线单位长度、单位截面上承受的荷载称为比载： N/mm2.m
* l 档距，相邻两悬挂点间垂直于荷载方向的投影距离称为档距： m
* h 高差，相邻两悬挂点沿荷载方向的高差，当右悬挂点高于左悬挂点时 h 为正值，反之为负值： m
*
* f 电线的弧垂，指自两悬挂点连线沿荷载方向到电线轴线间的距离： m
* fM 档距中央弧垂，档内电线的最大弧垂
* fO 悬链线最低点 O 的弧垂
*
* fAO 低悬点 A 对 O 的高差
* fBO 高悬点 B 对 O 的高差
*
* A 左（低）悬挂点，应力 TA
* B 右（高）悬挂点，应力 TB
* O 最低点，仅有水平应力 T0
*
* s 斜距 |AB| ，两悬挂点连线的直线距离： sqrt(l*l+h*h)
* a 平距 |AO| ，电线最低点到左悬挂点 A 垂直于荷载方向的投影距离
* b 平距 |BO| ，电线最低点到右悬挂点 B 垂直于荷载方向的投影距离
* cosB l 与 s 的比： 1/s
*
* 其中：
* elec 电力
* catenary 悬链线
* hyperbolic 双曲线公式，精确计算公式
* parabolic  抛物线公式，高阶近似计算公式
* sag 弧垂
* suspension 悬挂点
****************************************************************************************/
AABBBAAABBB^
'''
#/**
#* 悬链线最低点 O 到悬挂点 A 间垂直于荷载方向的投影 a ( 可以 <0)
#* 使用双曲线方程 ( 精确式 ) 计算 P61 (3-6)
#* 说明 b = l - a
#*/
def elec_catenary_hyperbolic_lowest_proj ( T0,  w, l, h):
    Lh0 = elec_catenary_hyperbolic_length_equal_high (T0, w, l)
    if Lh0 != 0.:
        a = l/2. - T0/w*np.arcsinh(h/Lh0) 
        b = l/2. + T0/w*np.arcsinh(h/Lh0)
    else:
        a = l/2.
        b = l/2.
    return a


#/**
#* 悬挂点等高时悬链线线长双曲线公式 . P61 (3-6)
#*/
def elec_catenary_hyperbolic_length_equal_high ( T0,  w, l  ):
    ret = (2*T0/w)*np.sinh(w*l/2/T0)
    return ret

#/**
#* 悬链线双曲线坐标方程 P62 (3-9)
#* 悬链线上任何一点对 A 点的高差
#* y = f(x), x = [0, l]
#* 验证： f(0)=0, f(l)=h
#*/
def elec_catenary_hyperbolic_equation (  T0,  w,  l,  h,  x ):
    a = elec_catenary_hyperbolic_lowest_proj (T0, w, l, h)
    y = T0*(np.cosh((x-a)*w/T0) - np.cosh(w*a/T0))/w
    return y


#/**
#* 悬链线双曲线弧垂计算方程 P63 (3-12)
#* f = d(x), x = [0, l]
#* 验证： fA = d(0) = 0, fB = d(l) = 0
#*/
def elec_catenary_hyperbolic_sag ( T0, w, l, h,  x ):
    Lh0 = elec_catenary_hyperbolic_length_equal_high (T0, w, l)
    fx = h*x/l - T0*h/w/Lh0*(np.sinh(w*l/2/T0) + np.sinh(w*(2*x-l)/2/T0)) + (2*T0/w*np.sinh(w*x/2/T0)*np.sinh(w*(l-x)/2/T0))*np.sqrt(1+h*h/(Lh0*Lh0))
    return fx


#def rad(d):
    #return d * np.pi/180.0

 
#根据经纬度计算两点距离的Python代码
def distance(latlng1, latlng2):
    radlat1 = np.deg2rad(latlng1[0])
    radlat2 = np.deg2rad(latlng1[0])
    a = radlat1 - radlat2
    b = np.deg2rad(latlng1[1]) - np.deg2rad(latlng2[1])
    s = 2 * np.arcsin(np.sqrt(pow(np.sin(a/2),2) + np.cos(radlat1) * np.cos(radlat2) * pow(np.sin(b/2),2)))
    earth_radius=6378137
    s = s * earth_radius

    if s<0:
        return -s
    else:
        return s

def f( l,  h,  z0,  x, T0=0.8, w=0.001):
    return elec_catenary_hyperbolic_equation( T0,  w,  l,  h,  x ) + z0
    #return elec_catenary_hyperbolic_sag( T0,  w,  l,  h,  x ) + z0


######################################
######垂直比载########################
######################################
def g_vertical(sectional_area, calc_mass):
    return 9.807 * calc_mass / sectional_area / 1000.0
    
######################################
######覆冰比载########################
######################################
def g_ice(ice_thickness, sectional_area, calc_diameter):
    return 27.728 * ice_thickness *( ice_thickness + calc_diameter) / sectional_area / 1000.0

######################################
######覆冰垂直总比载########################
######################################
def g_ice_vertical(ice_thickness, sectional_area, calc_mass, calc_diameter):
    return g_vertical(sectional_area, calc_mass) + g_ice(ice_thickness, sectional_area, calc_diameter)


######################################
######无冰时风压比载########################
######################################
def g_no_ice_wind(wind_speed, sectional_area, calc_diameter):
    #0.613*IF(wind_speed<20,1,IF(wind_speed<30,0.85,IF(wind_speed<35,0.75,0.7)))*IF(calc_diameter<17,1.2,1.1)*calc_diameter*SUMSQ(wind_speed)/sectional_area/1000.0
    a = 0.7
    if wind_speed<35:
        a = 0.75
    b = a
    if wind_speed<30:
        b = 0.85
    c = b
    if wind_speed<20:
        c = 1.0
    d = 1.1
    if calc_diameter<17:
        d = 1.2
    return 0.613 * c * d * calc_diameter * wind_speed * wind_speed / sectional_area /1000.0
    
######################################
######覆冰时风压比载########################
######################################
def g_ice_wind(wind_speed, ice_thickness, sectional_area, calc_diameter):
    #0.613*IF(wind_speed<20,1,IF(wind_speed<30,0.85,IF(wind_speed<35,0.75,0.7)))*1.2*(calc_diameter+2*ice_thickness)*SUMSQ(wind_speed)/sectional_area/1000
    a = 0.7
    if wind_speed<35:
        a = 0.75
    b = a
    if wind_speed<30:
        b = 0.85
    c = b
    if wind_speed<20:
        c = 1.0
    return 0.613 * c * 1.2 *(calc_diameter + 2 * ice_thickness) * wind_speed * wind_speed / sectional_area /1000.0

######################################
######无冰有风时综合比载########################
######################################
def g_add_no_ice_wind(wind_speed, sectional_area, calc_mass, calc_diameter):
    g1 = g_vertical(sectional_area, calc_mass)
    g4 = g_no_ice_wind(wind_speed, sectional_area, calc_diameter)
    return math.sqrt(g1*g1 + g4*g4)


######################################
######有冰无风时综合比载########################
######################################
def g_add_ice_no_wind(wind_speed, ice_thickness, sectional_area, calc_mass, calc_diameter):
    g3 = g_ice_vertical(ice_thickness, sectional_area, calc_mass, calc_diameter)
    g5 = g_ice_wind(wind_speed, ice_thickness, sectional_area, calc_diameter)
    return math.sqrt(g3*g3 + g5*g5)


######################################
##       g1 垂直比载                ##
##       g2 覆冰比载                ##
##       g3 覆冰垂直总比载          ##
##       g4 无冰时风压比载          ##
##       g5 覆冰时风压比载          ##
##       g6 无冰有风时综合比载      ##
##       g7 有冰无风时综合比载      ##
######################################
def get_g(line, wind_speed=28, ice_thickness=15):
    g1 = g_vertical(line['sectional_area'], line['calc_mass'])
    g2 = g_ice(ice_thickness, line['sectional_area'], line['calc_diameter'])
    g3 = g_ice_vertical(ice_thickness, line['sectional_area'], line['calc_mass'], line['calc_diameter'])
    g4 = g_no_ice_wind(wind_speed, line['sectional_area'], line['calc_diameter'])
    g5 = g_ice_wind(wind_speed, ice_thickness, line['sectional_area'], line['calc_diameter'])
    g6 = g_add_no_ice_wind(wind_speed, line['sectional_area'], line['calc_mass'], line['calc_diameter'])
    g7 = g_add_ice_no_wind(wind_speed, ice_thickness, line['sectional_area'], line['calc_mass'], line['calc_diameter'])
    return g1,g2,g3,g4,g5,g6,g7

######################################
## sigma_p   瞬时破坏应力
## sigma_m   最大使用应力
## sigma_n   年平均运行应力
######################################

def get_sigma(line):
    sigma_p = line['break_force']/line['sectional_area']
    #sigma_m = sigma_p/k
    sigma_n = sigma_p * 0.25
    return sigma_n
    
    


    
if __name__ == "__main__":
    pass
