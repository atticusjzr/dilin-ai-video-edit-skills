---
name: memory-flash-edit
description: 回忆快闪剪辑技巧：一组照片每张 1 秒、开头放大 1.08 缓出缩回、柔光、接缝闪白叠化、首尾渐显渐隐，在堤麟AI网页剪辑里用工程档一次排好（或拆成 13 步逐步写回）。附示范工程与素材（15 张情侣插画＋钢琴配乐），能直接在用户的剪辑页放好示范再改成用户自己的。另含「每张 0.2 秒＋晃动」的快节奏变体。用户要做回忆快闪、照片快闪、情侣/毕业/旅行回忆短片时用。没接堤麟 MCP 时先教用户接（第 0 节）。
---

# 回忆快闪（堤麟网页剪辑）

效果：N 张照片首尾相接，每张 1 秒；每张从 1.08 倍缓出缩回 1 倍，带柔光；接缝闪白叠化；第一张渐显、最后一张渐隐；底下铺一条配乐。15 张＝15 秒。

整套流程：**接上堤麟 MCP → 开一个剪辑页、把网址给用户 → 放好示范工程 → 问用户要换成自己的素材，还是照这个效果剪别的。**

## 0. 接上堤麟 MCP

本技能靠堤麟AI的 MCP 工具读写网页剪辑：`create_video_edit`、`get_video_edit`、`update_video_edit`、`list_drive`；传素材用 `import_file`（只有本机版有，读本机路径）或 `import_url`（远端版有，收公开网址）。
**先看自己的工具里有没有 `create_video_edit`。** 有就跳到第 1 节；没有就教用户接，接好再继续。

教之前先判断你自己跑在哪个软件里、用户是什么系统，**只讲那一家的步骤**，别把整张表丢给用户。步骤每一步都写清楚点哪里、贴什么；各家设定画面会改版，以用户看到的为准，对不上就请用户截图给你看。

MCP 网址：`https://dilinai.com/api/mcp`（大陆版帐号用 `https://dilinai.cn/api/mcp`）。走 OAuth：贴上网址后会跳到堤麟登入页，用户登入、选一只「外部角色」（或当场新建）、**权限要有「堤麟剪辑」和云端硬碟的写入**（新建角色默认勾好；选现有角色就照它现在的权限，缺了要去角色权限里补勾）、按同意就接好，不用领钥匙。本夹 `mcp.json` 是同一份设定。

| 你跑在 | 教用户这样接 |
|---|---|
| Claude Code | 终端跑 `claude mcp add --transport http dilinai https://dilinai.com/api/mcp`，再在 Claude Code 里打 `/mcp`，选 dilinai → 登入授权 |
| Codex CLI | `codex mcp add dilinai --url https://dilinai.com/api/mcp`，照提示在浏览器登入 |
| Claude 网页版／桌面版 | 设定 → 连接器 → 新增自订连接器，名称填「堤麟」，网址贴上，按连接后登入 |
| ChatGPT | 设定 → 连接器（Apps）→ 进阶里打开开发者模式 → 新增连接器，贴网址，验证方式选 OAuth |
| Cursor | Settings → MCP → Add new MCP server，类型选 HTTP（或在 `~/.cursor/mcp.json` 照本夹 `mcp.json` 加一段），再点 Login |
| VS Code（Copilot） | 命令面板跑「MCP: Add Server」→ HTTP → 贴网址 → 名称 dilinai，开始时按登入 |
| 其他支持 MCP 的软件 | 找「MCP 服务器／连接器」设定，新增一个远端（HTTP／Streamable HTTP）服务器，贴网址 |

- 接好后，通常要**重开对话**或重载工具，新工具才会出现；出现了再继续。
- 软件不支持 OAuth：请用户在堤麟网站「API 金钥」页建一把勾了「堤麟剪辑」和云盘写入的钥匙，用 `Authorization: Bearer <钥匙>` 请求头连同一个网址。⛔ 钥匙别写进任何档案、别贴在对话里给别人看。
- 终端型 AI（Claude Code、Codex）想要能直接传本机档（`import_file`）：改装本机版，`curl -fsSL https://dilinai.com/mcp.sh | bash`，再跑 `dilinai login` 在浏览器授权；装好会自动加名为 dilinai 的 MCP。
- 前提：用户要有堤麟AI帐号，且帐号已开放「剪辑」（云端硬碟按「新增」能看到剪辑）。没开放就照实说，别硬试。
- 官方说明：https://dilinai.com/docs/mcp 、https://dilinai.com/docs/video-edit

## 1. 开剪辑页，把网址给用户

1. 用户指定了放哪个资料夹：`list_drive {"type":"folder","name_contains":"<名字>"}` 找到它的 id。**没指定就放云盘根目录**（不带 `folder_id`）。
2. `create_video_edit {"name":"回忆快闪-示范"}`（有指定资料夹再加 `"folder_id"`）。回包里：
   - `id`＝剪辑工程档，后面读写都用它；
   - `folder_id`＝网站替这个工程新开的同名资料夹，素材传进这里；
   - `url`＝剪辑页网址。
3. 马上把 `url` 给用户，请他用电脑上的 Chrome 或 Edge 打开（剪辑页要电脑浏览器）。写进工程后，开着的剪辑页约 2 秒内会自己更新。

## 2. 放好示范工程

示范素材是 15 张竖版插画（1080×1920）和一段 15 秒钢琴配乐，放在公开网址上（台湾、大陆都能下载），清单是本夹 `demo/demo_urls.json`：每条 `{"name":"<模板里的档名>","url":"https://term.dilinai.com/skills/dilin-ai-video-edit-skills/demo/…"}`。`demo/demo_project.template.json` 是排好的工程，素材编号写成 `{{档名}}` 占位。从 GitHub 装的版本不带图档本身，只有这份网址清单。

1. 把 16 个档传进上一步的 `folder_id`，三条路按顺序挑第一条走得通的：
   - **有 `import_url`（远端连接器 `https://dilinai.com/api/mcp` 就有，首选）**：照 `demo_urls.json` 逐条把 `url` 导入 `folder_id`（参数名照工具自己的说明填），记下每条回的档案 id，用这条的 `name` 对回模板占位。云盘里的档名会是网址上的英文名（couple01.jpg…），不影响。⛔ 别把本机路径或沙盒路径交给远端，它读不到。
   - 有 `import_file`（只有本机版有，读本机路径）：先把 `demo_urls.json` 里的 16 个档下载到一个临时夹（例如 `curl -fsSL -o <临时夹>/<name> <url>`，档名用 `name`），再逐个 `import_file {"path":"<临时夹>/<name>","folder_id":"<folder_id>"}`，记下每个档回的档案 id；传完删掉临时夹。
   - 两样都用不了：把 `demo_urls.json` 里的网址给用户下载，请他打开堤麟「云端硬碟」，进到跟剪辑同名的那个资料夹，把档拖进页面上传。传完说一声，你用 `list_drive {"folder_id":"<folder_id>"}` 按档名对上 id。
2. 把模板里每个 `{{档名}}` 换成对应的档案 id（纯文字替换就行，档名一字不差）。
3. `get_video_edit {"id":"<id>"}` 拿 `updated_at` → `update_video_edit` 把换好的整份当 `project` 写回，带 `base_updated_at`。回包 `drops` 必须是空的；不空就照提示改了再写。
4. 请用户在剪辑页按播放看一遍。

## 3. 问用户接下来要怎么做

示范放好后**一定要问**，别自己往下做：
- **换成自己的照片**：请用户把照片传进那个资料夹（或告诉你在哪个资料夹），问播放顺序、要不要配乐（用他的音乐，或沿用示范钢琴）。`list_drive` 拿 id → 写 `photos.json` → 第 4 节产生工程 → 照第 2 节第 3 步写回。可以覆盖这份，或另开一份。
- **照这个效果剪别的**：问清楚题材、照片张数、每张停多久、横屏还是竖屏，再调第 4 节的参数。
- **只想改参数**（更快、缩放更大、不要柔光……）：改对应栏位重写。

完成后告诉用户：导出要他自己在剪辑页右上按「匯出」（MCP 不能导出）。

## 4. 参数与工程档

这组跟剪映原教程成片逐帧比对，PSNR 平均 32.3 dB。

| 项 | 工程档写法 | 说明 |
|---|---|---|
| 每张时长 | `length:1`，首尾相接 | |
| 缩放关键帧 | `kf.sx/sy: [{t:0,v:1.08,e:"out"},{t:0.9667,v:1}]` | 结尾帧放在倒数一帧（30fps），放在 1.0 接缝会顿一下 |
| 柔光 | `fx:[{fx:"fx-soft_bloom",strength:1}]` | `fx-glow` 0.3 比对差，`fx-soft_bloom` 拉满最像 |
| 接缝转场 | 第 2 张起每张 `transIn:{tr:"tr-flash_dissolve",length:0.4667}` | 闪白叠化最像；漏光叠化 `tr-leak_dissolve` 只有 21.6 dB |
| 渐显/渐隐 | 第一张 `anim.in {id:"in-fade",dur:0.27}`；最后一张 `anim.out {id:"out-fade",dur:0.33}` | |
| 比例 | `ratio:{kind:"fit"}` 跟素材；要固定就 `{kind:"preset",key:"9:16"}` | |
| 配乐 | 另开 audio 轨 `bgm`，从 0 起铺满全片，`fadeOut:1` | audio 轨排在 main 下面 |

产生工程档：
`python3 build_flash.py photos.json out.json [--music <配乐档 id> --music-name 名字.mp3] [--ratio 9:16]`
`photos.json`：`[{"name":"01.jpg","driveId":"<档案 id>"},…]`，照播放顺序（格式见 `example_photos.json`）。其余参数：`--each --zoom --fx --fxs --tr --trlen --fin --fout`。
跑不了 Python 时，照上表直接写 JSON，结构跟 `demo/demo_project.template.json` 一样。

有原片时可逐帧比对：`ffmpeg -i ex.mp4 -i ref.mp4 -lavfi "[0]scale=1080:1920,fps=30[a];[1]scale=1080:1920,fps=30[b];[a][b]psnr=stats_file=psnr.log" -f null -`，平均 30 dB 以上算对。

## 5. 拆成 13 步逐步写回（教学或录屏用）

`python3 build_flash.py photos.json out.json --steps steps/` 另出 p01–p13，一步写回一份：
p01 空工程 → p02 第一张上主轨 3 秒 → p03 结尾打缩放关键帧 1 → p04 开头关键帧 1.3 → p05 时长改 1 秒、结尾帧移到 0.97 → p06 开头改 1.08 → p07 缓出 → p08 加柔光 → p09 强度拉满 → p10 复制 N 份首尾相接 → p11 换成其余照片 → p12 接缝挂闪白叠化 → p13 首尾渐显渐隐（p13 就是最终工程）。
每写一份，等剪辑页上「正在编辑」的遮罩消失再写下一份。

## 6. 变体：快节奏快闪（每张 0.2 秒）

`python3 build_flash.py photos.json fast.json --fast [--music …]`：第一张 1.5 秒（1.25→1 缓出），其余每张 0.2 秒（1.35→1 缓出＋`fx-shake` 0.5）。适合 30 张左右，同一场景的两张别连着放。
要拖影：运动模糊 `look.mblur {amount:30,blend:30,passes:4}` 只对影片生效，图片要先在剪辑页全选这些片段、右键合并成一段影片，再在那段上开。
