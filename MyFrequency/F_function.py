# import pandas as pd
from decimal import Decimal

# df = pd.read_excel('1.xlsx')
lte = []
# for inx, row in df.iterrows():
#     lte.append(list(row.values))
# print(lte)
# a = 1895.1


def float2int(f):
    if str(f).split('.')[-1] == '0':
        # print(str(f).split('.')[-1])
        return int(f)
    else:
        return f


def f2n(f):
    res = []
    for i in lte:
        if i[1] <= f <= i[1] + i[-1] * 0.1:
            band = int(i[0])
            DL = float2int(float(Decimal(str(f))))
            DL_N = float2int(float((Decimal(str(f)) - Decimal(str(i[1]))) * 10 + Decimal(str(i[2]))))
            UL = float2int(float(Decimal(str(f)) - Decimal(str(i[1])) + Decimal(str(i[3]))))
            UL_N = float2int(float((Decimal(str(f)) - Decimal(str(i[1]))) * 10 + Decimal(str(i[4]))))
            if DL == UL:
                re = [band, DL, DL_N, '-', '-']
            else:
                re = [band, DL, DL_N, UL, UL_N]
            if re not in res:
                res.append(re)
        if i[3] <= f <= i[3] + i[-1] * 0.1:
            band = int(i[0])
            DL = float2int(float(Decimal(str(f)) - Decimal(str(i[3])) + Decimal(str(i[1]))))
            DL_N = float2int(float((Decimal(str(f)) - Decimal(str(i[3]))) * 10 + Decimal(str(i[2]))))
            UL = float2int(float(Decimal(str(f))))
            UL_N = float2int(float((Decimal(str(f)) - Decimal(str(i[3]))) * 10 + Decimal(str(i[4]))))

            if DL == UL:
                re = [band, DL, DL_N, '-', '-']
            else:
                re = [band, DL, DL_N, UL, UL_N]
            if re not in res:
                res.append(re)
    return res


def n2f(f):
    res = []
    for i in lte:
        if i[2] <= f <= i[2] + i[-1]:
            band = int(i[0])
            DL = float2int(float((Decimal(str(f)) - Decimal(str(i[2]))) / 10 + Decimal(str(i[1]))))
            DL_N = float2int(float(Decimal(str(f))))
            UL = float2int(float((Decimal(str(f)) - Decimal(str(i[2]))) / 10 + Decimal(str(i[3]))))
            UL_N = float2int(float(Decimal(str(f)) - Decimal(str(i[2])) + Decimal(str(i[4]))))
            if DL == UL:
                re = [band, DL, DL_N, '-', '-']
            else:
                re = [band, DL, DL_N, UL, UL_N]
            if re not in res:
                res.append(re)
        if i[4] <= f <= i[4] + i[-1]:
            band = int(i[0])
            DL = float2int(float((Decimal(str(f)) - Decimal(str(i[4]))) / 10 + Decimal(str(i[1]))))
            DL_N = float2int(float(Decimal(str(f)) - Decimal(str(i[4])) + Decimal(str(i[2]))))
            UL = float2int(float((Decimal(str(f)) - Decimal(str(i[4]))) / 10 + Decimal(str(i[3]))))
            UL_N = float2int(float(Decimal(str(f))))

            if DL == UL:
                re = [band, DL, DL_N, '-', '-']
            else:
                re = [band, DL, DL_N, UL, UL_N]
            if re not in res:
                res.append(re)
    return res


# 5G各种带宽在不同Scs下的RB数
scs_15 = {'5': 25, '10': 52, '15': 79, '20': 106, '25': 133
    , '30': 160, '40': 216, '50': 270}

scs_30 = {'5': 11, '10': 24, '15': 38, '20': 51, '25': 65
    , '30': 78, '40': 106, '50': 133, '60': 162
    , '70': 189, '80': 217, '90': 245, '100': 273}

scs_60 = {'10': 11, '15': 18, '20': 24, '25': 31
    , '30': 38, '40': 51, '50': 65, '60': 79
    , '70': 93, '80': 107, '90': 121, '100': 135
    , '200': 264}

scs_120 = {'50': 32, '100': 66, '200': 132, '400': 264}


# ---------------------GSCN输出----------------------
def gscn_print(Fref):
    if 0 < Fref < 3000:
        n = int((Fref - 0.15) / 1.2)
        return 3 * n

    if 0 < Fref < 24250:
        n = int((Fref - 3000) / 1.44)
        return 7499 + n

    if 0 < Fref < 100000:
        n = int((Fref - 24250.08) / 17.28)
        return 22256 + n

    return 'NA'


# --------------------RB数据输出---------------------
def rb_print(scs, bandwidth):
    if scs == 120:
        return scs_120[bandwidth]

    if scs == 60:
        return scs_60[bandwidth]

    if scs == 30:
        return scs_30[bandwidth]
    return scs_15[bandwidth]


# --------------------SSB频点输出--------------------
def ssb_print(Rb_number, Nref, scs, F_global):
    if Rb_number % 2 == 0:
        return Nref
    else:
        return Nref - (6 * scs) / (F_global * 10 ** 3)


# -----------------中心频点步长输出------------------
def step_print(scs, band):
    if band == 'Band-41':
        if scs == 30:
            return 6
        else:
            return 3
    if band == 'Band-77' or band == 'Band-78' or band == 'Band-79':
        if scs == 30:
            return 2
        else:
            return 1
    return 20


# ---------------------Band输出----------------------
def Band_print(Nref):
    if Nref > 402000 and Nref < 405000:
        return 'Band-34'

    if Nref > 514000 and Nref < 524000:
        return 'Band-38'

    if Nref > 376000 and Nref < 384000:
        return 'Band-39'

    if Nref > 460000 and Nref < 480000:
        return 'Band-40'

    if Nref > 499200 and Nref < 537999:
        return 'Band-41'

    if Nref > 285400 and Nref < 286400:
        return 'Band-51'

    if Nref > 422000 and Nref < 440000:
        return 'Band-66'

    if Nref > 399000 and Nref < 404000:
        return 'Band-70'

    if Nref > 123400 and Nref < 130400:
        return 'Band-71'

    if Nref > 286400 and Nref < 303400:
        return 'Band-75'

    if Nref > 285400 and Nref < 286400:
        return 'Band-76'

    if Nref > 620000 and Nref < 653333:
        return 'Band-78'

    if Nref > 620000 and Nref < 680000:
        return 'Band-77'

    if Nref > 693334 and Nref < 733333:
        return 'Band-79'

    if Nref > 422000 and Nref < 434000:
        return 'Band-1'

    if Nref > 386000 and Nref < 398000:
        return 'Band-2'

    if Nref > 361000 and Nref < 376000:
        return 'Band-3'

    if Nref > 173800 and Nref < 178800:
        return 'Band-5'

    if Nref > 524000 and Nref < 538000:
        return 'Band-7'

    if Nref > 185000 and Nref < 192000:
        return 'Band-8'

    if Nref > 145800 and Nref < 149200:
        return 'Band-12'

    if Nref > 158200 and Nref < 164200:
        return 'Band-20'

    if Nref > 386000 and Nref < 399000:
        return 'Band-25'

    if Nref > 151600 and Nref < 160600:
        return 'Band-28'

    return 'NA'


# ---------------------频率转频点----------------------
def Nref_point():
    # 判断用户输入的中心频率是否合法
    while True:
        Fref = input('\n请输入中心频率:')
        try:
            if int(float(Fref)) > 0:
                break
            else:
                print('不合规请重新输入')
        except:
            print('不合规请重新输入')

    # 判断用户输入的小区带宽是否合法
    while True:
        bandwidth = input('请输入小区带宽(单位MHz):')
        if bandwidth.isdigit():
            if int(bandwidth) in [5, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 200, 400]:
                break
            else:
                print('不合规请重新输入')
        else:
            print('不合规请重新输入')

    # 判断用户输入的子载波间隔是否合法
    while True:
        Scs = input('请输入子载波间隔(单位KHz):')
        if Scs.isdigit():
            if int(bandwidth) < 51 and int(Scs) == 15:
                break
            if int(bandwidth) < 101 and int(Scs) == 30:
                break
            if int(bandwidth) > 11 and int(bandwidth) < 101 and int(Scs) == 60:
                break
            if int(bandwidth) > 51 and int(bandwidth) < 101 and int(Scs) == 120:
                break
            else:
                print('不合规请重新输入')
        else:
            print('不合规请重新输入')

    if float(Fref) < 100000:
        F_global = 60 * 10 ** -3
        Fref_offs = 24250
        Nref_offs = 2016667

    if float(Fref) < 24250:
        F_global = 15 * 10 ** -3
        Fref_offs = 3000
        Nref_offs = 600000

    if float(Fref) < 3000:
        F_global = 5 * 10 ** -3
        Fref_offs = 0
        Nref_offs = 0

    Nref = (float(Fref) - Fref_offs) / F_global + Nref_offs  # 中心频点计算
    print(Nref)

    Band = Band_print(Nref)  # 频带获取
    print(Band)

    Step_size = int(step_print(int(Scs), Band))  # 频点栅格步长获取
    print(Step_size)

    # 中心频点修正
    while int(Nref) % Step_size != 0:
        Nref += 1

    Rb_number = rb_print(int(Scs), str(int(bandwidth)))  # NRB数据获取

    SSB_ref = ssb_print(Rb_number, Nref, int(Scs), F_global)  # SSB频点获取

    Gscn = gscn_print(float(Fref))  # GSCN获取

    print('\n计算结果如下：')
    print('    中心频率：', Fref, 'MHz')
    print('    小区带宽：', bandwidth, 'MHz')
    print('    载波间隔：', Scs, 'KHz')
    print('    NRB个数：', Rb_number)
    print('    频点栅格：', int(F_global * 10 ** 3), 'KHz')
    print('    中心频点:', int(Nref))
    print('    SSB频点:', int(SSB_ref))
    print('    GSCN频点:', Gscn)
    print('    小区频带:', Band)
    print('    频点步长:', Step_size)


# ---------------------频点转频率----------------------
def Fref_point():
    # 判断用户输入的中心频点是否合法
    while True:
        Nref = input('\n请输入中心频点:')
        if Nref.isdigit():
            if int(Nref) > 0:
                break
            else:
                print('不合规请重新输入')
        else:
            print('不合规请重新输入')

    # 判断用户输入的小区带宽是否合法
    while True:
        bandwidth = input('请输入小区带宽(单位MHz):')
        if bandwidth.isdigit():
            if int(bandwidth) in [5, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 200, 400]:
                break
            else:
                print('不合规请重新输入')
        else:
            print('不合规请重新输入')

    # 判断用户输入的子载波间隔是否合法
    while True:
        Scs = input('请输入子载波间隔(单位KHz):')
        if Scs.isdigit():
            if int(bandwidth) < 51 and int(Scs) == 15:
                break
            if int(bandwidth) < 101 and int(Scs) == 30:
                break
            if int(bandwidth) > 11 and int(bandwidth) < 101 and int(Scs) == 60:
                break
            if int(bandwidth) > 51 and int(bandwidth) < 101 and int(Scs) == 120:
                break
            else:
                print('不合规请重新输入')
        else:
            print('不合规请重新输入')

    if int(Nref) < 3279167:
        F_global = 60 * 10 ** -3
        Fref_offs = 24250
        Nref_offs = 2016667

    if int(Nref) < 2016666:
        F_global = 15 * 10 ** -3
        Fref_offs = 3000
        Nref_offs = 600000

    if int(Nref) < 599999:
        F_global = 5 * 10 ** -3
        Fref_offs = 0
        Nref_offs = 0

    Band = Band_print(int(Nref))  # 频带获取

    Step_size = int(step_print(int(Scs), Band))  # 频点栅格步长获取

    Fref = int(Fref_offs + F_global * (int(Nref) - Nref_offs))  # 中心频率计算

    Rb_number = rb_print(int(Scs), str(int(bandwidth)))  # NRB数据获取

    SSB_ref = ssb_print(Rb_number, int(Nref), int(Scs), F_global)  # SSB频点获取

    Gscn = gscn_print(int(Fref))  # GSCN获取

    print('\n计算结果如下：')
    print('    中心频率：', Fref, 'MHz')
    print('    小区带宽：', bandwidth, 'MHz')
    print('    载波间隔：', Scs, 'KHz')
    print('    NRB个数：', Rb_number)
    print('    频点栅格：', int(F_global * 10 ** 3), 'KHz')
    print('    中心频点:', int(Nref))
    print('    SSB频点:', int(SSB_ref))
    print('    GSCN频点:', Gscn)
    print('    小区频带:', Band)
    print('    频点步长:', Step_size)


# -----------------------程序入口------------------------
if __name__ == '__main__':
    print('5G子载波间隔与小区带宽对应规则：')
    print('    15KHz间隔:5M 10M 15M 20M 25M 30M 40M 50M')
    print('    30KHz间隔:5M 10M 15M 20M 25M 30M 40M 50M 60M 70M 80M 90M 100M')
    print('    60KHz间隔:10M 15M 20M 25M 30M 40M 50M 60M 70M 80M 90M 100M 200M')
    print('    120KHz间隔:50M 100M 200M 400M')
    while True:
        sele = input('\n请选择计算方式：1、频率转频点；2、频点转频率;3、退出程序:')
        if sele.isdigit():
            if int(sele) == 3:
                print('\n欢迎再次使用！')
                exit(0)
            if int(sele) == 1:
                Nref_point()
                continue
            if int(sele) == 2:
                Fref_point()
                continue
            else:
                print('输入有误请重新输入')
        else:
            print('输入有误请重新输入')
