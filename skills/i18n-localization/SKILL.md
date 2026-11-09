---
name: i18n-localization
description: >-
  Builds software for more than one language and locale: string extraction and catalogs, ICU
  pluralization, date/number/currency formatting, right-to-left layout, locale negotiation, URL
  and hreflang strategy, and the translation workflow. Use when shipping to a second market,
  adding a language picker, fixing mojibake or broken plurals, handling RTL, or setting up
  translated routes. Single-locale copies, translation itself, and general frontend layout route
  to frontend-web-engineer.
metadata:
  version: 1.0.0
  domain: delivery
  grade: G2
  status: active
  last-reviewed: '2026-11-08'
  authored-by: ui-ux-architect
---

# Internationalization and Localization

i18n is the code change that makes a second locale possible. l10n is the content work of adding
one. Do them in that order, once, or pay for both repeatedly.

## WHEN TO USE

- Adding a second language, region, or currency to a product that assumed one.
- A user reports broken plurals, wrong date order, mistranslated strings, or text overflowing a button.
- Setting up RTL (Arabic, Hebrew, Farsi, Urdu) or a locale picker.
- Choosing between `/de/`, `de.example.com`, and `?lang=de` for translated routes.
- A translation pipeline exists but strings keep leaking into code.

## WHEN NOT TO USE

- One locale, and the product has no stated plan for a second. Speculative i18n adds a lookup
  layer to every string for no user.
- The task is translating copy, not building the mechanism. That is a translator, not a skill.
- The problem is only date formatting in one locale. Use `Intl` directly.

## DECISION TREE

```text
What is the locale problem?
├─ strings live in components ...................... extract to catalogs, key by meaning
│  └─ keys are English sentences .................. use stable IDs; changing copy must not break keys
├─ plurals wrong ................................... ICU MessageFormat, one message per plural category
│  └─ language has 3+ plural forms (pl, ru, ar) ... never `count === 1 ? a : b`
├─ dates/numbers/currency wrong .................... Intl.DateTimeFormat / NumberFormat, locale + timeZone explicit
│  └─ currency stored as float .................... integer minor units + currency code
├─ layout breaks in German/Russian ................. 30-40% expansion budget, no fixed-width buttons
├─ RTL looks mirrored and broken ................... logical CSS properties, dir attribute, mirrored icons only
├─ locale not detected ............................. negotiate: URL > user setting > Accept-Language > default
├─ translated routes / SEO ......................... sub-path per locale + hreflang + self-referencing canonical
└─ translations drift from source .................. extraction in CI, missing-key build failure
```

### Choices that are expensive to reverse

| Choice | Default | When to deviate |
|---|---|---|
| URL strategy | sub-path `/de/...` | sub-domain when regions are operated separately |
| Message format | ICU MessageFormat (JSON) | Fluent if you need gender/select-at-scale |
| Keys | stable IDs (`cart.empty.title`) | source-text keys only if the source language never changes |
| Fallback | default locale, never raw key | never render a key to a user |
| Plural source | CLDR categories for the target locale | never assumed from English |

## FAILURE MODES & MITIGATIONS

| Failure | Mechanism | Mitigation |
|---|---|---|
| String concatenation | `"Hello " + name + "!"` cannot be reordered by a translator | One message with placeholders |
| English plural logic | Two forms hardcoded; Polish needs four | ICU `plural` with CLDR categories |
| Locale from IP | VPN and travel produce the wrong language | Explicit setting, then `Accept-Language`, then default |
| Text expansion overflow | German and Russian run 30% longer; buttons clip | Pseudo-locale with `[!! ... !!]` padding in tests |
| RTL as `transform: scaleX(-1)` | Mirrors text and numerals, breaks icons | `dir="rtl"` + logical properties (`margin-inline-start`) |
| Currency as double | Rounding drift, wrong symbol placement | Integer minor units; `Intl.NumberFormat` with `style: 'currency'` |
| Untranslated keys shipping | Missing key renders the ID or English | CI fails on missing keys; fallback logged, not silent |
| Mojibake | Bytes decoded as the wrong charset | UTF-8 end to end, `Content-Type` charset, DB collation checked |
| Wrong day boundary | Server formats in UTC, user sees yesterday | Store UTC, render in the user's IANA zone |

## QUANTITATIVE RULES

- **Budget 30% string growth** (40% for German and Russian) in every fixed-width surface.
- **Minimum three plural categories** tested: `one`, `other`, and one of `few`/`many`/`two`.
- **Two locales minimum** in any i18n test suite, and one must be RTL.
- **Zero hardcoded user-visible strings** in components, enforced by lint, not review.
- **All date output carries an explicit `timeZone`.** Default only if the product is genuinely single-zone.

## VERIFICATION GATE

- [ ] Pseudo-locale build renders with padded strings and no clipped text.
- [ ] One RTL locale renders correctly in a screenshot, with icons and numerals not mirrored.
- [ ] A plural test covers every CLDR category for the target locale.
- [ ] Switching locale changes formatting of a date, a number, and a currency.
- [ ] Missing-key path is exercised and shows a fallback, never a raw key.
- [ ] Translated pages emit `hreflang` plus a self-referencing canonical.

## REFERENCES

- `frontend-web-engineer` for layout, routing, and SSR mechanics.
- `email-notifications` for localized templates and per-locale sending.
- `web-performance` for the cost of shipping one bundle per locale.
- `test-engineer` for pseudo-locale and plural test harnesses.
