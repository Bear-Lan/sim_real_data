# 三任务仿真 / 真机数据包

本数据包整理 Adjust_Bottle、Grab_Roller、Stack_Bowls_Two：每个任务仿真 100 条、真机 100 条，共 600 条 episode。原数据保留，本文件夹是完整独立副本，不依赖原路径的链接。

## 新增真机 transfer 任务

`real-transfer-20261010` Release 单独提供原始 `transfer` 真机数据：LeRobot v3、30 Hz、100 条 episode、100,681 帧、三路 AV1 视频及 18 维状态/动作，原始文件约 2.56 GiB。保留采集时全部记录，不重编码、不重采样。该任务没有配套仿真数据。其中 episode 18 只有 5 帧、episode 72 只有 2 帧，下载后的 `transfer_inventory.json` 列出逐条长度及逐文件 SHA256；原始采集条数不等于已重新审核的成功示范条数。

```powershell
python download_data.py --output E:/datasets/sim_real_data --task transfer
```

该命令仅下载新增任务，校验后还原至 `real/transfer`。原有默认下载命令仍下载最初六组600条数据，原有 Release 保留。

## GitHub 下载方式（不使用 Git LFS）

完整数据体积约 113 GiB，不放入普通 Git，也不使用 Git LFS。仓库保存说明、映射参考和下载脚本；完整原始数据放在本仓库的 GitHub Release 分卷附件中。Release 只有在全部附件上传、数量及传输校验通过后才会发布；发布前不会向读者提供不完整的数据下载。

下载时需要 Python 3.10 或更新版本。安装 Python 后，在本仓库克隆目录运行：

```powershell
python download_data.py --output E:/datasets/sim_real_data
```

也可以只下载某一个任务：

```powershell
python download_data.py --output E:/datasets/sim_real_data --task Grab_Roller
```

脚本逐卷校验 SHA256，合并、解压至 sim / real 对应任务目录。原始数据和校验文档保留原格式。完整下载需要约 113 GiB 的数据空间，另需保留最大单任务压缩包的临时空间；建议准备至少 200 GiB 可用空间。此处公开的是实验采集数据，不包含 SSH / Hugging Face / GitHub 凭据。

```text
sim_real_data/
  sim/Adjust_Bottle/       100 条成功仿真 episode
  sim/Grab_Roller/         100 条成功仿真 episode（64 + 36 条续采）
  sim/Stack_Bowls_Two/     100 条成功仿真 episode
  real/Adjust_Bottle/      真机 LeRobot v3，100 条
  real/Grab_Roller/        真机 LeRobot v3，100 条
  real/Stack_Bowls_Two/    真机 LeRobot v3，100 条
  reference/              已有接口映射代码与说明
  sim_inventory.json      仿真来源、episode、文件大小清单
  real_inventory.json     真机来源、文件大小及 SHA256
  verification_report.json  最终数量和复制校验报告
```

## 数据格式

仿真保留原始 10 Hz 记录：每条包含 metadata.json、frames.jsonl、diagnostics.jsonl，以及 front / left_wrist / right_wrist 三路 PNG。未做视频有损压缩、重采样、单位转换或训练。

真机保留原始 LeRobot v3 的 data / meta / videos / images 目录，30 Hz。v3 的一份 Parquet / MP4 可包含多条 episode，不应按文件个数统计轨迹条数；应读取 meta 和 episode_index。

动作和状态均为 18 维：右臂关节 0–5、右夹爪 6、左臂关节 7–12、左夹爪 13、底盘速度 14–16、升降 17。左右按机器人自身定义，不按面对机器人的画面左右定义。

## 使用前注意

1. 仿真夹爪字段是两指总开口（米），真机字段是电机角度（弧度）。已有 V2 换算为 `real_gripper_rad = sim_opening_m / 0.10 * (-4.5)`；升降的米 / 毫米换算为 `real_height_mm = sim_height_m * 1000`。本包保留原单位，没有套用换算。
2. reference 中的映射文档来自 Adjust_Bottle 的既有训练实验；它不是另外两个任务已完成跨域校准的证明。手臂零位、方向、相机、限位、起始姿态和动力学仍需核对。
3. 仿真 Stack_Bowls_Two 按场景指定的底碗先搬：bowl0 右手、bowl1 左手；底碗可随机变化。已检查的真机 100 条都是右手先、左手后，本次仅整理，不改动顺序或重新筛选。
4. 仿真 success=true 是仿真采集判定，不代表真机部署安全；真机 100 条是原始采集条数，不额外宣称已用仿真判据重新审核成功率。
5. 将整个 sim_real_data 文件夹发给对方即可。只有 verification_report.json 的 status 为 verified_complete 时，本次整理才算完成。

## 复制校验

仿真导出只选 success=true 且 complete=true 的完整 episode，核对轨迹帧数、三路图像文件名、时间戳和数值有限性。服务器低优先级无损归档；下载归档 SHA256 校验通过后解包，并核对每个文件大小和每条 metadata 的 SHA256。真机按实际 Parquet episode_index 验证 100 条和总帧数，复制后逐文件 SHA256 比较。原始采集的图像内容验证报告（若有）独立于本次传输校验。
