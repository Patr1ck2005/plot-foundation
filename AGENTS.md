# Plot Foundation Agent Instructions

Navigation: [Repository homepage](README.md) · [Research-system map](D:/Obsidian/MyPhysics/System/Research-System-Map.md).

For work belonging to the user's research system, actually read the canonical
[MyPhysics system entry](D:/Obsidian/MyPhysics/System/README.md). Research figure
delivery is maintained in [style-policy.md](docs/style-policy.md#a4-paper-delivery);
do not copy its numerical requirements into consumer rule documents. This
pointer does not change this library's domain-neutral boundaries below.

## Mission

Provide reusable, domain-neutral plotting specifications, style policy, and
backend renderers. The package must not know about a scientific domain,
simulator, DataFrame, manifest, registry, or consumer output workflow.

## Boundaries

- Public inputs are arrays and typed models.
- Renderers draw on caller-owned axes and never create directories or close figures.
- Saving requires an explicit path and never creates parent directories.
- Domain meaning and schema mapping remain in consumer adapters.
- Matplotlib global state must not be mutated at import time. Use scoped style
  contexts.
- New primitives require a consumer characterization case and package tests.

## Data-space decision invariant

Plot Foundation supplies views; it does not infer the caller's data model.
Before choosing a spec or renderer, classify intrinsic data dimension and
sampling topology, enumerate compatible views, and select the views required
by the task. Rendering dimension does not determine data dimension: a heatmap
and a 3D surface can represent the same 2D scalar grid. Use the canonical
[Data Space and Visualization Views](https://github.com/Patr1ck2005/plot-workflows/blob/main/docs/data-space-and-visualization.md)
specification and its seven-field Agent decision record.

When a caller applies a scientific reduction before rendering, classify and
document the derived analysis space separately from the raw data space. This
package renders the resulting typed payload; it does not infer peak/ridge,
extrema, branch, or projection semantics. A caller may also render its raw
payload directly when no analysis transformation is required.

## Workflow

1. Characterize the required visual and artist contract in the caller.
2. Add a domain-neutral model and renderer behavior here.
3. Keep schema, output paths, and physical interpretation in caller adapters.
4. Record `runtime_info()` in acceptance provenance.
5. Update the public API document and run package tests.
6. Release a stable wheel; production callers do not use sibling path injection.
7. Keep the canonical data-space specification link in this Agent entry point.


<!-- project-hub:integration:start -->
## 项目总览接入约定

- 本项目的开发计划与验收证据继续保存在原有项目文档中，无需为总览维护额外进度摘要。总览直接读取本地 Git 提交；不再要求更新 `PROJECT_STATUS.md`，也不删除其他会话留下的状态原文。
- 若本项目已接入主要网页，入口以根目录 `PROJECT_WEB.json` 和 `WEB_ENTRY.md` 为准。修改网页入口、启动命令、依赖、端口或停止方式时，同步更新配置、统一启动脚本及入口说明，并验证启动、打开和停止。
- 使用 `start_web.bat`、`stop_web.bat`，需要加载后端或构建改动时使用 `start_web.bat restart`。开关由 Project Hub 统一管理；不要另起重复服务、按端口直接杀进程或自动换端口。
- Git 提交标题准确描述实际改动，不把提交活动视为完成度或验收证明。更新入口不构成提交授权；每次 commit 仍须向用户确认来源分类和具体模型，遵循既有 Origin 规则。
- 多会话修改前重新读取相关文件，只修改自己负责的内容；保留个人关注和备注。已有会话需重新读取本段，本约定不会自动同步会话或发送任务。
<!-- project-hub:integration:end -->
