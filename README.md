# dilin-ai-video-edit-skills

堤麟AI的剪辑技巧技能集。每个插件是一个单独的剪辑技巧：AI 读了就能在[堤麟AI网页剪辑](https://dilinai.com/docs/video-edit)里把效果直接排好。

| 技巧 | 做什么 | 技能直达 |
|---|---|---|
| memory-flash-edit | 回忆快闪：照片每张 1 秒、1.08 缓出缩回、柔光、闪白叠化、首尾渐显渐隐；附示范工程 | [SKILL.md](memory-flash-edit/skills/memory-flash-edit/SKILL.md) |

## Claude Code：当插件装（会自动接上堤麟 MCP）

```
/plugin install memory-flash-edit --marketplace atticusjzr/dilin-ai-video-edit-skills
```

旧版 Claude Code 分两步：

```
/plugin marketplace add atticusjzr/dilin-ai-video-edit-skills
/plugin install memory-flash-edit@dilin-ai-video-edit-skills
```

装好后第一次用会跳出堤麟登入页：登入、选一只外部角色、权限要有「堤麟剪辑」和云端硬碟写入，按同意即可。更新：`/plugin marketplace update`。

## 其他 AI（Codex、Cursor、Claude 网页版、ChatGPT…）

把技能直达那一层资料夹交给它（放进它自己的技能夹，或直接让它读 SKILL.md）。技能第 0 节会教它按你用的软件接上堤麟 MCP（`https://dilinai.com/api/mcp`，OAuth 登入，不用钥匙）。

## 前提

堤麟AI帐号，且帐号已开放「剪辑」。

## 回报与讨论

- 使用问题、作品分享、想要的新技巧：[Discussions](https://github.com/atticusjzr/dilin-ai-video-edit-skills/discussions)
- 技能本身的错误、堤麟网站／剪辑页的问题：[Issues](https://github.com/atticusjzr/dilin-ai-video-edit-skills/issues)（选对应模板）

## 授权

- 技能说明、脚本、工程模板：[Apache-2.0](LICENSE)。不授权使用「堤麟／Dilin AI」名称作为商标。
- 示范图与配乐（放在 `term.dilinai.com/skills/dilin-ai-video-edit-skills/demo/`）：[CC BY 4.0](LICENSE-ASSETS.txt)，使用时请注明「示范素材来自 堤麟AI（dilinai.com）」。
- 示范图为 AI 生成；示范配乐用 FluidR3_GM 音色库（MIT）合成。详见 [NOTICE](NOTICE)。
