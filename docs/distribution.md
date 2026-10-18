# Independent LLM distribution

Package `llama-index-llms-acedatacloud`; class `llama_index.llms.acedatacloud.AceDataCloud`.
Maintainer: Ace Data Cloud. Standard LlamaIndex namespace, explicit model/context,
preset Ace endpoint, dedicated application token, no fallback, no default model.

Official reference: existing OpenRouter wraps OpenAILike in its own integration package.
https://github.com/run-llama/llama_index/tree/main/llama-index-integrations/llms/llama-index-llms-openrouter
Policy: https://github.com/run-llama/llama_index/blob/main/CONTRIBUTING.md
New packages are independently maintained and published to PyPI, not added to monorepo.

Release gate: human source review/merge authorization; existing authorized PyPI owner
configures pending/new Trusted Publisher for `llama-index-llms-acedatacloud`, owner
AceDataCloud, repo AceDataCloudModelProviderLlamaIndex, workflow publish.yml, environment pypi.
Then approve/tag a real release, verify the public wheel and a clean install.
No secrets, identities, terms acceptance or production settings are created here.

Official docs discovery proposal: add an externally maintained Ace Data Cloud entry to
Available LLM integrations, linking actual source/release status. Keep it a draft until
publication gates are met; no default inclusion or endorsement is claimed.

Real GUI/token screenshot collection belongs to the coordinating UI owner. The account
setup screenshots in README are existing redacted real images, not a new LlamaIndex GUI.
