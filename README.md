# 仿真 / 真机机器人数据集（801 条记录）

本仓库发布5个任务、8组原始数据，共 **801 条 episode：仿真300条、真机501条**。Adjust_Bottle、Grab_Roller、Stack_Bowls_Two 各有仿真100条和真机100条；transfer 只有真机100条；PickBall 只有真机101条。数据本体保存在三个已公开的 GitHub Release 中，克隆仓库只获得说明、下载脚本和清单。

## 数据总览

| 任务 | 仿真 episode / 帧数 | 真机 episode / 帧数 | Release |
| --- | --- | --- | --- |
| Adjust_Bottle | 100 / 41,049 | 100 / 78,591 | dataset-20261006 |
| Grab_Roller | 100 / 16,041 | 100 / 53,235 | dataset-20261006 |
| Stack_Bowls_Two | 100 / 66,648 | 100 / 78,245 | dataset-20261006 |
| transfer | 无 | 100 / 100,681 | real-transfer-20261010 |
| PickBall | 无 | 101 / 32,942 | real-pickball-20261022 |
| 合计 | 300 / 123,738 | 501 / 343,694 | 三个 Release |

- [原有三个任务：600条数据](https://github.com/Bear-Lan/sim_real_data/releases/tag/dataset-20261006)，原始文件约113.4 GiB。
- [新增 transfer 真机任务：100条记录](https://github.com/Bear-Lan/sim_real_data/releases/tag/real-transfer-20261010)，原始文件约2.56 GiB。
- [新增 PickBall 真机任务：101条记录](https://github.com/Bear-Lan/sim_real_data/releases/tag/real-pickball-20261022)，原始文件约0.71 GiB。

合计原始文件125,267,243,853字节，约116.7 GiB。三批独立发布，原有600条数据与 transfer 的 Release 和校验清单保持不变。

## 新增真机 transfer 任务

`real-transfer-20261010` Release 单独提供原始 `transfer` 真机数据：LeRobot v3、30 Hz、100 条 episode、100,681 帧、三路 AV1 视频及 18 维状态/动作，原始文件约 2.56 GiB。保留采集时全部记录，不重编码、不重采样。该任务没有配套仿真数据。其中 episode 18 只有 5 帧、episode 72 只有 2 帧，下载后的 `transfer_inventory.json` 列出逐条长度及逐文件 SHA256；原始采集条数不等于已重新审核的成功示范条数。

```powershell
python download_data.py --output E:/datasets/sim_real_data --task transfer
```

该命令仅下载新增任务，校验后还原至 `real/transfer`。原有默认下载命令仍下载最初六组600条数据，原有 Release 保留。

## 新增真机 PickBall 任务

`real-pickball-20261022` Release 单独提供原始 `PickBall` 真机数据：LeRobot v3.0、**20 Hz**、101 条 episode、32,942 帧、front / left_wrist / right_wrist 三路 AV1（480×640、crf 30）、18 维状态/动作，`robot_type=hei_rebot_lift_client`，原始文件约 0.71 GiB。保留采集时全部记录，不重编码、不重采样、不重新筛选。该任务没有配套仿真数据。

```powershell
python download_data.py --output E:/datasets/sim_real_data --task PickBall
```

校验后还原至 `real/PickBall`。该批的逐条长度、文件大小及 SHA256 记录在 `pickball_inventory.json`，Release 内另有一份 `pickball_release_manifest.json`。

与 transfer 不同的是，本批 101 条记录长度分布正常：最短 252 帧、最长 493 帧、均值 326 帧（20 Hz 下约 12.6–24.7 秒），没有低于 30 帧的残片。101 是采集时的实际条数，不是 100 条筛出来的结果。

## GitHub 下载方式（不使用 Git LFS）

数据不放入普通 Git，也不使用 Git LFS。仓库保存说明、映射参考和下载脚本；原始数据放在上述三个已发布的 GitHub Release 分卷附件中，全部分卷已核对大小和 SHA256。

下载需要 Git 和 Python 3.10 或更新版本。脚本只使用 Python 标准库，公开下载无需账号或 token。先克隆仓库：

```powershell
git clone https://github.com/Bear-Lan/sim_real_data.git
cd sim_real_data
```

下载全部 **801条**需要执行以下三条命令，使用同一个输出目录：

```powershell
python download_data.py --output E:/datasets/sim_real_data
python download_data.py --output E:/datasets/sim_real_data --task transfer
python download_data.py --output E:/datasets/sim_real_data --task PickBall
```

**默认命令仅下载原有600条，不包含 transfer 和 PickBall。** 带 `--task` 时脚本按任务选择对应 Release；其他任务及默认命令选择原有 Release。可用 `--tag` 显式指定标签。也可以只下载某一个原有任务的仿真和真机数据：

```powershell
python download_data.py --output E:/datasets/sim_real_data --task Grab_Roller
```

脚本逐卷校验 SHA256，按顺序合并并核对完整压缩包 SHA256 后，解压至 sim / real 对应任务目录。分卷是同一压缩包的连续字节段，不能单独解压，无需手动合并。原始数据和校验文档保留原格式。全部801条需要约117 GiB数据空间及最大单任务压缩包的临时空间，建议至少200 GiB可用空间。解压完成后脚本删除自己的临时压缩包，保留数据和恢复记录。

以下目录对应三条下载命令均执行完成后的输出：

```text
sim_real_data/
  sim/Adjust_Bottle/       100 条成功仿真 episode
  sim/Grab_Roller/         100 条成功仿真 episode（64 + 36 条续采）
  sim/Stack_Bowls_Two/     100 条成功仿真 episode
  real/Adjust_Bottle/      真机 LeRobot v3，100 条
  real/Grab_Roller/        真机 LeRobot v3，100 条
  real/Stack_Bowls_Two/    真机 LeRobot v3，100 条
  real/transfer/           真机 LeRobot v3，100 条（含两条极短记录）
  real/PickBall/           真机 LeRobot v3，101 条（20 Hz）
  reference/              已有接口映射代码与说明
  sim_inventory.json      仿真来源、episode、文件大小清单
  real_inventory.json     真机来源、文件大小及 SHA256
  verification_report.json  原有600条数据的复制校验报告
  transfer_inventory.json   transfer 逐条长度、文件大小及 SHA256
  pickball_inventory.json   PickBall 逐条长度、文件大小及 SHA256
```

## 数据格式

仿真保留原始 10 Hz 记录：每条包含 metadata.json、frames.jsonl、diagnostics.jsonl，以及 front / left_wrist / right_wrist 三路 PNG。未做视频有损压缩、重采样、单位转换或训练。

真机保留原始 LeRobot v3 的 data / meta / videos / images 目录。既有三组及 transfer 为 30 Hz，PickBall 为 20 Hz。v3 的一份 Parquet / MP4 可包含多条 episode，不应按文件个数统计轨迹条数；应读取 meta 和 episode_index。

动作和状态均为 18 维：右臂关节 0–5、右夹爪 6、左臂关节 7–12、左夹爪 13、底盘速度 14–16、升降 17。左右按机器人自身定义，不按面对机器人的画面左右定义。

## 使用前注意

1. 仿真夹爪字段是两指总开口（米），真机字段是电机角度（弧度）。已有 V2 换算为 `real_gripper_rad = sim_opening_m / 0.10 * (-4.5)`；升降的米 / 毫米换算为 `real_height_mm = sim_height_m * 1000`。本包保留原单位，没有套用换算。
2. reference 中的映射文档来自 Adjust_Bottle 的既有训练实验；它不是其他任务已完成跨域校准的证明。手臂零位、方向、相机、限位、起始姿态和动力学仍需核对。
3. 仿真 Stack_Bowls_Two 按场景指定的底碗先搬：bowl0 右手、bowl1 左手；底碗可随机变化，100条中61条左手先、39条右手先。已检查的真机100条都是右手先、左手后，发布时不改动顺序或重新筛选。
4. 仿真 success=true 是仿真采集判定，不代表真机部署安全；真机 100 条是原始采集条数，不额外宣称已用仿真判据重新审核成功率。
5. transfer 原样保留 episode 18（5帧）和 episode 72（2帧）。训练时可按自己的规则筛选；100条原始记录不等于100条已审核的成功示范。该任务没有配套仿真数据。
6. PickBall 为 20 Hz、101 条、无配套仿真数据，采集时的任务文本为 `PickBall`，`robot_type=hei_rebot_lift_client`。它与 transfer 共用 18 维状态/动作定义，但频率不同，混合训练前需重采样；它的 101 条同样只是原始采集条数，未标注成败。

## 复制校验

仿真导出只选 success=true 且 complete=true 的完整 episode，核对轨迹帧数、三路图像文件名、时间戳和数值有限性。服务器低优先级无损归档；下载归档 SHA256 校验通过后解包，并核对每个文件大小和每条 metadata 的 SHA256。真机按实际 Parquet episode_index 验证 100 条和总帧数，复制后逐文件 SHA256 比较。原始采集的图像内容验证报告（若有）独立于本次传输校验。

transfer 核对100个 episode ID、100,681帧、逐条长度、帧编号、状态/动作有限性及 metadata 引用的视频文件存在性。无损归档中的20个源文件均逐文件核对 SHA256，分卷核对 GitHub 返回的大小与 SHA256。未额外执行整段视频解码审计或任务成功率审核。

PickBall 核对101个 episode ID 连续覆盖 0–100、32,942帧、逐条长度与 data parquet 行数逐条一致、`observation.state` / `action` 全部有限、三路相机9个 mp4 存在且非空，18个源文件逐个记录 SHA256。同样未执行整段视频解码审计或任务成功率审核。

`verification_report.json`、`sim_inventory.json` 和 `real_inventory.json` 仅覆盖原有600条。transfer 与 PickBall 的校验范围和逐条长度分别记录在 `transfer_inventory.json`、`pickball_inventory.json`。仓库中的 `release_manifest.json` 对应原有600条，`transfer_release_manifest.json` 对应 transfer 的100条，`pickball_release_manifest.json` 对应 PickBall 的101条；三份清单均为 `status=verified_complete`。三个 Release 的附件各自有一份清单，下载脚本按所选 Release 读取，不将清单混用。
