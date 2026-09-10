# Amos ComfyUI · AutoDL 部署与验证

Amos辰工作台的公开部署配套仓库，用于说明和验证 AutoDL 镜像中的 ComfyUI / MiniMax H3 环境。

**这个仓库公开的是启动、环境验证与使用说明。Amos 工作台以已签名运行程序随镜像提供，核心工作台源码不在本仓库。** ComfyUI 和各模型、节点属于各自上游项目。

## 当前状态

- 云端工作台：r42；Windows 本地客户端：r43。
- 已有实例完成 A-01 / A-02 / A-03 的云端生成与智能体接入短样片测试；本地连接云端路径已测试。
- 公开镜像正在准备关联与审核。新镜像首次拉取验收尚未完成，不能将已有实例测试当作新镜像已经验收。
- 当前定位为试用版本。自动升级、ComfyUI 多版本切换、LTX 跨模型精修和 DLSS 5 不属于已支持功能。

## 开机使用

1. 使用配套 AutoDL 镜像创建实例并开机。生成需要可用 GPU；无卡模式只能管理、设置及检查服务。
2. 从平台打开 **WebUI-6008** 使用 Amos 工作台；**WebUI-6006** 为原生 ComfyUI。
3. 在本机使用 Windows 客户端时，运行 `云端本地运行版.exe`，粘贴平台 WebUI-6008 打开后的**完整网址**，确认连接。外部映射端口不一定是6008，不要手动改写。
4. 下次启动会预填上次成功地址；更换实例时替换地址，成功连接后保存。不要填写SSH命令或Jupyter网址。

## 在镜像内运行本仓库代码

Python 3.10+，仅使用标准库。自测不联网、不使用GPU、不修改环境：

```bash
cd /root/amos-comfyui-autodl
python amos_cloud.py self-test
python amos_cloud.py doctor
```

检查已经启动的服务（不启动推理）：

```bash
python amos_cloud.py smoke
```

手动启动已安装的签名工作台（通常开机脚本已自动启动，无需重复）：

```bash
python amos_cloud.py start
```

`doctor`核对ComfyUI、配套运行程序和Python包版本；`smoke`检查6008工作台身份及6006响应。它们不会下载模型、卸载显存或提交工作流。检查通过不是视频质量保证。

## 目录与自主管理

默认ComfyUI在 `/root/ComfyUI`，工作台r42在 `/root/amos-cloud-r42`。可通过 `COMFY_ROOT` 和 `AMOS_ROOT` 覆盖工具目标。

镜像使用者可以自行添加模型、插件、工作流或另装ComfyUI。Amos的签名只保护自身发行文件，不限制原生ComfyUI。若自行管理ComfyUI启停，在启动环境设置 `AMOS_AUTOSTART_COMFY=0`；需要切换后端时设置 `COMFY_ROOT`。新插件兼容性由对应上游项目决定。

公开模型库是外部挂载/引用，不因保存系统盘镜像就自动打入全部权重。首次使用应检查模型挂载与加载器是否匹配；不要全量下载模型库。

## 反馈

使用GitHub Issues反馈：工作台版本、GPU型号、所选工作流、现象和已脱敏错误。不要公开SSH密码、令牌、完整私有服务地址或个人素材。

## 来源与许可

- ComfyUI：https://github.com/Comfy-Org/ComfyUI
- A-01工作流基于T8（T8star-Aix）；A-02/A-03基于WorkFisher方案，工作流及节点归各作者。
- 模型和第三方节点遵循各自许可；本仓库不重新许可第三方内容。
- 本仓库的配套脚本采用MIT许可；此许可不扩展到未包含的Amos核心程序、模型权重或上游项目。

AutoDL镜像发布需平台审核，本仓库不代表AutoDL官方认证。