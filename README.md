# OpenART Mini 板级显示与 SPI 验证

逐飞 OpenART Mini 板上的 ST7789 屏驱与 SPI 收发验证片段，用于把摄像头画面搬到板载小屏上显示；不是业务主程序。

## 这个工程做什么

- `st7789_openart_mini.py`：1.54 寸 240×240 ST7789 SPI 屏驱动（`_init` / `fill` / `pixel` / `image` / `show_string`），并把摄像头 320×240 RGB565 画面居中裁成 240×240 后循环刷到屏幕，约 30 FPS。
- `openart_spi_test.py`：最小 SPI 收发测试，用来先确认总线通不通。
- 平台特征：OpenMV 兼容 MicroPython 的 `machine.SPI` / `Pin`；与 OMV RT5 同属 OpenMV 生态（那边是整机识别程序），与 K230 完全不同。

## 部署

1. **烧固件**：给 OpenART Mini 烧录带 `machine.SPI` 的 OpenMV 兼容 MicroPython 固件。
2. **接线**：屏与板子按脚本里的定义连接 —— SPI3(30)、40 MHz、mode 0；`CS = B3`、`DC = B13`、`RST = B12`、`BLK = B2`（背光可省略）。引脚与实际板卡不符时改脚本末尾的 `Pin(...)` 即可。
3. **先测总线**：运行 `openart_spi_test.py`。注意原文件第一行 `from machime import SPI` 是笔误，**改成 `from machine import SPI` 才能跑**（仓库保留原文便于对照）。
4. **跑显示**：把 `st7789_openart_mini.py` 拷到板子根目录并运行（或另存为 `main.py` 上电自启）。脚本会 `sensor.reset()` → RGB565 → QVGA → 开窗 240×240 → 白屏 → 循环显示。
5. **验证**：屏幕先亮白底，随后出现实时画面。若颜色异常，检查 `image()` 里的字节序交换；若黑屏，先查 `BLK` 背光与 `RST` 时序。

## 第三方内容（均未上传）

固件提供的 `machine` / `SPI` / `Pin` 模块来自 OpenMV 项目，板级支持库与配套例程来自逐飞科技；ST7789 初始化序列与显示逻辑为本仓库自写实现。厂商资料请到各自开源仓库获取。

## 项目系列

同一竞赛项目按**硬件环境**拆分的独立仓库，各平台固件 API 与运行栈互不相通，代码不能混用。

| 硬件环境 / 运行栈 | 仓库 |
| --- | --- |
| 嘉楠 K230 · CanMV K230（MicroPython 固件） | [canmv-k230-vision](https://github.com/kevin-kaisilanna/canmv-k230-vision) |
| 逐飞 OMV RT5 · OpenMV 兼容固件 | [omv-rt5-openmv-vision](https://github.com/kevin-kaisilanna/omv-rt5-openmv-vision) |
| 逐飞 OpenART Mini · 板级显示 / SPI | **openart-mini-display** ← 本仓库 |
| KICKPI K7C · RK3576（Ubuntu + CPython/OpenCV） | [rk3576-k7c-vision](https://github.com/kevin-kaisilanna/rk3576-k7c-vision) |
| 竞赛设计报告（跨平台文档，无代码） | [rolling-ball-design-report](https://github.com/kevin-kaisilanna/rolling-ball-design-report) |

> 所有仓库均只收录自研代码；第三方开源库、厂商 SDK、平台生成代码与预训练模型未上传，来源见各仓库 README。

## 许可证

仅收录自研代码，尚未指定开源许可证（默认保留所有权利）；第三方组件权利归各自权利人。
