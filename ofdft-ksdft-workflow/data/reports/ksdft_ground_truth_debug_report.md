# KSDFT Ground-Truth Debug Benchmark Report

Date: 2026-07-07

## 结论摘要

本项目当前已经建立了以 QE/PBE KSDFT 为 ground truth 的自建算法对标通路：

```text
候选结构 -> 快算法筛选 -> QE/KSDFT 标注 -> delta 校正模型 -> 统一精度/时间 benchmark
```

当前完成的是 `Mg(0001)+O` 的本地 debug benchmark，不是最终生产级 OFDFT 结论。真实 QE 计算已经接通并完成 12 个结构的 KSDFT 单点计算，全部解析为 `ks_status = parsed_converged`。自建算法侧已经有四类候选：确定性的快代理 `raw_fast`、基于 KSDFT 标签训练的 `delta_corrected`、真实 DFTpy-LDA/WT runner、以及通过本地 LibXC 兼容层跑通的 DFTpy-PBE/WT runner。DFTpy runner 已能执行并进入统一 benchmark；经过收敛扫描，`maxiter=100` 可使 12/12 个 Mg/O debug 结构的 DFTpy 密度优化收敛。但由于赝势仍是 QE/PAW UPF 的 local part，且 WT-KEDF 对该吸附体系的相对能量尺度严重失真，当前结果仍不能作为最终 OFDFT 精度结论。

关键结果：

- KSDFT ground truth：QE 7.4.1 + PBE PAW PSL 赝势。
- 数据集：`Mg(0001)+O`，4 个吸附位点，3 个高度，共 12 个结构。
- 训练/测试划分：7 train / 5 test。
- 5 个测试结构的 QE 总耗时：92.67 s，median 18.61 s/structure。
- `raw_fast` 的总能量原始 MAE 为 23575.33 eV，主要是绝对能量零点不同导致的大常数偏移。
- `raw_fast` offset-aligned MAE 为 1.06 eV，Spearman 为 -0.90。
- `delta_corrected` 原始 MAE 降到 1.29 eV，但 offset-aligned MAE 为 1.22 eV，Spearman 为 -0.20。
- `dftpy_lda_wt_m100` 在 12 个结构上 12/12 密度收敛，相对 QE/PBE 的 offset-aligned MAE 仍为 50.88 eV，运行时间约快 9.3x。
- `dftpy_pbe_wt_atomic_m100` 已通过本地 `pylibxc` 兼容层跑通，在 12 个结构上 12/12 收敛；相对 QE/PBE 的 offset-aligned MAE 为 51.37 eV，运行时间约快 9.2x，没有比 LDA/WT 改善。
- `dftpy_lda_wt_atomic_m100 + delta` 在 5 个测试结构上吸附能 raw MAE 为 1.61 eV，aligned MAE 为 1.55 eV，运行时间约快 9.8x；误差仍远高于 0.05-0.20 eV 的实用目标。
- `dftpy_pbe_wt_atomic_m100 + delta` 在 5 个测试结构上吸附能 raw MAE 为 1.53 eV，aligned MAE 为 1.47 eV，运行时间约快 9.6x；比 LDA-delta 略好，但排序 Spearman 为 -0.50，仍不可用于筛选决策。
- 已完成 Mg/O debug 的 KSDFT reference：clean slab `-23011.7128 eV`，isolated O `-558.6014 eV`，并写入 12 个结构的 `ks_adsorption_energy_ev`。
- DFTpy-LDA/WT atomic m100 的 adsorption-energy benchmark：raw MAE 为 250.77 eV，aligned MAE 为 50.73 eV，top-1 不匹配，说明当前 OFDFT 参考能和吸附能口径明显不可用。
- DFTpy-PBE/WT atomic m100 的 adsorption-energy benchmark：raw MAE 为 254.64 eV，aligned MAE 为 51.37 eV，top-1 不匹配，说明问题不是单纯的 LDA/PBE 交换关联泛函不一致。

因此，当前通路可用；DFTpy 也已从“可执行”推进到“可收敛并可跑 PBE debug”，但当前 OFDFT 物理设置还不能替代 KSDFT。下一步应优先解决 OFDFT local pseudopotential 与 KEDF 适用性问题，并把 delta/M-OFDFT 模型扩大到正式训练集。

补充进展：已经完成正式 pilot 批次的 12/12 多结构真值，详见 `data/reports/formal_training_progress_report.md`。本轮发现 4x4x4 `Mg(0001)+O` 在本机单进程 QE 下 600 s 内无法完成一个结构；随后改用 3x3x3 `mg0001_o_pilot` 跑通 12 个真实 QE/PBE scf 标签，并补齐 clean slab / isolated O reference。该 pilot 中 DFTpy/PBE/WT 相对 QE 的 speedup 为 62.31x，但 total-energy offset-aligned MAE 为 48.16 eV，raw adsorption-energy MAE 为 236.78 eV；4-fold adsorption delta CV 把 raw MAE 降到 1.56 eV，但仍远高于可用目标且 top-1 不匹配，说明正式 pilot 也支持“当前 OFDFT 物理底座不可直接替代 KSDFT”的结论。

补充诊断：在同一 12 个 pilot 真值上补跑 DFTpy-LDA/WT 后，LDA adsorption aligned MAE 为 48.10 eV，PBE 为 48.16 eV，Spearman 同为 -0.105；LDA/PBE 几乎没有改变结构相关误差。因此当前大误差不是单纯 LDA/PBE mismatch，优先应检查 OFDFT local pseudopotential 与 KEDF 适用性。

补充扩样本：已实装 deterministic lateral jitter，并从 465 个 jitter 候选中抽样 48 个，完成 DFTpy-PBE/WT 筛选和 38 个新增 QE/PBE scf 标签。合并后 all50 pilot 的 QE 总耗时为 6674.64 s，匹配 DFTpy 总耗时为 104.76 s，speedup 为 63.71x；raw adsorption MAE 为 236.13 eV，aligned MAE 为 31.60 eV，Spearman 为 0.153。5-fold adsorption delta CV 的 raw MAE 为 0.33 eV，aligned MAE 为 0.33 eV，Spearman 为 0.827，但 top-1 和 top-3 仍不匹配。这说明自建 `OFDFT + KSDFT delta` 通路已能和纯 KSDFT 做统一精度/时间对标；增加训练点能明显改善 delta 绝对误差和整体排序相关性，但当前 OFDFT 底座和 top-k 筛选能力仍不足。

## Ground Truth 定义

本项目将收敛的 KSDFT 结果作为内部 ground truth。每个结构以稳定的 `structure_id` 对齐，核心标签为：

- `ks_total_energy_ev`
- `ks_forces_ev_per_ang`
- `ks_max_force_ev_per_ang`
- `qe_runtime_seconds`
- `ks_status = parsed_converged`

当前 QE 环境：

- 执行程序：`_runtime/q-e-7.4.1/bin/pw.x`
- 赝势目录：`pseudo/`
- 赝势：
  - `Mg.pbe-spnl-kjpaw_psl.1.0.0.UPF`
  - `O.pbe-n-kjpaw_psl.1.0.0.UPF`
  - `Al.pbe-n-kjpaw_psl.1.0.0.UPF`
  - `H.pbe-kjpaw_psl.1.0.0.UPF`

## 当前测试体系

配置文件：

- `configs/systems/mg0001_o_debug.yaml`
- `configs/calculators/qe_pbe_smoke.yaml`

体系设置：

- 表面：`Mg(0001)`
- slab：`2 x 2 x 3`
- 真空层：10 A
- 吸附原子：`O`
- 吸附位点：`top`, `bridge`, `fcc`, `hcp`
- 高度：1.6, 2.0, 2.4 A
- 候选结构数：12

这套参数用于本地 debug，目的是让真实 QE 能在本机跑完并生成可解析 benchmark；生产级参数需要更大的 slab、更严格的 cutoff/k 点和更系统的收敛测试。

## Benchmark 结果

结果目录：

- `data/reports/benchmarks/mg0001_o_debug_delta/`
- `data/reports/benchmarks/mg0001_o_debug_dftpy_lda_benchmark.*`
- `data/reports/benchmarks/mg0001_o_debug_dftpy_sweep.md`
- `data/reports/benchmarks/mg0001_o_debug_dftpy_convergence_benchmark.*`
- `data/reports/benchmarks/mg0001_o_debug_dftpy_lda_wt_m100_delta/`
- `data/reports/benchmarks/mg0001_o_debug_dftpy_lda_wt_atomic_m100_delta/`
- `data/reports/benchmarks/mg0001_o_debug_adsorption_benchmark.*`
- `data/reports/benchmarks/mg0001_o_debug_adsorption_pbe_benchmark.*`
- `data/reports/benchmarks/mg0001_o_debug_dftpy_lda_wt_atomic_m100_ads_delta/`
- `data/reports/benchmarks/mg0001_o_debug_dftpy_pbe_wt_atomic_m100_ads_delta/`

汇总表：

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| raw_fast | 5 | 23575.33 | 1.06 | -0.90 | no | 0.0000723 | 1.28e6 |
| delta_corrected | 5 | 1.29 | 1.22 | -0.20 | no | 0.0000723 | 1.28e6 |

真实 DFTpy/WT runner 对全部 12 个结构的 debug benchmark：

| algorithm | matched | converged | raw MAE (eV) | aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_lda_wt_m30 | 12 | 0/12 | 532.80 | 50.88 | 0.154 | no | 21.59 | 10.01 |
| dftpy_lda_wt_m100 | 12 | 12/12 | 532.68 | 50.88 | 0.154 | no | 23.29 | 9.28 |
| dftpy_lda_wt_atomic_m100 | 12 | 12/12 | 532.13 | 50.73 | 0.154 | no | 22.96 | 9.41 |
| dftpy_pbe_wt_atomic_m100 | 12 | 12/12 | 480.37 | 51.37 | 0.154 | no | 23.51 | 9.20 |
| raw_fast | 12 | 12/12 | 23575.50 | 1.00 | -0.664 | no | 0.000219 | 9.89e5 |

DFTpy + KSDFT delta-learning 的 7 train / 5 test benchmark：

| algorithm | matched | raw MAE (eV) | aligned MAE (eV) | Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_lda_wt_m100_raw | 5 | 527.96 | 58.57 | 0.70 | no | 9.64 | 9.61 |
| dftpy_lda_wt_m100_delta | 5 | 1.66 | 1.61 | -0.50 | no | 9.64 | 9.61 |
| dftpy_lda_wt_atomic_m100_raw | 5 | 527.49 | 58.51 | 0.70 | no | 9.49 | 9.76 |
| dftpy_lda_wt_atomic_m100_delta | 5 | 1.60 | 1.55 | -0.50 | no | 9.49 | 9.76 |

Adsorption-energy benchmark using matched KSDFT and DFTpy references:

| algorithm | matched | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | adsorption Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_lda_wt_atomic_m100_ads | 12 | 250.77 | 50.73 | 0.154 | no | 22.96 | 9.41 |
| dftpy_pbe_wt_atomic_m100_ads | 12 | 254.64 | 51.37 | 0.154 | no | 23.51 | 9.20 |

Adsorption-energy delta benchmark, 7 train / 5 test:

| algorithm | matched | adsorption raw MAE (eV) | adsorption aligned MAE (eV) | adsorption Spearman | top-1 | candidate runtime (s) | speedup |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| dftpy_lda_ads_raw | 5 | 246.13 | 58.51 | 0.70 | no | 9.49 | 9.76 |
| dftpy_lda_ads_delta | 5 | 1.61 | 1.55 | -0.50 | no | 9.49 | 9.76 |
| dftpy_pbe_ads_raw | 5 | 249.87 | 59.61 | 0.70 | no | 9.69 | 9.56 |
| dftpy_pbe_ads_delta | 5 | 1.53 | 1.47 | -0.50 | no | 9.69 | 9.56 |

逐结构测试误差：

| structure_id | site | h(A) | KS E(eV) | raw aligned err(eV) | delta err(eV) | QE s | fast s |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| af93973140fe595b | top | 2.0 | -23575.570682 | +0.201399 | +0.498122 | 18.662 | 0.00002000 |
| c0e80c3f8db2ae82 | bridge | 1.6 | -23577.492066 | +2.166369 | +1.815862 | 15.768 | 0.00001242 |
| cf3dec1024a17bba | fcc | 2.0 | -23575.725299 | +0.275999 | -0.680884 | 18.145 | 0.00001904 |
| d6956ca864e76798 | fcc | 2.4 | -23574.090018 | -1.395282 | -1.939492 | 21.488 | 0.00001158 |
| d934123ad1c64e6c | hcp | 2.4 | -23574.216817 | -1.248486 | -1.535958 | 18.607 | 0.00000925 |

## 误差解释

1. 原始总能量 MAE 很大并不代表所有相对趋势都错。
   `raw_fast` 与 KSDFT 的绝对能量零点不同，导致约 23575 eV 的常数偏移。表面吸附问题更应关注相对能量、吸附能、排序和力。

2. offset-aligned 误差仍在 eV 级，说明当前快代理不具备足够物理精度。
   `raw_fast` 的 aligned MAE 为 1.06 eV，`delta_corrected` 为 1.22 eV，二者都不能达到催化/腐蚀筛选中常见的 0.05-0.20 eV 级目标。

3. delta 校正修掉了绝对能量零点，但没有改善排序。
   当前 train set 只有 7 个结构，特征也很粗；`delta_corrected` 只是线性 ridge baseline。它可以验证训练/测试和 benchmark 机制，但不能作为正式 M-OFDFT 精度结论。

4. 当前时间加速比只代表软件通路，不代表真实 OFDFT 加速比。
   `raw_fast` 是本地确定性代理，运行时间接近零。真实结论必须接入 DFTpy/OFDFT/M-OFDFT 后重新统计。

5. DFTpy 的主要问题已经从“数值不收敛”转为“物理口径不一致”。
   初始 `maxiter=30` 时 12/12 不收敛；扫描后 `maxiter=100` 可让 HEG 和 atomic 初始密度配置都达到 12/12 收敛。但收敛后 aligned MAE 仍约 50.7-50.9 eV，说明误差不是单纯由 density optimization 提前停止导致。

6. 当前 DFTpy-delta 能修掉大部分绝对偏差，但仍不是可用精度。
   `dftpy_lda_ads_delta` 的测试吸附能 raw MAE 为 1.61 eV，`dftpy_pbe_ads_delta` 为 1.53 eV，仍高于催化/腐蚀筛选常见目标。Spearman 从原始 DFTpy 的 0.70 变成 -0.50，说明 7 个训练点和简单线性特征不足以稳定保留排序。

7. PBE/LibXC 已经从“阻塞项”变成“debug 可运行项”，但没有解决核心误差。
   当前通过本地 `src/pylibxc/functional.py` 兼容层调用 Homebrew `libxc 7.0.0`，使 DFTpy/PBE 可运行。PBE/WT atomic m100 的 aligned MAE 仍为 51.37 eV，吸附能 raw MAE 仍为 254.64 eV，因此误差不应再归因于单纯 LDA/PBE mismatch。

8. 吸附能 benchmark 排除了“只是总能量零点不同”的解释。
   KSDFT debug 吸附能范围为 -7.18 到 -3.78 eV，而当前 DFTpy-LDA/WT 使用自身 clean slab/O atom reference 后仍给出 127 到 312 eV 的正吸附能。这个量级错误不是常数 offset 可以解决的，更像是当前 OFDFT 赝势/KEDF/XC 组合对含氧吸附体系不适用。

9. 当前最可疑的误差源是 OFDFT local pseudopotential 与 KEDF。
   现有 DFTpy runner 直接读取 QE/PAW UPF 的 local part，并未使用专门为 OFDFT 构造和验证的 bulk-derived local pseudopotential。对于含氧吸附、低配位表面和强密度非均匀区域，WT 类 KEDF 也可能明显超出适用范围。

## 已发现并修复的问题

- 修复 benchmark 中 candidate energy 的字段优先级，避免预测文件里带有 `ks_total_energy_ev` 时泄漏 ground truth。
- 修复 runtime 统计，KSDFT truth 只使用 `qe_runtime_seconds` 或 `ks_runtime_seconds`，候选算法才使用 `runtime_seconds`。
- 修复 ASE/extxyz 读取 `structure_id` 时把十六进制样式字符串解析成 `inf` 的问题。
- `parse_ks_outputs` 增加 `--overlay`，可以在重建 manifest 后保留已完成 QE job 的运行时间和状态。
- 增加 `DftpyCalculatorRunner`，把真实 DFTpy 计算接入现有 `ofks-fast-screen` 和 `ofks-benchmark`。
- benchmark 增加 candidate 收敛计数，避免把非收敛 OFDFT 结果误读成有效精度。
- 增加 `ofks-sweep-dftpy`，用于正式 benchmark 前的小规模 DFTpy 收敛参数扫描。
- 增加 `ofks-merge-candidate-labels`，用于把收敛 DFTpy 输出和 KSDFT 标签合并后训练 delta 校正。
- delta 训练/测试现在会跳过非收敛 candidate，避免把失败 OFDFT 标签喂给模型。
- 增加 `ofks-add-adsorption-energy`，在 clean slab 和 isolated adsorbate reference 能量可用时可写入 `ks_adsorption_energy_ev` 或 `adsorption_energy_ev`。
- benchmark 在发现吸附能字段时会额外输出 adsorption-energy MAE/RMSE、offset-aligned error 和排序指标。
- 完成 Mg/O debug 的 QE clean slab 与 isolated O reference 单点计算，并生成 `mg0001_o_debug_ks_adsorption.jsonl`。
- 完成 DFTpy-LDA/WT atomic m100 的 clean slab 与 isolated O reference，并生成 adsorption-energy benchmark。
- 增加本地 `pylibxc.functional` 兼容层，使 DFTpy/PBE debug 路径可调用 Homebrew `libxc 7.0.0`。
- 完成 DFTpy-PBE/WT atomic m100 的 12 结构 benchmark、clean slab/O reference 和 adsorption-energy benchmark。
- 修复 adsorption-only delta benchmark 的 Markdown 汇总表，使总表能显示吸附能 raw/aligned MAE、Spearman 和 top-1。

## 下一步执行建议

优先级 1：把 DFTpy runner 从“可收敛”推进到“物理口径可用于科学 benchmark”。

- 将当前本地 `pylibxc` 兼容层替换或补强为正式可维护的 LibXC 依赖路径；当前兼容层只覆盖 debug 所需的 unpolarized LDA/GGA。
- 准备 Mg/O/Al/H 的 OFDFT local pseudopotential，避免直接把 QE/PAW UPF 的 local part 当生产 OFDFT 输入。
- 当前 `maxiter=100`, `grid_spacing=0.8`, `WT/LDA/PBE` 已实现 12/12 density 收敛；后续收敛测试应重点转向 local pseudopotential、KEDF 族和吸附能参考态。
- 输出继续沿用现有 benchmark contract：`structure_id`, `total_energy_ev`, `forces_ev_per_ang`, `max_force_ev_per_ang`, `runtime_seconds`, `backend=dftpy`。

优先级 2：把 debug 吸附能 benchmark 扩展为生产级吸附能 benchmark。

- 当前 debug reference 已完成；生产级需要重新以更严格 cutoff/k 点、spin-polarized isolated O、合适盒长和收敛阈值计算 reference。
- 使用 `ofks-add-adsorption-energy` 对正式结构输出 `ks_adsorption_energy_ev` 和 `adsorption_energy_ev`。
- adsorption-energy benchmark 已能输出 MAE/RMSE、offset-aligned error 和排序指标。

优先级 3：扩大数据规模。

- 本地科学 benchmark：50-100 个结构。
- 生产 benchmark：200+ 个结构，覆盖 `H/Al(111)`, `O/Mg(0001)`, `H2O/Al(111)`。
- 每个体系至少保留 clean slab、单分子/原子、低覆盖度吸附、不同位点和高度。

优先级 4：正式比较算法族。

- `raw_ofdft`
- `m_ofdft`
- `delta_ofdft`
- `ml_surrogate`
- `ksdft_qe_pbe` ground truth

所有算法必须进入同一个 `ofks-benchmark` 或 `ofks-evaluate-delta` 框架，避免不同脚本口径下的误差和时间不可比。

优先级 5：把“自建算法 vs 纯 KSDFT”的验收标准固定下来。

- ground truth：同一结构的 QE/PBE KSDFT 单点能、力和吸附能。
- accuracy：总能量相对误差、吸附能 MAE/RMSE、Spearman 排序、top-k recall、力误差。
- cost：候选算法 wall time、KSDFT wall time、speedup_vs_truth。
- 通过线：吸附能 MAE 先以 `<0.20 eV` 作为阶段目标，top-3 recall 明显高于随机基线；正式目标再收紧到 `<0.05-0.10 eV`。
