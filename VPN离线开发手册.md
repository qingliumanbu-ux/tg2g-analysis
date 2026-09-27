# 太钢二炼钢 前台/IDK 离线开发手册（VPN 断网模式专用）

> 目的：连上 VPN（断网模式）后无法使用大模型和 npm 外网源，
> 所有需要外网的事必须在连 VPN **之前**做完；本手册覆盖连上 VPN 之后的全部操作。
> 生成日期：2026-09-21

---

## 一、环境现状（已核实）

| 项 | 状态 |
|---|---|
| Node.js | v24.19.0（要求 ≥16.13.2 ✔）npm 11.17.0 / yarn 1.22.22 / pnpm 11.24.0 均可用 |
| 前台工程 | 9 个子应用（xr-fbsm、xr-tksm、xr-mmlc、xr-mmsm-ag、xr-pssm、xr-qmbs-ag、xr-tmsmx、xr-wmgh、xr-wmsmx），全部同源于信融3.0 框架模板 xr-er-example |
| 技术栈 | Vite 5.4 + Vue 3.5 + TypeScript 5.5 + Module Federation（@originjs/vite-plugin-federation） |
| 平台网关 | `http://10.76.53.54:10003`（所有 .env.development 的 VITE_APP_BASE_API） |
| 账套/应用 | VITE_APPLICATION_NAME = 'TGZ1Z0'，VITE_APP_COMPANY_CODE = 'BS' |
| IDK 插件 | baosight.iplat4cforvscode-1.1.11（后台窗口登录问题已修复：Server/APBD/.env.development 已补建并本地 git-ignore） |
| 依赖安装 | ⚠️ 各前台工程 node_modules 均为空，**连 VPN 前必须先装** |

---

## 二、连 VPN 之前（需要外网，一次做完）

1. **安装依赖**（要跑哪个子应用就装哪个）：
   ```bash
   cd D:/work/company/太钢二炼钢/Client/xr-fbsm
   npm config get registry        # 确认是 https://registry.npmmirror.com/
   npm install                    # 或 yarn install；postinstall 会自动执行 patch-package
   ```
2. **让 AI 把要写的代码骨架/模板提前生成好**（断网后写不了就得手写）。
3. 把所有需要的文档下载到本地（本手册、《信融3.0安装配置指南.md》已在本地）。

---

## 三、连 VPN 之后（固定流程）

### 1. 确认内网通
```
浏览器或 curl 打开 http://10.76.53.54:10003   # 通了才能往下走
```

### 2. 重新取 token（⚠️ 8 小时有效，每天/每次超时都要重取）
- `.env.development` 里现有的 VITE_APP_SIGNATURE_TOKEN 内嵌日期均为过去时间（2025-08 ~ 2026-05），**全部已过期**。
- 取新 token：
  1. 浏览器打开信融项目**基座地址**并登录；
  2. F12 → 「应用/Application」面板 → 本地存储空间（或会话存储）；
  3. 复制 `signature_token` 的值 → 填入该工程 `.env.development` 的 `VITE_APP_SIGNATURE_TOKEN`；
  4. 顺手更新 `VITE_APP_REFRESH_TOKEN`；
  5. **重启 dev 服务**（改 env 不会热生效）。

### 3. IDK 登录
- 前台窗口：点左侧 IDK 图标 → 类型视图/模块视图 → 「登录」（记住密码存在 `~/Documents/iPlat4C_IDK_VSCode/login.json`，下次自动预填）。
- 后台窗口（Server.code-workspace）：APBD 已补 `.env.development` 可弹登录框；其他 Server 仓库若也要登录，把 `.env.development`（两行：VITE_APP_BASE_API、VITE_APPLICATION_NAME）复制到该仓库根目录即可——插件只认工作区**第一个文件夹**。

### 4. 启动调试（两种方式等价）
- **一键**：资源管理器右键任意 `.vue` 文件 → 「启动调试-BaoSight」→ 输入默认启动画面（默认=右键的文件名）→ 子画面可留空回车。
  插件会：找项目根 → 检测端口（5173 被占自动 +1）→ 终端执行 `npm run dev` → 等 30 秒端口就绪 → 自动打开浏览器。
- **手动**：终端进工程目录执行 `npm run dev`（dev 脚本固定 --port 5173），浏览器开：
  ```
  http://localhost:5173/画面名                 # 或 ?formName=子画面名
  ```
  ⚠️ 只能用 localhost 访问。
- 停止：在对应终端 `[5173] xr-xxx` 里 Ctrl+C。

### 5. 新建业务画面
`src/views/` 下建文件夹 `XXX00`，内含三件套：`XXX00.vue`（模板）、`XXX00.ts`（逻辑）、`XXX00.scss`（样式）。
参考现成例子：`src/views/DEMOAG`、`DEMOPX`。画面和按钮要在平台的 **EPESOBJ** 画面注册。

---

## 四、构建发布

1. 检查 `.env.production`（账套/子系统/应用名与运行环境一致）。
2. 编译打包：
   ```bash
   yarn build        # = vue-tsc --noEmit && vite build
   ```
   产物在 `dist/<子应用名>/`（如 dist/FBSM）。
3. 发布：发布服务器 `nginxhome/child/` 下建**与子应用名同名**的文件夹（VITE_APP_NAME，如 FBSM），把 dist 内容 FTP 上去；首次发布先在 **EPNG01** 画面注册子应用。

---

## 五、常见问题对照表

| 现象 | 原因 | 处理 |
|---|---|---|
| IDK 登录报 Network Error: unable to connect to server | VPN 没连/到 10.76.53.54 不通 | 先通内网再登录 |
| 调用服务报签名/token 失效 | VITE_APP_SIGNATURE_TOKEN 过 8 小时有效期 | 按上文重取 token 并重启 dev |
| 页面白屏、控制台 remote_exposes 404 | 公共组件(EFX/EIX/ERX/EBFR)从平台加载，内网不通或 baseApi 错 | 确认 VPN 与 .env.development |
| 后台窗口点 IDK 登录没反应 | 工作区第一个文件夹缺 .env.development | 复制两行 env 到该仓库根目录（参考 Server/APBD） |
| IDK 提示「请勿重复登录」 | 登录状态只存在当前窗口内存 | 重开窗口即恢复未登录 |
| 登录已失效，请重新登录 | 会话过期 | 重开窗口重新登录 IDK |
| 端口被占用 | 5173 已有 dev 在跑 | 插件自动换端口；手动用 `npm run dev -- --port 5174` |
| yarn build 类型报错 | vue-tsc 严格检查 | 按 TS 报错逐条修，或临时 `npx vite build` 跳过类型检查 |

---

## 六、断网期间用不了大模型怎么办

- 断网期间的疑问**记进一个 todo 文件**（如 `analysis/断网问题清单.md`），恢复网络后一次性问。
- 参考资料都在本地：本手册、`信融3.0安装配置指南.md`、`analysis/` 目录、各工程 README 与现成画面代码（最好的"范例库"就是 src/views 里既有画面）。
- 需要大段新代码（新画面、新组件）尽量在连 VPN 前让 AI 生成好骨架。
