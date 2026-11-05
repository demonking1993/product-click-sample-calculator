# 测款神器 · Product Click Sample Calculator

一个用于电商选品和投放前规划的桌面可视化工具：根据预计购买率、观测可信度和允许的相对误差，测算至少需要多少有效访问样本，帮助评估产品转化表现所需的数据量。

## 主要功能

- 调整观测可信度 `a`、允许上下浮动比例 `r` 和预计真实购买率 `p1`。
- 自动计算最低测试人流量，并将样本量向上取整。
- 展示预计购买人数、购买率参考范围和对应购买人数范围。
- 展示计算依据，支持恢复默认参数和复制完整计算结果。
- 使用 Python / Tkinter 实现本地桌面界面，无需账号或联网服务。
- 包含 Windows 打包脚本、macOS Universal2 打包脚本及现有双系统交付包。

## 默认示例

| 参数或结果 | 数值 |
| --- | --- |
| 观测可信度 | 80% |
| 允许相对浮动 | ±20% |
| 预计真实购买率 | 3% |
| 最低测试人流量 | 1,328 人 |
| 预计购买人数 | 约 39.8 人 |
| 购买率参考范围 | 2.40%～3.60% |
| 对应购买人数 | 32～47 人 |

## 计算方法与适用范围

采用二项分布的正态近似进行样本量规划：

```text
z = 标准正态分布在 (1 + a) / 2 处的分位数
m = ceil(z² × (1 - p1) / (r² × p1))
购买率参考范围 = p1 × (1 ± r)
```

公式中的 `a`、`r` 和 `p1` 使用小数形式；界面中输入百分数。

这个工具计算的是估计购买率所需的样本量。它没有读取实际订单、计算实际观测数据的置信区间或自动判定“爆款”。界面中的“p2 可信范围”由输入的预计购买率及允许浮动直接生成，用于规划参考。

“人流量”应使用与购买率分母一致的有效访问或独立访客口径；如果使用广告点击量，应先核对重复点击与访客的统计口径。实际测款时应尽量保持流量来源、价格、素材和投放时段可比。样本少或购买事件少时，正态近似存在局限。

## 从源码运行

建议使用 Python 3.10 或更新版本，并安装带 Tk 支持的 Python。

```bash
python app.py
```

应用运行只使用 Python 标准库，不需要额外的 pip 运行依赖。

## 测试

```bash
python -m unittest -v test_app.py
```

现有测试覆盖默认 3% 购买率、12% 购买率和部分无效参数。

## 打包与交付

### Windows

```powershell
python -m pip install -r requirements-build.txt
powershell -ExecutionPolicy Bypass -File .\build.ps1
```

输出为 `dist/StyleTestTool.exe`。`make_icon.py` 生成图标时优先使用 Windows 微软雅黑字体。

### macOS

在 Mac 上安装带 Tk 和 Universal2 支持的 Python，然后执行：

```bash
zsh build_macos.sh
```

脚本会创建构建虚拟环境，生成 Universal2 应用并执行本地临时签名，输出 `dist/测款神器-Mac-universal.zip`。脚本会清理当前项目下的 `build/` 和 `dist/`。未包含 Apple Developer ID 签名或公证流程。

### 已有交付包

仓库中的 `测款神器-双系统交付版.zip` 为本地已有的 v1.0 双系统交付归档，内含 Windows EXE、Mac DMG 和使用说明；本次归档没有重新构建安装包。

## 项目文件

| 文件 | 用途 |
| --- | --- |
| `app.py` | 样本量计算与 Tkinter 桌面界面 |
| `test_app.py` | 计算函数测试 |
| `build.ps1` | Windows 打包 |
| `build_macos.sh` | macOS Universal2 打包 |
| `make_icon.py`、`app.ico`、`app_1024.png` | 图标生成与图标资源 |
| `StyleTestTool.spec`、`version_info.txt` | Windows 构建与版本配置 |
| `requirements-build.txt` | Windows 构建所需依赖 |
| `使用说明.txt`、`Mac使用说明.txt`、`双系统交付说明.txt` | 使用与交付说明 |
| `测款神器-双系统交付版.zip` | 现有 Windows / Mac 交付归档 |

构建中间产物、重复安装包、Python 缓存及含其他桌面窗口内容的历史全屏截图不纳入版本控制。
