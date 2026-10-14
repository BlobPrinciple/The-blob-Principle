🇬🇧 English · 🇫🇷 [Version française](../IA_CONTRIBUER.md)

# Contributing to the Blob with an AI

The Blob Principle was built with several AIs used as critical sparring partners, never as oracles. The laboratory therefore welcomes contributions made with an AI (ChatGPT, Claude, Gemini, Mistral, Llama, DeepSeek or any other), on one condition: **a human checks and signs what is submitted.**

> **TOE demonstrated: NO** · physical gates 0/7 · 27 open research problems. An AI that "confirms" the Blob proves nothing; an AI that helps find a verifiable error, proof or refutation moves the programme forward.

## In three steps

1. **Pick a challenge** in [CHALLENGES.md](CHALLENGES.md) or in its machine-readable version, [docs/defis.json](https://blobprinciple.github.io/The-blob-Principle/defis.json).
2. **Give your AI the prompt below**, with the chosen challenge.
3. **Check the result yourself**, then submit it with the "AI-assisted contribution" issue template.

## Prompt to paste into your AI

```text
You are taking part in the public laboratory of the Blob Principle (author: Rudolphe
Mirante, DOI 10.5281/zenodo.23188586). Declared status: theory of everything
demonstrated NO, physical gates 0/7, level 1 (reproducible mathematical model).

Authoritative sources:
- Armature V347.1 (English): https://github.com/BlobPrinciple/The-blob-Principle/blob/main/corpus/00_master_courant/EN/armature_V347-1_EN.md
- Programme status: https://github.com/BlobPrinciple/The-blob-Principle/blob/main/en/PROGRAMME_STATUS.md
- Challenges: https://blobprinciple.github.io/The-blob-Principle/defis.json

Challenge addressed: DEFI-__ (copy its statement).

Rules:
1. Work only from the sources above; cite the section or line for every claim about
   the corpus. If you cannot find it, say so.
2. Label every statement: [T] proved, [M] measured, [H] hypothesis, [OPEN] open.
3. Provide everything a third party needs to check: full derivations, runnable code,
   command, expected output.
4. A clean refutation counts as much as a proof. Do not try to confirm the Blob:
   look for what is true.
5. End with: what is established, what remains to be checked, and the weakest point
   of your own answer.
```

## What a contribution must contain

- the **model** used (name and version) and the **prompt** given;
- the **name of the person** who checked the result;
- the **verifiable elements**: files actually present, values traceable in the corpus (file and line), a command that reproduces the result;
- the **weakest point** of the contribution.

Batch-generated submissions lacking these elements are closed without review on the merits (see [CONTRIBUTING.md](CONTRIBUTING.md#5-what-will-not-be-accepted)).

## What happens next

Each contribution is reviewed, re-run when it contains computation, then classified: **accepted** (listed on the honour roll or the Wall of Refuters, under the name of the person who signed it), **to be completed**, or **not accepted**, with the reason. Only the author of the programme decides what enters the corpus and any change of status ([GOVERNANCE.md](GOVERNANCE.md)). A contribution transfers no rights over the Blob Principle ([AUTHORSHIP.md](AUTHORSHIP.md), [CLA.md](CLA.md)).
