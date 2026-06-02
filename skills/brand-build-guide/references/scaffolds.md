# Scaffolds — brand-neutral templates to fill

Copy these into the generated skill's `assets/` and `references/`, replacing every `{{TOKEN}}` with the value from `design-tokens.json`. They are the proven layouts; only the token values change per brand.

Token keys used below: `{{primary}}`, `{{accent}}`, `{{bg}}`, `{{card}}`, `{{soft}}`, `{{border}}`, `{{text_primary}}`, `{{text_secondary}}`, `{{zebra}}`, `{{link}}`, `{{font_stack}}`, `{{radius_card}}` (e.g. 12px), `{{accent_bar_height}}` (e.g. 6px), `{{logo_url}}`, `{{logo_report_size}}` (e.g. 140px), `{{logo_email_size}}` (e.g. 160px), `{{footer_company}}`, `{{footer_address}}`, `{{footer_phone}}`, `{{footer_website_href}}`, `{{footer_website_display}}`.

## 1. HTML report scaffold → `assets/report-scaffold.html` and the core of `references/html-reports.md`

```html
<!DOCTYPE html>
<html lang="{{lang}}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{brand_name}} — [Document Title]</title>
  <style>
    :root {
      --brand: {{primary}};
      --accent: {{accent}};
      --bg: {{bg}};
      --card: {{card}};
      --soft: {{soft}};
      --border: {{border}};
      --text: {{text_primary}};
      --muted: {{text_secondary}};
      --zebra: {{zebra}};
      --link: {{link}};
      --font: {{font_stack}};
    }
    * { box-sizing: border-box; }
    html, body { margin:0; padding:0; background:var(--bg); color:var(--text); font-family:var(--font); line-height:1.65; -webkit-font-smoothing:antialiased; }
    .page-bg { min-height:100vh; padding:24px 12px; }
    .container { max-width:900px; margin:0 auto; background:var(--card); border-radius:{{radius_card}}; box-shadow:0 6px 18px rgba(0,0,0,.08); overflow:hidden; }
    .top-accent { height:{{accent_bar_height}}; background:var(--accent); }
    .header { padding:22px 22px 8px; }
    .title { margin:0; color:var(--brand); font-size:1.45rem; font-weight:800; }
    .subtitle { margin:4px 0 0; color:var(--muted); font-size:.95rem; }
    .meta { margin:0 22px 16px; border:1px solid var(--border); border-radius:10px; overflow:hidden; width:calc(100% - 44px); border-collapse:separate; border-spacing:0; font-size:13px; }
    .meta td { padding:10px 12px; border-bottom:1px solid var(--border); vertical-align:top; }
    .meta tr:last-child td { border-bottom:0; }
    .meta td.label { width:40%; background:var(--soft); color:var(--brand); font-weight:700; border-right:1px solid var(--border); }
    .block { margin:0 22px 16px; border:1px solid var(--border); border-radius:{{radius_card}}; overflow:hidden; background:#fff; }
    .block-header { background:var(--soft); border-bottom:1px solid var(--border); padding:10px 14px; }
    .block-title { margin:0; color:var(--brand); font-weight:800; font-size:1.05rem; }
    .block-body { padding:14px 16px; }
    table.data { width:100%; border-collapse:collapse; font-size:13px; font-variant-numeric:tabular-nums; }
    table.data th { background:var(--soft); color:var(--brand); font-weight:700; text-align:left; padding:10px 12px; border-bottom:1px solid var(--border); }
    table.data td { padding:9px 12px; border-bottom:1px solid var(--border); }
    table.data tr:nth-child(even) td { background:var(--zebra); }
    table.data td.num, table.data th.num { text-align:right; }
    a { color:var(--link); text-decoration:none; }
    a:hover { text-decoration:underline; }
    .grid-2 { display:grid; grid-template-columns:1fr 1fr; gap:16px; margin:0 22px 16px; }
    .grid-2 > .block { margin:0; }
    .kpi { padding:16px; border-top:4px solid var(--accent); }
    .kpi-value { color:var(--brand); font-size:2rem; font-weight:800; line-height:1.1; }
    .kpi-label { color:var(--muted); font-size:.85rem; margin-top:4px; text-transform:uppercase; letter-spacing:.05em; }
    .footer { padding:18px 22px 26px; text-align:center; border-top:1px solid var(--border); color:var(--muted); font-size:13px; line-height:1.5; }
    .footer img { display:block; max-width:{{logo_report_size}}; margin:0 auto 8px; }
    .footer .company { color:var(--text); font-weight:700; }
    @media print { body { background:#fff; } .page-bg { padding:0; } .container { box-shadow:none; max-width:100%; } .block { page-break-inside:avoid; } }
  </style>
</head>
<body>
  <div class="page-bg">
    <div class="container">
      <div class="top-accent"></div>
      <div class="header">
        <h1 class="title">[Document Title]</h1>
        <p class="subtitle">[Optional subtitle / date]</p>
      </div>
      <table class="meta">
        <tr><td class="label">Datum</td><td>[date]</td></tr>
        <tr><td class="label">Opgesteld door</td><td>[author]</td></tr>
      </table>
      <div class="block">
        <div class="block-header"><h2 class="block-title">[Section]</h2></div>
        <div class="block-body"><p>[Content]</p></div>
      </div>
      <div class="footer">
        <img src="{{logo_url}}" alt="{{brand_name}} logo">
        <div class="company">{{footer_company}}</div>
        <div>{{footer_address}}</div>
        <div>{{footer_phone}}</div>
        <div><a href="{{footer_website_href}}">{{footer_website_display}}</a></div>
      </div>
    </div>
  </div>
</body>
</html>
```

**Chart palette** (for `references/html-reports.md`): primary `{{primary}}`, secondary `{{accent}}`, tertiary `{{text_secondary}}`, grid `{{border}}`, axis `{{text_secondary}}`. More than three series → repeat `{{primary}}` at reduced opacity. Chart titles in `{{primary}}`, never the accent.

## 2. Email scaffold → `assets/email-scaffold.html` and the core of `references/email.md`

Email rules: all CSS inline, `<table>` layout, `Margin` (capital M) on `<body>`, max-width ~680px, preheader span, top accent, centered logo footer.

```html
<!DOCTYPE html>
<html lang="{{lang}}">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{brand_name}} — [Onderwerp]</title>
  </head>
  <body style="Margin:0;padding:24px 0;background-color:{{bg}};">
    <div style="display:none;max-height:0;overflow:hidden;opacity:0;mso-hide:all;">[preheader]</div>
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="width:100%;border-collapse:collapse;background-color:{{bg}};">
      <tr>
        <td align="center" style="padding:24px 12px;">
          <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="width:100%;max-width:680px;border-collapse:collapse;background-color:{{card}};border:1px solid {{border}};border-radius:{{radius_card}};overflow:hidden;box-shadow:0 4px 12px rgba(0,0,0,.08);">
            <tr><td style="padding:0;border-top:{{accent_bar_height}} solid {{accent}};"></td></tr>
            <tr>
              <td style="background-color:{{bg}};padding:18px 22px;border-bottom:1px solid {{border}};text-align:center;font-family:{{font_stack}};">
                <div style="font-size:18px;line-height:1.4;color:{{primary}};font-weight:700;">[Titel]</div>
              </td>
            </tr>
            <tr>
              <td style="padding:18px 22px 8px 22px;font-family:{{font_stack}};font-size:14px;line-height:22px;color:{{text_primary}};">
                [Aanhef + korte intro. Geen marketingtaal.]
              </td>
            </tr>
            <tr>
              <td style="padding:14px 22px 6px 22px;font-family:{{font_stack}};font-size:14px;line-height:22px;color:{{text_primary}};">
                Met vriendelijke groet,<br><strong>[Afzender]</strong>
              </td>
            </tr>
            <tr>
              <td align="center" style="padding:16px 22px 24px 22px;border-top:1px solid {{border}};font-family:{{font_stack}};font-size:13px;line-height:1.4;color:{{text_secondary}};">
                <img src="{{logo_url}}" alt="{{brand_name}} logo" style="display:block;max-width:{{logo_email_size}};height:auto;margin:0 auto 8px;border:0;outline:none;">
                <p style="margin:4px 0;"><strong style="color:{{text_primary}};">{{footer_company}}</strong></p>
                <p style="margin:2px 0;">{{footer_address}}</p>
                <p style="margin:2px 0;">{{footer_phone}}</p>
                <p style="margin:2px 0;"><a href="{{footer_website_href}}" style="color:{{primary}};text-decoration:none;">{{footer_website_display}}</a></p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
```

**Optional CTA** (only when asked): a pill button in `{{primary}}` with white text, `border-radius:999px`. Never use the accent for CTA.

## 3. Voice & tone template → `references/voice-and-tone.md`

Fill from the extracted voice. Structure:

```markdown
# {{brand_name}} — Voice & Tone

## 1. Brand voice in one paragraph
{{personality_paragraph}}

## 2. Tone by context
| Context | Tone | Form of address |
|---|---|---|
| Customer email | {{...}} | {{u_or_je}} |
| Internal mail | {{...}} | {{...}} |
| Report / document | {{...}} | {{...}} |

## 3. Sentence patterns — Do / Don't
**Do:** {{do_list}}
**Don't:** {{dont_list}}

## 4. Greetings & sign-offs
Formal: {{...}} · Informal: {{...}}

## 5. Vocabulary swaps
| Instead of | Use |
|---|---|
| {{...}} | {{...}} |

## 6. Numbers, dates, money
{{locale_format_rules}}

## 7. Before / after
{{example_1}}
{{example_2}}
```

Keep it concrete: prefer real examples from the brand's own copy over abstract rules.
