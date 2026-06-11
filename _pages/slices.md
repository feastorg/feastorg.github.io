---
layout: default
title: Slice Registry
parent: Projects
nav_order: 1
has_children: true
permalink: /slices/
---

# Slice Registry

All BREAD Slice modules, auto-generated from each repo's `slice.yaml` manifest.

{% assign slices = site.data['slice-index'].slices %}
{% assign summary = site.data['slice-index'].summary %}
{% assign generated = site.data['slice-index'].generated %}
{% assign total = site.data['slice-index'].total %}

{% if slices %}

**{{ total }} slices** · Generated {{ generated | slice: 0, 10 }}
{%- if summary.released and summary.released > 0 %} · <span class="slice-badge slice-badge--released">released {{ summary.released }}</span>{% endif %}
{%- if summary.validated and summary.validated > 0 %} · <span class="slice-badge slice-badge--validated">validated {{ summary.validated }}</span>{% endif %}
{%- if summary.prototype and summary.prototype > 0 %} · <span class="slice-badge slice-badge--prototype">prototype {{ summary.prototype }}</span>{% endif %}
{%- if summary.concept and summary.concept > 0 %} · <span class="slice-badge slice-badge--concept">concept {{ summary.concept }}</span>{% endif %}
{%- if summary.deprecated and summary.deprecated > 0 %} · <span class="slice-badge slice-badge--deprecated">deprecated {{ summary.deprecated }}</span>{% endif %}

---

{% assign categories = "actuation,sensing,integrated,power,interface,template,prototype" | split: "," %}

{% for cat in categories %}
{% assign cat_slices = slices | where: "category", cat %}
{% if cat_slices.size > 0 %}

## {{ cat | capitalize }}

<div class="slice-registry" markdown="block">

| Module | Summary | Status | HW | Tags |
|---|---|---|---|---|
{% for s in cat_slices -%}
| [{{ s.name | default: s.repo }}]({{ s.url }}) | {{ s.summary | default: "—" }} | <span class="slice-badge slice-badge--{{ s.status }}">{{ s.status }}</span> | {% if s.hw_version %}v{{ s.hw_version }} (gen {{ s.hw_gen_current }}){% else %}—{% endif %} | {% if s.tags and s.tags.size > 0 %}{{ s.tags | join: ", " }}{% else %}—{% endif %} |
{% endfor %}

</div>

{% endif %}
{% endfor %}

{% else %}

{: .warning }
Slice index not yet generated. It is built automatically on each site deployment.

{% endif %}
