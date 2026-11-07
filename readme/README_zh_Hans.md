# Ace Data Cloud：LlamaIndex 原生 LLM 类

[English](../README.md) · [当前模型与价格](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=ace_llm_llamaindex_pricing_zh)

包名 `llama-index-llms-acedatacloud`，导入 `llama_index.llms.acedatacloud.AceDataCloud`。
独立维护方为 Ace Data Cloud；地址已预设，用户不必手填 OpenAI base URL。
**PyPI 0.1.0 已发布**：[正式页面](https://pypi.org/project/llama-index-llms-acedatacloud/0.1.0/)。
2026-10-20 已用全新 Linux 环境从官方 PyPI 普通包名安装并验原生类元数据和依赖检查；
2026-11-07 再核版本与双工件哈希一致，无模型请求。官方收录、默认内置和模型真实质量仍未证明。

## 1. 安装

Python 3.10+，普通包名安装；[GitHub v0.1.0](https://github.com/AceDataCloud/AceDataCloudModelProviderLlamaIndex/releases/tag/v0.1.0) 提供同字节 wheel/sdist 备用：

```bash
python -m pip install "llama-index-llms-acedatacloud==0.1.0"
```

## 2. 注册、General application 和专用 Key

[注册/登录](https://platform.acedata.cloud?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=ace_llm_llamaindex_register_zh)后进入[Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=ace_llm_llamaindex_api_key_zh)。
找到 **General application**，没有时点 **Initialize General Application**。
核当前模型权限、价格及余额，复制 API Key 或 **Manage Keys → Create** 创建 `LlamaIndex LLM` 专用 Key。

![真实 Ace 控制台：复制或管理已遮挡的 Key](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

按需设置有效期、用量限制与 Allowed APIs；限制接口时允许 `/openai/chat/completions`。
创建后回列表复制。只复制原始 Token，不加 Bearer/空格/引号，不用 `platform-...` 管理令牌。

![真实 Ace 控制台：创建独立 Key](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

图片来自固定 SunoDify 提交、2026-10-18 获取，凭据已遮挡；旧示例名 `Dify tutorial` 请改成 `LlamaIndex LLM`。
它们只展示通用账户步骤，不证明本包已真实调用。不要将 Key 放入 prompt、日志或截图。

## 3. 在代码中选择 Ace

配置环境变量 `ACEDATACLOUD_API_TOKEN`，然后选择当前账户支持的模型和对应上下文 Token 上限：

```python
from llama_index.core import Settings
from llama_index.llms.acedatacloud import AceDataCloud

llm = AceDataCloud(model="YOUR_AVAILABLE_CHAT_MODEL", context_window=YOUR_MODEL_CONTEXT_TOKEN_LIMIT, max_tokens=256)
Settings.llm = llm
```

替换占位符后再用。构造不发 API；没有默认/兜底模型。
LlamaIndex 是代码框架，原生类在代码中选择，不承诺服务商下拉框或聊天 GUI。

## 4. 首次聊天与流式输出

获得费用授权并核价格后，`llm.chat([ChatMessage(role="user", content="Hello")])` 发一次收费请求。
英文 README 提供完整代码。流式与异步接口继承官方 OpenAILike，聊天返回文本，不产生媒体 task ID。
Suno 等媒体任务应使用独立服务工具，同 ID 查询，不由本 LLM 假装处理。

工具调用默认关闭；仅当前模型确实支持时传 `is_function_calling_model=True`，再接 FunctionAgent。
不能把一个模型验证当成所有模型均支持工具。401/403/429/500 保留协议错误类别；禁自动重试。
模型序列化不含 Key，不能覆盖固定的 Ace endpoint/鉴权字段。

## 5. 免费离线检查

```bash
pip install -e ".[dev]"
python examples/offline.py
pytest
python -m build
```

模拟 HTTP 和假 Token 验证真实原生类、聊天和流式协议；不证明真实质量、消费或营收。
现有发布身份已完成本 Provider 的 PyPI 0.1.0 发布，不需要为安装该版本新注册或重配 Token。
五个媒体工具包的 registry 状态单独验收，不由本 Provider 发包推定完成。
已发行 wheel/sdist 与 PyPI 长描述保留原始快照，不覆盖文件；当前仓库 README 修正历史“未发布”字样。
若安装失败，先核 Python3.10+ 和官方 PyPI/CDN 网络；没有新项目配额阻挡本已存在版本下载的证据。
后续版本按正常源码/发行流程，官方收录单独验收，不自动接受新协议。
