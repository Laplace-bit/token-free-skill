# Integrate any target agent

The skill executor only needs to understand `SKILL.md` and have suitable local tools. It can be Claude Code, Codex, OpenCode, Gemini CLI, another skill-enabled agent, or an agent told to read this directory directly. Its identity does not determine which client the user wants connected to models. Skill discovery directories and invocation commands belong to that executor's current documentation; do not assume `$token-free-skill` or `~/.codex/skills` works everywhere.

## Select the connection route

1. Identify the user's target client, version, OS/host and existing provider configuration. If multiple targets are plausible, complete independent installation work first and ask which to configure. Do not switch every discovered agent.
2. If the installed Magpie detects that client in Agents, use its supported adapter and documented restart notice. Examples include Claude Code, Codex, OpenCode and Gemini CLI; use the current installed list rather than a frozen enumeration.
3. Otherwise inspect the client's official documentation for custom-provider support, API protocol, base URL semantics, model field and credential settings. A missing Magpie row does not prevent gateway use if the client supports compatible API configuration. Do not invent an adapter command or edit an undocumented schema.
4. If the client cannot configure a compatible endpoint, report that precise limitation. Installation of the two tools can still be complete; do not promise arbitrary closed clients work or automatically replace the user's client.

## Configure a compatible custom client

Find the running Magpie's actual loopback address and port from its UI/current settings. `GET /api/hello` identifies the Magpie gateway; do not treat any process listening on port 3425 as Magpie. Use the current [official integration guide](https://usemagpie.ai/docs/integrate) to verify endpoint and authentication rules.

| Client protocol | Typical base URL on the same machine | Request endpoint |
| --- | --- | --- |
| OpenAI Chat Completions | `http://127.0.0.1:<port>/v1` | `/v1/chat/completions` |
| OpenAI Responses over HTTP/SSE | `http://127.0.0.1:<port>/v1` | `/v1/responses` |
| Anthropic Messages | `http://127.0.0.1:<port>` | `/v1/messages` |
| Google Gemini | `http://127.0.0.1:<port>` | `/v1beta/models/{model}:generateContent` |

These are gateway routes, not a rule for every SDK's URL field. Check whether the target app appends `/v1` or expects a full endpoint before saving; avoid `/v1/v1`. Match its actual request protocol. The reviewed Magpie manual supports Responses through HTTP/SSE, not WebSocket upgrades; a client requiring another transport needs verified compatibility or a supported client setting.

List models from the running gateway's `/v1/models` catalog or Magpie UI and use the actual returned ID. Our Free Model usually appears with the `our-free-model/` provider prefix. Some clients add a separate configuration-provider prefix (for example, an OpenCode Magpie adapter may use `magpie/our-free-model/<id>`). Use the client adapter's generated value; do not send an extra client-only prefix to the gateway API or hard-code a model that was never discovered.

For ordinary same-machine loopback access, the official guide accepts a non-secret client label such as `magpie-<client-id>` as its API key and usage identifier. Check the installed gateway's current policy rather than applying that assumption to containers, remote hosts or proxies. Network clients require an enabled gateway key when sharing is configured. Treat real gateway keys as credentials. Do not use the plugin's temporary Cloudflare management URL as a model endpoint or enable public/LAN sharing as an incidental setup step. If gateway and client are on different hosts, agree on the deployment route first.

Use the client's documented UI, configuration file or per-client environment variables. `OPENAI_BASE_URL`, `ANTHROPIC_BASE_URL` and `GOOGLE_GEMINI_BASE_URL` are examples only: not every app honors them, and auth/model variables differ. Prefer a Magpie provider entry alongside the user's existing providers. Avoid global shell exports that redirect unrelated applications. Back up only changed files/settings, preserve other providers, and use the actual user/profile/config location for this client.

Apply the target's documented new-session/restart procedure. Observe model selection, then test only within the user's verification scope. Text success alone does not establish image, reasoning, streaming or tool-call support. Choose the single minimal authorized confirmed-free probe to cover the user's essential capability; do not add separate capability probes under the basic setup allowance. Report remaining capabilities as unverified unless the user asks for broader testing. Report the target name/version, protocol, host, discovered model ID and verified stage without secrets. Give a restore path to the previous provider.

## Primary references

- [Agent Skills specification](https://agentskills.io/specification)
- [Magpie integration guide](https://usemagpie.ai/docs/integrate)
- [Magpie agent adapters and gateway manual](https://github.com/yetone/magpie/blob/main/docs/reference.md)
