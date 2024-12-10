import base64
import os
import cv2
from playwright.sync_api import Playwright, sync_playwright, expect


def _tran_canny(image):
    """消除噪声"""
    image = cv2.GaussianBlur(image, (3, 3), 0)
    return cv2.Canny(image, 50, 150)


def template_matching(img_path, tm_path):
    # 导入图片，灰度化
    img_rgb = cv2.imread(img_path)
    template_rgb = cv2.imread(tm_path)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    tm_gray = cv2.cvtColor(template_rgb, cv2.COLOR_BGR2GRAY)
    # 缺口图去除背景
    h, w = tm_gray.shape
    w_start_index, h_start_index = 0, 0
    w_end_index, h_end_index = w, h
    # 缺口图去除背景
    # 算出高起始位置
    for i in range(h):
        if not any(tm_gray[i, :]):
            h_start_index = i
        else:
            break
    # 算出高的结束位置
    for i in range(h - 1, 0, -1):
        if not any(tm_gray[i, :]):
            h_end_index = i
        else:
            break
    # 算出宽的起始位置
    for i in range(w):
        if not any(tm_gray[:, i]):
            w_start_index = i
        else:
            break
    # 算出宽的起始位置
    for i in range(w - 1, 0, -1):
        if not any(tm_gray[:, i]):
            w_end_index = i
        else:
            break

    # 取出完整的缺口图
    tm_gray = tm_gray[h_start_index:h_end_index + 1, w_start_index:w_end_index + 1]
    # 自适应阈值话
    img_thresh = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 0)
    tm_thresh = cv2.adaptiveThreshold(tm_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 0)

    # 边缘检测
    img_canny = cv2.Canny(img_thresh, 0, 500)
    tm_canny = cv2.Canny(tm_thresh, 0, 500)
    # cv2.imshow("img_canny", img_canny)
    # cv2.imshow("tm_canny", tm_canny)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    h, w = tm_gray.shape[:2]
    # 模板匹配
    res = cv2.matchTemplate(img_canny, tm_canny, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc[0]  # 横坐标

    right_bottom = (max_loc[0] + w, max_loc[1] + h)  # 右下角
    # 圈出矩形坐标
    cv2.rectangle(img_rgb, max_loc, right_bottom, (0, 0, 255), 2)

    # 保存处理后的图片
    cv2.imwrite('./images/res.png', img_rgb)

    # 显示图片 参数：（窗口标识字符串，imread读入的图像）
    # cv2.imshow("test_image", img_rgb)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return top_left - 22


# 有的检测移动速度的 如果匀速移动会被识别出来，来个简单点的 渐进
def get_track(distance):  # distance为传入的总距离
    # 移动轨迹
    track = []
    # 当前位移
    current = 0
    # 减速阈值
    mid = distance * 4 / 5
    # 计算间隔
    t = 0.2
    # 初速度
    v = 2

    while current < distance:
        if current < mid:
            # 加速度为2
            a = 4
        else:
            # 加速度为-2
            a = -1
        v0 = v
        # 当前速度
        v = v0 + a * t
        # 移动距离
        move = v0 * t + 1 / 2 * a * t * t
        # 当前位移
        current += move
        # 加入轨迹
        track.append(round(move))
    return track


class epms_token:
    def __init__(self, username, password):
        self.login_url = "https://iepms.zte.com.cn/zte-crm-iepms-baseui/#/main/menu/iframeParse/M03020023"
        self.username = username
        self.password = password
        self.page = None
        self.context = None
        self.browser = None
        self.token = None
        self.account = None

    def start(self):
        with sync_playwright() as p:
            self.init_page(p)
            self.login()

            if not os.path.exists("./images"):
                os.mkdir("./images")

    def init_page(self, p):
        """初始化浏览器，获取page对象"""
        self.browser = p.chromium.launch(headless=False, args=['--start-maximized','--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'])

        # playwright 默认启动的浏览器窗口大小是1280x720， 我们可以通过设置no_viewport参数来禁用
        # 固定的窗口大小 ，no_viewport 禁用窗口大小
        self.context = self.browser.new_context(no_viewport=True)
        self.page = self.context.new_page()

    def login(self):
        """通过账号密码登录"""
        print("开始登录")
        # 访问页面
        self.page.goto(self.login_url)
        self.page.wait_for_timeout(5000)
        self.page.get_by_placeholder("用户名 / 邮箱 / 手机号 / 工号").click()
        self.page.get_by_placeholder("用户名 / 邮箱 / 手机号 / 工号").fill(self.username)
        self.page.get_by_placeholder("密码").click()
        self.page.get_by_placeholder("密码").fill(self.password)
        self.page.wait_for_timeout(5)
        self.page.get_by_role("button", name="登录", exact=True).click()
        self.page.wait_for_timeout(2000)
        self.page.locator('#slider').bounding_box()

        self.get_slide_bg_img()
        while not self.move_slider():
            self.get_slide_bg_img()

    def get_slide_bg_img(self):
        """截取滑动验证码背景图片"""
        # self.page.wait_for_timeout(2000)
        print("正在获取滑动验证码背景图片")
        # 获取滑动验证码所在的iframe
        captcha_iframe = self.page.locator("#block").get_attribute("src")
        with open("MyEpms/images/slider.png", "wb") as f:
            img = base64.b64decode(captcha_iframe.split('data:image/png;base64,')[-1])
            f.write(img)
        # 获取滑动验证码的背景图
        slide_bg = self.page.locator("#bigImage").get_attribute("src")
        with open("MyEpms/images/slider_bg.png", "wb") as f:
            img = base64.b64decode(slide_bg.split('data:image/png;base64,')[-1])
            f.write(img)

    def move_slider(self):
        s = self.page.wait_for_selector('//*[@id="slider"]')
        # 找到这个元素再当前页面的坐标（这个会返回一个字典里边四个数字）
        box = s.bounding_box()
        # 移动鼠标到上边元素的中心（上边四个参数用途来了）
        self.page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        # 按下鼠标（这个不多说）
        self.page.mouse.down()
        # 这里获取到x坐标中心点位置
        x = box["x"] + box["width"] / 2
        # 这个把缺口获取到的长度放到轨迹加工一下得到一个轨迹
        top_left = template_matching('MyEpms/images/slider_bg.png', 'MyEpms/images/slider.png')
        tracks = get_track(top_left)
        for track in tracks:
            # 循环鼠标按照轨迹移动
            # strps 是控制单次移动速度的比例是1/10 默认是1 相当于 传入的这个距离不管多远0.1秒钟移动完 越大越慢
            self.page.mouse.move(x + track, 0, steps=5)
            x += track
        # 移动结束鼠标抬起
        self.page.mouse.up()
        self.page.wait_for_timeout(2000)
        try:
            self.page.wait_for_selector('//*[@id="slider"]', timeout=2)
        except:
            print("已通过滑动验证码")
            storage = self.context.storage_state()
            localStorage_list = storage['cookies']
            self.token = [i['value'] for i in localStorage_list if i['name'] == 'UCSSSOToken'][0]
            self.account = [i['value'] for i in localStorage_list if i['name'] == 'UCSSSOAccount'][0]
            self.browser.close()
            return True
        else:
            print(f"滑动失败")
            return False


if __name__ == "__main__":
    slide = epms_token('kongweibiao@shunscom.com', 'Kwb231027')
    slide.start()
