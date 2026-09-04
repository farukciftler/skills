# On-device and hybrid AI on Apple platforms

The most-changed area of the stack. Verify specifics against `developer.apple.com/documentation/FoundationModels` and the WWDC26 sessions before writing production code.

## Contents
- [The four paths](#the-four-paths)
- [Foundation Models framework](#foundation-models-framework)
- [Core AI](#core-ai)
- [MLX](#mlx)
- [Core ML](#core-ml)
- [App Intents: the distribution layer](#app-intents-the-distribution-layer)
- [Designing an AI feature that survives](#designing-an-ai-feature-that-survives)
- [Evaluations](#evaluations)
- [Privacy positioning](#privacy-positioning)

---

## The four paths

| Path | For | Cost | Availability |
|---|---|---|---|
| **Foundation Models — on-device** | Summarisation, extraction, classification, structured generation, tool-calling, short conversational turns | Zero. No API key, no metering | Apple Intelligence devices (A17 Pro / M1 or later) |
| **Foundation Models — Private Cloud Compute** | The same API when the task exceeds on-device capability. 32K context, reasoning levels, no account setup or keys, private | Free for App Store Small Business Program members under 2M lifetime first-time downloads; otherwise metered | iOS 27+, now also watchOS 27 |
| **Foundation Models — third-party provider** | Frontier capability. Anthropic and Google publish Swift packages conforming to `LanguageModel` | Your API key, your bill. OAuth + Keychain for auth; per-token usage tracking including cache and reasoning tokens | Any device with network |
| **Core AI / MLX — your own model** | Custom or open-weight models, domain-specific fine-tunes, full control of weights | Your engineering time, app bundle size or download | Apple silicon |

The strategic shape: **Apple gave up competing on model quality and is competing on integration.** Foundation Models is a good-enough free tier for the simple 80%; escalate to a frontier model for the hard 20%. Design so that escalation is a configuration change, not a rewrite.

## Foundation Models framework

### The iOS 27 shape

A `LanguageModel` protocol backs `LanguageModelSession`. Everything conforms:

- Apple's on-device model (the one powering Apple Intelligence)
- `PrivateCloudComputeLanguageModel` — Apple's server model, 32K context, reasoning levels
- `CoreAILanguageModel` — open source, runs local models on Neural Engine and GPU
- `MLXLanguageModel` — open source, MLX-backed
- `ChatCompletionsLanguageModel` — any chat-completions endpoint, including a local MLX-LM Server
- Third-party packages (Anthropic's `ClaudeForFoundationModels`, Google's Gemini equivalent)

Swap providers through Swift Package Manager with everything downstream unchanged. This is the single most important architectural fact: **put the model behind the protocol and the choice becomes reversible.**

### Capabilities

- **Structured output** via `@Generable` / guided generation — constrain output to a Swift type instead of parsing JSON out of prose. Use this everywhere you can; it eliminates a whole class of failure.
- **Tool calling** — your Swift functions as tools. Built-in tools now include `BarcodeReaderTool` and `OCRTool` (Vision-backed) and a Spotlight-powered search tool that gives you **fully local RAG** without building an embedding pipeline.
- **Multimodal prompts** — images alongside text.
- **Dynamic Profiles** — swap model, tools, and instructions on the fly within a continuous session. This is the primitive behind multi-agent workflows and the "skills" abstraction Apple ships as a separate package.
- **Streaming** — partial responses for responsive UI.
- **`Response.usage`** — token accounting, new in iOS 27. Budgets are small on-device; this is how you see what you're spending.

### Beyond the app

- **`fm` CLI** on macOS 27 — `fm chat` interactively, or pipe into shell scripts to summarize/extract/generate.
- **Python SDK** — same on-device model, availability checks and structured responses in a few lines.
- **Utilities package** — transcript management, a skill API, chat-completions interfacing.
- **Open source** — the core framework runs wherever Swift runs, including Linux servers.

### Constraints to design around

The on-device model is small and its context window is tight. Assume:

- Long documents need chunking, or escalation to PCC.
- Quality is materially below frontier models on reasoning, code, and multilingual work — including Turkish, where the on-device model is noticeably weaker than on English.
- Latency is device-dependent — see `hardware.md`. What feels instant on an A19 Pro feels sluggish on an A17 Pro.
- Availability must be checked at runtime. Devices without Apple Intelligence, or with it disabled, need a graceful path.
- Guardrails can refuse. Handle refusal as a normal outcome, not an error state.

Verify current context window and rate limits in the documentation rather than assuming — this number changed between iOS 26 and 27.

## Core AI

New in iOS 27. Built into the OS, purpose-built for Apple silicon, for running **your own** models on-device:

- Modern memory-safe Swift API to load, specialize and run models
- Automatic specialization for the hardware it runs on
- Ahead-of-time compilation for quick load times
- Fine-grained control over inference memory
- Zero-copy data paths, stateful execution
- Scales from compact vision models to large-scale generative AI, across all Apple platforms

Use it when Foundation Models' model isn't the right model — a domain fine-tune, a specific open-weight model, a vision model you trained. `CoreAILanguageModel` bridges it into the Foundation Models session API, so you get the same downstream ergonomics.

## MLX

Apple's array framework for machine learning on Apple silicon. Where Core AI is the productionised path, MLX is the research/flexibility path — running open-weight models, experimenting with quantization, MLX-LM Server for a local chat-completions endpoint. `MLXLanguageModel` brings it into Foundation Models sessions.

On a Mac with enough unified memory this is how you run a genuinely capable local model. On iPhone the memory ceiling binds hard — see `hardware.md`.

## Core ML

Still the right tool for classic ML: image classification, object detection, sound classification, tabular models, anything you'd train with Create ML. Not deprecated. For generative and large models, Core AI is the newer path.

## App Intents: the distribution layer

Treat this as part of the AI story, not as a separate integrations chore.

**Why it matters now:** Siri is a primary entry point to the phone. Entity schemas contribute your content to the Spotlight semantic index so Siri can surface it with attribution back to your app. Intent schemas let people act on that content in natural language — no phrases to define, no code changes as Siri's language understanding expands to new languages and dialects. An app without intents is invisible to that surface.

**What it costs you:** your domain model needs real entities. `AppEntity` conformance wants stable identifiers, queryable collections, and display representations. If your model is a bag of view state, this is painful — which is the argument for the domain layer in `architecture.md`.

**New in iOS 27:** View Annotations API maps views to entities so people can reference and act on what's onscreen conversationally. App Intents Testing framework validates the whole integration through real system pathways.

## Designing an AI feature that survives

**1. Put the model behind a protocol.** Not because you might switch — because you *will*, and because it's the only way to test.

```swift
protocol Summarizer: Sendable {
    func summarize(_ text: String) async throws -> Summary
}
```

The Foundation Models implementation, a PCC implementation, a Claude implementation, and a canned test implementation all conform. The feature code never knows which it has.

**2. Use structured output, not prose parsing.** `@Generable` types make the model's output a compile-checked contract.

**3. Design the failure path first.** Model unavailable, guardrail refusal, timeout, empty result, nonsense result. Each needs UI. An AI feature with no failure design will look broken to a meaningful fraction of users.

**4. Never block the user on inference.** Stream, or do it in the background and surface the result. A spinner over an LLM call is the most common bad AI UX.

**5. Escalation ladder, decided per feature.** On-device by default → PCC when the input exceeds on-device capability → frontier model when the task genuinely needs it. Each rung costs money, latency, or privacy; make the choice deliberately rather than defaulting everything to the top rung.

**6. Budget tokens explicitly.** `Response.usage` exists so you can see the cost. Manage transcript history rather than letting it grow — the framework's utilities package has transcript management for this.

**7. Be honest in the App Store listing.** Age ratings now explicitly account for AI assistant and chatbot functionality's effect on sensitive content frequency. See `shipping.md`.

## Evaluations

The Evaluations framework (iOS 27) measures whether AI features behave correctly across dynamic conditions — beyond what unit tests catch. If a product's value is an LLM feature, this belongs in CI from the start. The WWDC26 sessions to pull: "Meet the Evaluations framework" (298), "Create robust evaluations for agentic apps" (299), "Improve your prompts by hill-climbing with Evaluations" (335).

The discipline it enforces: a prompt change is a code change with a regression risk. Without evals you find out from reviews.

## Privacy positioning

On-device inference is a genuine product differentiator and worth saying plainly in marketing: no data leaves the device, no account, no server. Private Cloud Compute preserves most of that claim — Apple's stated architecture keeps data private and unretained — but it is not the same claim as on-device, and conflating them in marketing copy is the kind of thing that ages badly.

If the app escalates to a third-party model, that is a network call to someone else's servers and the privacy policy and App Privacy labels must say so. Get this right at submission rather than in an update.
