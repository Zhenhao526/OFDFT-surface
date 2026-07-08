# Formal Training Progress Report

Date: 2026-07-07

## 目标口径

本轮继续按用户目标推进：以 QE/PBE KSDFT 作为 ground truth，比较 `OFDFT/DFTpy + KSDFT 校正` 与纯 KSDFT 的精度和时间效率；如果误差很大，优先判断是算法物理问题、训练不足，还是流程 bug。

## 本轮新增结论

1. 正式 4x4x4 `Mg(0001)+O` 结构在本机单进程 QE 下过重。
   - 原 `relax` 配置：第一个 65 原子结构 600.56 s timeout。
   - `scf` pilot 配置：同一 65 原子结构 600.07 s timeout，输出显示推进到第 9 次 SCF iteration 但未收敛。
   - 结论：4x4x4 正式 KSDFT ground truth 不适合本机交互式串行跑批，应进入并行/HPC job queue，或先使用中等尺寸 pilot 完成软件闭环。

2. 已跑通一个中等尺寸正式 pilot：`mg0001_o_pilot`。
   - 体系：`Mg(0001)+O`, 3x3x3 slab, 28 atoms per adsorbed structure。
   - 候选结构：12。
   - DFTpy/PBE/WT atomic m100：12/12 收敛，总耗时 25.62 s，median 2.13 s/structure。
   - QE/PBE scf pilot：12/12 收敛，总耗时 1596.71 s，median 134.14 s/structure。
   - raw DFTpy vs QE benchmark：matched 12，speedup 62.31x。
   - 已完成 clean slab / isolated O reference，并写入 adsorption-energy benchmark。

3. 精度仍不可用。
   - raw DFTpy total-energy MAE：539.33 eV。
   - total-energy offset-aligned MAE：48.16 eV。
   - raw adsorption-energy MAE：236.78 eV。
   - adsorption-energy offset-aligned MAE：48.16 eV。
   - Spearman：-0.105，top-1 不匹配。
   - max-force MAE：1307.11 eV/A。
   - 结论：当前 DFTpy/PBE/WT + QE/PAW local-part pseudo 的物理口径仍不适合 Mg/O 表面吸附。

4. delta-learning 在当前小样本上不可靠。
   - 训练/测试：8 train / 4 test。
   - total-energy delta test：raw MAE 57.82 eV，aligned MAE 57.82 eV，Spearman 0.20。
   - adsorption-energy raw DFTpy test：raw MAE 185.37 eV，aligned MAE 45.16 eV，Spearman 0.60。
   - adsorption-energy delta test：raw MAE 3.81 eV，aligned MAE 4.32 eV，Spearman 0.40，top-1 不匹配。
   - 解释：delta 能修掉大部分绝对吸附能偏差，但仍远高于 0.05-0.20 eV 的催化/腐蚀筛选目标，排序也未可靠改善。

5. 新增 4-fold cross-validation 后，delta 结论更稳。
   - total-energy CV：raw DFTpy MAE 539.33 eV，delta MAE 40.96 eV；aligned MAE 从 48.16 eV 到 39.14 eV，仍不可用。
   - adsorption-energy CV：raw DFTpy MAE 236.78 eV，delta MAE 1.56 eV；aligned MAE 从 48.16 eV 到 1.69 eV，Spearman 0.30，top-1 仍不匹配。
   - 解释：交叉验证说明 delta/M-OFDFT 校正确实学到了一部分系统性偏差，但相对能量和排序仍不足以替代 KSDFT。

6. LDA/PBE 对照排除了“只是 XC mismatch”的解释。
   - DFTpy-PBE/WT：adsorption raw MAE 236.78 eV，aligned MAE 48.16 eV，Spearman -0.105，speedup 62.31x。
   - DFTpy-LDA/WT：adsorption raw MAE 230.96 eV，aligned MAE 48.10 eV，Spearman -0.105，speedup 68.99x。
   - LDA adsorption delta CV：raw MAE 1.91 eV，aligned MAE 2.10 eV，Spearman 0.196。
   - PBE adsorption delta CV：raw MAE 1.56 eV，aligned MAE 1.69 eV，Spearman 0.301。
   - 解释：换 XC 只改变绝对偏移和少量 force 误差，没有改善结构相关相对误差和排序；主因更可能是 QE/PAW local-part pseudo 不适合 OFDFT，以及 WT-KEDF 对含氧表面吸附区域的适用性不足。

7. 发现并修复了一个 ground-truth 污染 bug。
   - 正式 `mg0001_o` 旧标签中存在一个 `parsed_converged` 记录，但对应 `pw.out` 只有 2 个 force 行，而结构实际有 65 个原子。
   - 已在 `ofks-parse-ks` 增加 force-count sanity check：如果 QE 输出 force 数量与 `ks_structure` 原子数不一致，标记为 `ks_status=parse_inconsistent`，并不写入 `ks_total_energy_ev`，避免进入 benchmark。
   - 已在 `ofks-prepare-qe-runs` 中把 `parse_inconsistent` 纳入重跑清单，即使旧输出含 `JOB DONE` 也会重跑。

8. 长程训练式扩样本已推进到 50 个 KSDFT 标签。
   - 实装 deterministic lateral jitter，`mg0001_o_pilot_jitter` 生成 465 个候选结构。
   - 从 jitter pool 中抽样 48 个结构，DFTpy-PBE/WT 全部完成；四轮主动选择加最后 6 个结构共新增 38 个 QE/PBE scf 标签，38/38 全部完成并解析收敛。
   - 第二轮选择已支持 `--exclude-records`，可以排除已有 KSDFT 标签；新增 `ofks-combine-records` 用于按 `structure_id` 安全合并长程训练集。
   - 合并后当前 pilot 训练集为 50 个 KSDFT 标签；QE 总耗时 6674.64 s，median 133.27 s/structure；匹配 DFTpy 总耗时 104.76 s，median 2.08 s/structure；speedup 63.71x。
   - all50 raw adsorption MAE 236.13 eV，aligned MAE 31.60 eV，Spearman 0.153，top-1 不匹配。
   - all50 adsorption delta 5-fold CV：raw MAE 0.33 eV，aligned MAE 0.33 eV，Spearman 0.827，top-1 不匹配，top-3 recall 0.0。
   - 趋势：all12 delta CV raw MAE 1.56 eV，all16 约 0.96 eV，all20 约 0.96 eV，all28 约 0.57 eV，all36 约 0.47 eV，all44 约 0.42 eV，all50 降到 0.33 eV；新增数据持续改善 delta 绝对误差和整体排序相关性，但 top-k 命中和筛选级精度仍未达标。
   - 解释：自建 `OFDFT + KSDFT delta` 算法可以在同一 benchmark 框架内对标纯 KSDFT，并带来约 60x 本地单点速度优势；但当前物理底座和特征仍不足，不能替代 KSDFT 做最终判定。

## 关键产物

- 中等尺寸体系配置：`configs/systems/mg0001_o_pilot.yaml`
- 本机可跑 scf pilot QE 配置：`configs/calculators/qe_pbe_formal_scf_pilot.yaml`
- pilot 候选结构：`data/processed/structures/mg0001_o_pilot_candidates.extxyz`
- pilot DFTpy 输出：`data/processed/screens/mg0001_o_pilot_dftpy_pbe_wt_atomic_m100.jsonl`
- pilot KSDFT 标签：`data/processed/labels/mg0001_o_pilot_scf_all12_ks_parsed.jsonl`
- pilot KSDFT 吸附能标签：`data/processed/labels/mg0001_o_pilot_scf_all12_ks_adsorption.jsonl`
- pilot DFTpy 吸附能输出：`data/processed/screens/mg0001_o_pilot_dftpy_pbe_wt_atomic_m100_adsorption.jsonl`
- QE reference 标签：`data/processed/labels/mg0001_o_pilot_references_scf_ks_parsed.jsonl`
- DFTpy reference 输出：`data/processed/screens/mg0001_o_pilot_references_dftpy_pbe_wt_atomic_m100.jsonl`
- raw benchmark：`data/reports/benchmarks/mg0001_o_pilot_scf_all12_dftpy_pbe_benchmark.md`
- adsorption benchmark：`data/reports/benchmarks/mg0001_o_pilot_scf_all12_adsorption_benchmark.md`
- PBE/LDA adsorption benchmark：`data/reports/benchmarks/mg0001_o_pilot_scf_all12_adsorption_pbe_lda_benchmark.md`
- total-energy delta benchmark：`data/reports/benchmarks/mg0001_o_pilot_scf_all12_dftpy_pbe_delta/benchmark.md`
- adsorption delta benchmark：`data/reports/benchmarks/mg0001_o_pilot_scf_all12_ads_delta/benchmark.md`
- total-energy delta CV：`data/reports/benchmarks/mg0001_o_pilot_scf_all12_dftpy_pbe_cv/cv_report.md`
- adsorption delta CV：`data/reports/benchmarks/mg0001_o_pilot_scf_all12_ads_cv/cv_report.md`
- LDA adsorption delta CV：`data/reports/benchmarks/mg0001_o_pilot_scf_all12_lda_ads_cv/cv_report.md`
- jitter 扩展体系：`configs/systems/mg0001_o_pilot_jitter.yaml`
- jitter sample48 结构：`data/processed/structures/mg0001_o_pilot_jitter_sample48.extxyz`
- all50 KSDFT selection：`data/processed/splits/mg0001_o_pilot_all50_ks_batch.jsonl`
- all50 QE runtime 汇总：`data/raw/ksdft/mg0001_o_pilot_all50_qe_run_results.jsonl`
- all50 KSDFT 吸附能标签：`data/processed/labels/mg0001_o_pilot_all50_ks_adsorption.jsonl`
- all50 DFTpy/KS merged 标签：`data/processed/labels/mg0001_o_pilot_all50_dftpy_pbe_ks_ads_merged.jsonl`
- all50 adsorption benchmark：`data/reports/benchmarks/mg0001_o_pilot_all50_adsorption_benchmark.md`
- all50 adsorption CV：`data/reports/benchmarks/mg0001_o_pilot_all50_ads_cv/cv_report.md`
- all50 状态报告：`data/reports/formal_mg0001_o_pilot_all50_status.md`
- 项目完成情况汇报：`data/reports/project_completion_report.md`
- all44 状态报告：`data/reports/formal_mg0001_o_pilot_all44_status.md`
- all36 KSDFT selection：`data/processed/splits/mg0001_o_pilot_all36_ks_batch.jsonl`
- all36 QE runtime 汇总：`data/raw/ksdft/mg0001_o_pilot_all36_qe_run_results.jsonl`
- all36 KSDFT 吸附能标签：`data/processed/labels/mg0001_o_pilot_all36_ks_adsorption.jsonl`
- all36 DFTpy/KS merged 标签：`data/processed/labels/mg0001_o_pilot_all36_dftpy_pbe_ks_ads_merged.jsonl`
- all36 adsorption benchmark：`data/reports/benchmarks/mg0001_o_pilot_all36_adsorption_benchmark.md`
- all36 adsorption CV：`data/reports/benchmarks/mg0001_o_pilot_all36_ads_cv/cv_report.md`
- all36 状态报告：`data/reports/formal_mg0001_o_pilot_all36_status.md`
- all28 KSDFT selection：`data/processed/splits/mg0001_o_pilot_all28_ks_batch.jsonl`
- all28 QE runtime 汇总：`data/raw/ksdft/mg0001_o_pilot_all28_qe_run_results.jsonl`
- all28 KSDFT 吸附能标签：`data/processed/labels/mg0001_o_pilot_all28_ks_adsorption.jsonl`
- all28 DFTpy/KS merged 标签：`data/processed/labels/mg0001_o_pilot_all28_dftpy_pbe_ks_ads_merged.jsonl`
- all28 adsorption benchmark：`data/reports/benchmarks/mg0001_o_pilot_all28_adsorption_benchmark.md`
- all28 adsorption CV：`data/reports/benchmarks/mg0001_o_pilot_all28_ads_cv/cv_report.md`
- all28 状态报告：`data/reports/formal_mg0001_o_pilot_all28_status.md`
- all20 KSDFT 吸附能标签：`data/processed/labels/mg0001_o_pilot_all20_ks_adsorption.jsonl`
- all20 DFTpy/OFDFT 候选输出：`data/processed/screens/mg0001_o_pilot_all_candidate_dftpy_pbe_adsorption.jsonl`
- all20 adsorption benchmark：`data/reports/benchmarks/mg0001_o_pilot_all20_adsorption_benchmark.md`
- all20 adsorption CV：`data/reports/benchmarks/mg0001_o_pilot_all20_ads_cv/cv_report.md`
- all20 状态报告：`data/reports/formal_mg0001_o_pilot_all20_status.md`
- all16 历史状态报告：`data/reports/formal_mg0001_o_pilot_all16_status.md`
- pilot 状态报告：`data/reports/formal_mg0001_o_pilot_all12_status.md`
- 4x4x4 正式状态报告：`data/reports/formal_mg0001_o_status.md`

## 当前判断

这套项目通路已经从 debug 走到“中等尺寸多结构真实 QE 对标”：

```text
结构生成 -> DFTpy/OFDFT 候选 -> 主动选择 -> QE/PBE KSDFT 真值 -> benchmark -> delta 校正
```

但当前算法组合还没有达到可用于催化/腐蚀筛选的精度。误差大的主要原因更像是 OFDFT 物理口径问题，而不是代码跑错：

- DFTpy 密度优化本身可收敛。
- PBE 路径已经通过本地 LibXC shim 跑通。
- debug 和 pilot 都显示力误差异常大。
- 4x4x4 和 3x3x3 的 raw/aligned 总能量误差都远超实用目标。
- delta-learning 的样本数和特征都太弱，只能验证软件流程，不能掩盖 OFDFT 底座误差。

## 下一步

1. 不再把本机单进程 4x4x4 relax 作为主路径；它需要并行/HPC。
2. 以 all50 为当前本机正式训练基线，后续扩展应优先换体系或换物理底座，而不是只在同一 OFDFT 设置下机械加样本。
3. 对 adsorption-energy reference 做生产化修正：spin-polarized O atom、更严格盒长/cutoff/k 点收敛。
4. 准备真正适合 OFDFT 的 local pseudopotential，替代直接读取 QE/PAW UPF local part。
5. 在 local pseudo/KEDF 改善前，delta/M-OFDFT 训练应被视为工程基线，不应宣称可替代 KSDFT。
