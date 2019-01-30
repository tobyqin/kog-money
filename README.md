# kog-money

一个王者荣耀刷金币的小外挂。
始发于：[教你使用50行Python代码刷王者荣耀金币](https://betacat.online/posts/2017-12-14/hack-way-to-get-golden-coins-for-king-of-glory/)

`kog_simple.py`:刷金币版本

`kog.py`: 刷金币以及英雄熟练度，只支持android。真机支支持huawie mate20， 可使用[雷电模拟器](https://www.ldplayer.net/)。


## 原理

王者荣耀的冒险模式里有个挑战模式，第一次过关可以获得比较多的金币，后面重新挑战还是会获得少量金币，这不算是bug，你不嫌烦手动蛮力也可以刷金币。

> 推荐关卡：陨落的废都 - 魔女回忆

此关卡使用纯输出英雄20秒左右可以打BOSS，50秒左右可以通关，每次重复通关可以获得奖励19金币。在开挂前建议你手动通关体验一下。此为游戏原理。

简单来说，需要执行以下步骤：

1. 界面打开至挑战关卡：陨落的废都 - 魔女回忆 【点击下一步】
2. 进入阵容调整界面，提前安排好阵容。【点击闯关】
3. 进入挑战界面。【点击右上角-自动-等待挑战结束】
4. 进入挑战完成界面。【点击屏幕继续】
5. 进入关卡奖励界面。【点击再次挑战】
6. 进入阵容调整界面，循环至步骤1或步骤2【貌似取决于游戏区和版本】

只要你能模拟屏幕点击就可以完成刷金币的脚本.

在安卓模拟界面点击最简单的方式就是使用ADB发送命令，不需要root手机，不需要安装第三方软件，方便快捷。ADB命令点击屏幕坐标[x, y] 可以使用命令：

```
adb shell input tap x y
```

iOS与mac用户，可以利用WDA，参考[微信跳一跳辅助程序的相关安装步骤](https://www.jianshu.com/p/ff973a5910ae)，他们已经写的非常详细了。原理也是通过WDA来模拟屏幕点击，有兴趣的朋友可以看一下 `kog_ios.py` 中的源代码。这里也不再赘述环境的准备。（与跳一跳的环境是一样的）

## 准备

### 安卓
- 需要真实安卓手机。
- 手机需开启USB调试模式，允许电脑调试。
- 电脑需安装好安卓驱动，一般豌豆荚或者各种管家就可以自动帮你装好。
- 电脑需要有[ADB](https://developer.android.com/studio/releases/platform-tools.html)驱动，可以到[这里](https://adb.clockworkmod.com/)下载。
- ADB需要加入环境变量PATH中，方便随时调用。
- 电脑上需要安装Python，因为这是我选择的脚本语言。

专业的开发测试人员，也可以参考我的另外两篇博客：

- [在 Windows 下搭建 Appium + Android 自动化测试环境](https://betacat.online/posts/2017-05-03/setup-appium-automation-test-environment/)
- [在Mac OSX 上配置Appium+Android自动化测试环境](https://betacat.online/posts/2017-12-10/setup-appium-test-environment-on-mac-osx/)

如果只是为了刷金币，只需要安装好驱动和ADB工具即可。

### 刷金币以及英雄熟练度

##### 通用准备

- 电脑需要有[ADB](https://developer.android.com/studio/releases/platform-tools.html)驱动，可以到[这里](https://adb.clockworkmod.com/)下载。
- ADB需要加入环境变量PATH中，方便随时调用。
- 电脑上需要安装Python，因为这是我选择的脚本语言。
- 安装python依赖`pip install -r requirements.txt`

##### huawei mate20准备

- `git checkout mate20`  

`master`分支为模拟器版代码，真机版要切换到`mate20`分支上


##### 雷电模拟器准备
- 电脑需要安装[雷电模拟器](https://www.ldplayer.net/)
- 在雷电模拟器的设置中，性能设置选择`平板版 1280*720 (dpi 240)` （这个貌似是默认设置）


##### 刷金币

1. 运行`python money.py`， 第一次运行需要手动配置英雄阵容，点游戏中的`自动战斗`按钮。


##### 刷英雄熟练度
1. 配置`hero.json`, 配置熟练度未到蓝色的英雄拼音。（配置多个时，每次随机选择一个。建议最少配置两个，防止英雄被别人先选。）
2. 然后运行`python robot.py`


### iPhone
- 真实iPhone（目前只对6s进行适配）
- 安装WDA
- mac用户安装xcode，windows详情可参考微信跳一跳辅助程序相关代码

## 步骤

如果万事具备，那么步骤就非常简单。

### 环境检测
1. 用USB连接手机，如果弹出警告，请允许电脑调试手机。
2. 使用命令 `adb devices` 检验adb和手机状态已经就绪。

```
$ adb devices
List of devices attached
b******4        device
```
模拟点击屏幕，比如你可以打开画图软件，然后运行命令：

```
adb shell input tap 500 500
```
如果如果一切OK，那么你将看到画图软件在坐标（500,500）的位置有一个点。

### 代码实现

通关需要点击的屏幕位置是固定的，加上注释我们只需要不到30行代码就可以完成。

```python
def tap_screen(x, y):
    os.system('adb shell input tap {} {}'.format(x, y))

def do_money_work():
    print('#0 start the game')
    tap_screen(1600, 970)
    sleep(3)

    print('#1 ready, go!!!')
    tap_screen(1450, 910)
    sleep(15)

    print('#2 auto power on!')
    tap_screen(1780, 40)

    for i in range(25):
        tap_screen(1000, 500)
        sleep(1)

    print('#3 do it again...\n')
    tap_screen(1430, 980)
    sleep(3)
```

然后我们写一个主函数来循环刷钱。

```python
if __name__ == '__main__':
    for i in range(repeat_times):
        print('round #{}'.format(i + 1))
        do_money_work()
```

### 拿来主义

如果你喜欢拿来主义，请访问本文项目地址：

- https://github.com/tobyqin/kog-money

然后：
1. 下载项目中的 `kog_simple.py` 到本地，iOS为 `kog_ios.py`
2. 将游戏打开，进入挑战模式，魔女回忆，阵容调整界面。
3. 根据手机性能和分辨率，调整`kog_simple.py`中的参数。（手机分辨率，刷金次数等等）
4. 运行以下命令，手机上就可以查看实时运行效果。

```
python kog_simple.py
```

注意：

1. 每周金币上限4200，需要接近4个小时，不建议一次刷满，手机和你都要休息。
2. 铭文，手机性能，英雄选择都会影响通关速度，自己微调等待时间。
3. 如果你不想被USB数据线束缚，可以考虑[使用无线连接Android真机](https://betacat.online/posts/2017-12-12/connect-adb-via-wifi/)。

## 声明

本脚本纯属娱乐和探索的心得，如果你因为违反了游戏规则导致被封号，我概不负责。
