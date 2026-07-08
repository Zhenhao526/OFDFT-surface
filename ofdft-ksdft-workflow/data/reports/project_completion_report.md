# OFDFT/KSDFT 项目完成情况汇报

Date: 2026-07-07

## 目标

本项目目标是建立一条可落地的计算通路：以 QE/PBE KSDFT 作为 ground truth，测试多个真实表面吸附结构，比较 `OFDFT/DFTpy + KSDFT 校正` 与纯 KSDFT 的精度和时间效率；若误差较大，则分析问题来源和可能 bug。

## 已完成范围

- 真实 QE 环境已接通：`_runtime/q-e-7.4.1/bin/pw.x`
- 赝势已配置：Mg/O/Al/H 的 PBE PAW PSL UPF
- 正式 pilot 体系：`Mg(0001)+O`, 3x3x3 slab, 28 atoms per adsorbed structure
- 候选池：60 个 DFTpy/PBE/WT 吸附结构，其中 50 个已完成 KSDFT 标签
- reference：clean Mg slab 与 isolated O 已完成 QE/PBE 与 DFTpy/PBE reference
- 对标指标：吸附能 MAE/RMSE、offset-aligned MAE、Spearman、top-k recall、wall time、speedup
- bug 修复：QE force 行数与结构原子数不一致时标记为 `parse_inconsistent`，防止 ground truth 污染
- 自动化增强：active selection 支持 `--exclude-records`，新增 `ofks-combine-records` 安全合并长程训练集

## 最终 all50 结果

| item | value |
| --- | ---: |
| KSDFT labels | 50/50 parsed_converged |
| QE/PBE total runtime | 6674.64 s |
| QE/PBE median runtime | 133.27 s/structure |
| DFTpy matched total runtime | 104.76 s |
| DFTpy median runtime | 2.08 s/structure |
| speedup vs KSDFT | 63.71x |

| algorithm | adsorption raw MAE | adsorption aligned MAE | Spearman | top-1 | top-3 recall |
| --- | ---: | ---: | ---: | --- | ---: |
| raw DFTpy/PBE/WT | 236.13 eV | 31.60 eV | 0.153 | no | 0.0 |
| DFTpy/PBE/WT + delta, 5-fold CV | 0.33 eV | 0.33 eV | 0.827 | no | 0.0 |

## 学习曲线

| dataset | KS labels | delta CV adsorption MAE | Spearman | note |
| --- | ---: | ---: | ---: | --- |
| all12 | 12 | 1.56 eV | 0.301 | 初始正式 pilot |
| all16 | 16 | 0.96 eV | 0.271 | jitter 第一批部分标签 |
| all20 | 20 | 0.96 eV | 0.299 | jitter 第一轮完整标签 |
| all28 | 28 | 0.57 eV | 0.487 | 第二轮标签 |
| all36 | 36 | 0.47 eV | 0.643 | 第三轮标签 |
| all44 | 44 | 0.42 eV | 0.747 | 第四轮标签 |
| all50 | 50 | 0.33 eV | 0.827 | 当前本机正式基线 |

## 结论

通路已经跑通，并且 all50 结果说明 `OFDFT/DFTpy + KSDFT delta` 相对纯 KSDFT 有稳定的本机速度优势，约 64x。增加 KSDFT 标签后，delta 模型的吸附能 MAE 从 all12 的 1.56 eV 降到 all50 的 0.33 eV，排序相关性也提高到 Spearman 0.827。

但当前设置仍不能替代 KSDFT 做催化/腐蚀筛选。raw DFTpy/PBE/WT 的吸附能误差是百 eV 量级，offset-aligned 后仍有 31.60 eV；delta 后虽然降到 0.33 eV，但仍高于常见筛选目标 0.05-0.20 eV，且 top-1/top-3 仍未命中。

## 误差来源判断

当前大误差不像是流程 bug，主要证据如下：

- QE/PBE 真实计算 50/50 正常完成并解析收敛。
- `parse_ks_outputs` 已增加 force-count sanity check，旧的错读输出不会进入 benchmark。
- DFTpy 密度优化可收敛，PBE 路径已通过本地 LibXC shim 跑通。
- LDA/PBE 对照显示二者对结构相关误差和排序改善有限，排除了“只是 XC mismatch”的解释。
- raw OFDFT 的力误差和吸附能量级异常大，更符合 OFDFT local pseudopotential/KEDF 物理适用性问题。

最可疑的误差源是：直接读取 QE/PAW UPF local part 不等价于生产级 OFDFT local pseudopotential；WT 类 KEDF 对含氧吸附、低配位表面和强非均匀密度区域适用性不足。

## 主要产物

- all50 状态报告：`data/reports/formal_mg0001_o_pilot_all50_status.md`
- all50 KSDFT 标签：`data/processed/labels/mg0001_o_pilot_all50_ks_adsorption.jsonl`
- all50 QE runtime：`data/raw/ksdft/mg0001_o_pilot_all50_qe_run_results.jsonl`
- all50 benchmark：`data/reports/benchmarks/mg0001_o_pilot_all50_adsorption_benchmark.md`
- all50 delta CV：`data/reports/benchmarks/mg0001_o_pilot_all50_ads_cv/cv_report.md`
- 正式进展报告：`data/reports/formal_training_progress_report.md`
- ground-truth debug 报告：`data/reports/ksdft_ground_truth_debug_report.md`

## 下一步建议

1. 把 all50 固定为当前本机正式基线，避免只在同一错误物理底座上继续机械加样本。
2. 准备并验证真正适合 OFDFT 的 Mg/O local pseudopotential。
3. 系统比较 KEDF 族，而不只使用当前 WT 设置。
4. 对 reference 做生产级修正，包括 spin-polarized O atom、更严格 vacuum/cutoff/k-point 收敛。
5. 将 4x4x4 生产结构迁移到并行/HPC 队列，本机单进程 600 s 内无法稳定完成。
6. 在物理底座修正后重新训练 M-OFDFT/delta 模型，并以 adsorption MAE < 0.20 eV 和 top-k recall 显著高于随机作为下一阶段门槛。
