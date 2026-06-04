# Embedded brand fonts — licenses

All three typefaces are licensed under the **SIL Open Font License 1.1 (OFL)**,
which permits embedding (including base64-inlining into HTML deliverables) and
redistribution. Files are the Latin, weight-variable woff2 subsets mirrored by
[Fontsource](https://fontsource.org/) on jsDelivr.

- Fraunces — SIL Open Font License 1.1
- Inter — SIL Open Font License 1.1
- JetBrains Mono — SIL Open Font License 1.1

These are inlined at build time by `brand_fonts.fontface_css()` via the
`/*__FONTS__*/` token in each deliverable's template, keeping the generated HTML
fully self-contained and offline-capable.
