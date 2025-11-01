# AICP-Demo

This repository contains the Walmart-branded agentic commerce demo used throughout the
previous simulations. It includes both Python and TypeScript templates so you can plug
them into LangGraph/SWARM-style orchestrators.

## Running the demo

```bash
python main.py
```

The command prints the combo-offer analysis, inventory forecast, support ticket
summaries, and the multi-agent commerce strategy packet.

## Customising labels (e.g. SRM-SecOps Command Center)

Some downstream teams prefer alternate terminology for the console sections. To update a
heading such as **"SRM-SecOps Command Center"**, edit the following files directly:

- `main.py` – CLI section headers in `AgenticCommerceDemo._rule` calls.
- `templates/typescript/agenticCommerceDemo.ts` – exported demo template for Codex
  integrations.

If you are unsure where a label lives, run the helper script below to search the repo
without requiring additional tools like `rg`:

```bash
python tools/find_string.py "AI-SecOps Command Center"
```

Replace the quoted text with any other label you want to locate. The script prints the
file path and line number for each match so you can make the change locally.

## TypeScript template

To experiment with the TypeScript version, install dependencies for your local runtime
and execute the exported `runDemo` function in `templates/typescript/agenticCommerceDemo.ts`.

```bash
node templates/typescript/agenticCommerceDemo.ts
```

(Use `ts-node` or compile with `tsc` if you are working in a TypeScript project.)
