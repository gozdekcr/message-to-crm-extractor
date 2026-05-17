# message-to-crm-extractor

> An AI-assisted tool that transforms unstructured customer messages into structured CRM profiles — built as a mini case study for Iceberg Digital.

![Demo](assets/demo.gif)

---

## 🔍 Problem Statement

UK estate agents receive around **30 messages per day** across WhatsApp, email, and property portals. Roughly 30% of these contain new lead information that needs to be manually entered into a CRM system which around 9 messages per day.

At ~2 minutes per manual entry, this adds up to:
- **15–20 minutes of repetitive admin work every day**
- **Over 60 hours per year** spent on copy-pasting customer data

This manual process also results in incomplete or inconsistently structured profiles, increasing the risk of missed follow-ups and lost leads.

## 💡 Solution

Message-to-CRM Extractor automatically parses incoming customer messages and extracts structured lead data.Including budget, location, move date, bedroom count, and pet/furnishing preferences.

Key behaviours:
- **CRM relevance filter** — ignores non-actionable messages ("Thanks, Saturday works!")
- **Confidence flags** — distinguishes between exact, approximate, hard_limit, and flexible values
- **Missing field detection** — identifies what's unknown and suggests follow-up questions
- **Ambiguity preservation** — "around £1800" is stored as approximate, not forced into a hard number

> The goal is not to replace the agent — it's to eliminate the 90 seconds of manual data entry so they can focus on the actual conversation.

## 🔄 User Flow

1. Customer message arrives (WhatsApp, email, or portal)
2. System detects message and checks CRM relevance
3. LLM extracts structured fields from the message
4. Regex validation layer catches formatting errors and hallucinations
5. Confidence flags are assigned to each extracted value
6. Missing fields are identified and flagged
7. AI generates suggested follow-up questions for missing data
8. Agent reviews the extracted profile and approves or edits
9. System creates a new contact or updates an existing one
10. Interaction is logged to CRM history

![Flow Diagram](assets/flow.png)

## ⚙️ Technical Approach

This demo uses a **hybrid extraction model**:

### Rule-based layer (Regex)
Handles predictable patterns:
- Budget: `£1,800` / `1800ish` / `2k`
- Bedrooms: `2 bed` / `2 bedroom`
- Known London areas: matched against a curated list
- Month names: full and abbreviated forms

### LLM layer (planned)
In a production system, the regex layer would be paired with an LLM call for:
- Ambiguous or informal language
- Context-dependent extraction
- Multi-turn conversation handling

### Why hybrid?
- Regex is fast, deterministic, and free
- LLM handles edge cases regex can't
- Together they reduce hallucination risk

### Stack
- **Demo**: Vanilla HTML + CSS + JavaScript (no dependencies)
- **Production proposal**: Python backend, OpenAI/Claude API, CRM webhook integration

## 🏷️ Confidence Flag System

One of the core design decisions is preserving ambiguity rather than forcing false certainty.

| Flag | Meaning | Example |
|------|---------|---------|
| `exact` | Clearly stated | "2 bedrooms", "No pets" |
| `approximate` | Vague or estimated | "around £1800", "maybe October" |
| `hard_limit` | Explicit maximum | "max £2000", "up to £450,000" |
| `flexible` | Multiple options given | "Canary Wharf or Greenwich" |
| `unknown` | Not mentioned | No budget in message |

> Incorrect interpretation of ambiguous data (e.g. treating "around £1800" as a hard limit) can lead to missed property matches and poor recommendations.

## 📋 Extracted CRM Fields

| Field | Extracted From | Confidence Types |
|-------|---------------|-----------------|
| `budget` | £ amounts, "2k", "1800ish" | exact, approximate, hard_limit |
| `bedrooms` | "2 bed", "studio", "1 bedroom" | exact |
| `area` | Known London areas list | exact, flexible |
| `move_date` | Month names, "ASAP", "next month" | exact, approximate |
| `pet_friendly` | "dog", "cat", "no pets" | exact |
| `furnished` | "furnished", "unfurnished" | exact, approximate |

**Intentionally excluded:**
- Viewing availability — too variable for rule-based extraction, planned for LLM iteration
- Occupation, phone, number of tenants — require follow-up questions

## ⚠️ Risks & Limitations

### 1. Incorrect field extraction
Rule-based systems fail on unexpected phrasing. "A couple of bedrooms" won't be caught by the current regex.

**Mitigation:** Confidence flags + agent review before CRM save.

### 2. Ambiguity loss
AI may force certainty where none exists. "around £1800" must not become a hard limit.

**Mitigation:** Approximate flags preserve the original intent.

### 3. CRM data corruption
Duplicate contacts (two "John Smith" records) or wrong contact updates can corrupt lead data.

**Mitigation:** Match confidence scoring + confirm before merging + create new lead if unsure.

### 4. Incomplete extraction
"Relocating with my partner and small dog" — system catches pet info but misses occupant count.

**Mitigation:** Missing field detection + follow-up question generation.

### 5. Low agent trust / adoption
Even a technically accurate system fails if agents don't trust it.

**Mitigation:** Editable fields, confidence transparency, gradual rollout with feedback loop.

### 6. UK GDPR compliance
Messages contain personal data (budget, location, contact info).

**Mitigation:** Secure storage, audit logs, permission boundaries. *(Out of scope for this demo.)*

## 📊 Success Metrics

| Category | Metric | Target |
|----------|--------|--------|
| Efficiency | Manual entry time | 90s → 20s per message |
| Completeness | Auto-fill rate | 70%+ of CRM fields filled |
| Accuracy | Agent correction rate | <10% of extracted fields edited |

> A system that is fast but inaccurate is worse than no system at all — all three metrics must be tracked together.

## 🚀 What I'd Build Next

1. **LLM integration** — Replace regex with an LLM call for more accurate extraction of informal and ambiguous messages
2. **Multi-turn conversation support** — Track follow-up responses and update the CRM profile incrementally
3. **Duplicate detection** — Match incoming leads against existing CRM contacts by email, phone, or name similarity
4. **Lead scoring** — Rank leads by urgency, budget, and profile completeness to help agents prioritise
5. **CRM webhook integration** — Push extracted data directly to HubSpot, Salesforce, or a custom CRM via API
6. **Channel support** — Extend beyond email/portal to WhatsApp Business API and SMS

> This demo covers the core extraction and confidence logic. Production would layer LLM, deduplication, and CRM integration on top.
