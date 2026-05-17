# message-to-crm-extractor

> An AI-assisted tool that converts customer property messages into structured CRM fields. Built as a mini case study for Iceberg Digital.

![Demo](assets/demo.gif)

---

## Problem Statement

UK estate agents receive customer inquiries from multiple channels such as WhatsApp, email, and property portals.

Many of these messages contain CRM-relevant information including:
- budget
- preferred location
- move-in date
- bedroom requirements
- pet or furnishing preferences

Assumptions:
- ~30 incoming customer messages per day
- ~30% contain CRM-relevant lead information
- ~2 minutes manual CRM entry per relevant message

This results in:
- 15–20 minutes of repetitive admin work daily
- 60+ hours annually spent on manual CRM data entry

Manual entry also increases the risk of:
- incomplete customer profiles
- inconsistent data formatting
- missed follow-ups

## Solution

This tool extracts structured CRM data from raw customer messages: budget, location, move date, bedrooms, and pet/furnishing preferences.

- **CRM relevance filter** : ignores non-actionable messages like "Thanks, Saturday works!"
- **Confidence flags** : distinguishes exact, approximate, hard_limit, and flexible values
- **Missing field detection** : identifies missing customer information
- **Ambiguity preservation** : "around £1800" stays approximate, not forced into a hard number

> The goal is not to replace the agent. It's to eliminate the 2 minutes of manual data entry so they can focus on the actual conversation.

## User Flow

1. Customer message arrives
2. System checks CRM relevance
3. Extracts structured fields
4. Flags ambiguity / missing fields
5. Agent reviews output
6. CRM is updated

## Technical Approach

**Tech Stack**
- HTML, CSS, JavaScript
- No backend or external dependencies

**Extraction Logic**
- Regex patterns for budget, bedrooms, and dates
- Rule-based matching for London areas and keywords
- Confidence flags to handle ambiguous language

**Python Version**
A standalone Python implementation is also included in `demo/extractor.py` , using the same extraction logic for backend integration experiments.

## Confidence Flag System

Each extracted field gets a confidence flag to preserve ambiguity rather than forcing false certainty.

| Flag | Meaning | Example |
|------|---------|---------|
| `exact` | Clearly stated | "2 bedrooms", "No pets" |
| `approximate` | Vague or estimated | "around £1800", "maybe October" |
| `hard_limit` | Explicit maximum | "max £2000", "up to £450,000" |
| `flexible` | Multiple options given | "Canary Wharf or Greenwich" |
| `unknown` | Not mentioned | No budget in message |

## Risks & Limitations

- **Incorrect extraction** : unexpected phrasing may be missed. Mitigated by agent review before CRM save.
- **Ambiguity loss** : "around £1800" must not become a hard limit. Mitigated by confidence flags.
- **Incomplete extraction** : some details require follow-up. Mitigated by missing field detection.
- **Low agent trust** : system fails if agents don't use it. Mitigated by editable fields and transparency.

## Success Metrics

- **Efficiency** : reduce manual CRM entry time from ~2 minutes to under 30 seconds per message
- **Completeness** : 70%+ of CRM fields auto-filled from the original message
- **Accuracy** : less than 10% of extracted fields require manual correction by the agent

## What I'd Build Next

1. **LLM integration** : more accurate extraction for informal and ambiguous messages
2. **Multi-turn support** : track follow-up responses and update CRM profile incrementally
3. **Lead scoring** : rank leads by urgency and profile completeness
4. **Channel support** : extend to WhatsApp Business API and SMS
