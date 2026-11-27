---
layout: default
title: Slice Registry
parent: Projects
nav_order: 1
has_children: true
permalink: /slices/
---

# Slice Registry

All BREADS-compatible Slice modules, auto-generated from each repo's
`slice.yaml` manifest.

{% assign slices = site.data['slice-index'].slices %}
{% assign summary = site.data['slice-index'].summary %}
{% assign generated = site.data['slice-index'].generated %}
{% assign total = site.data['slice-index'].total %}

{% if slices %}

**{{ total }} slices** · Generated {{ generated | slice: 0, 10 }}
{%- if summary.released and summary.released > 0 %} · <span class="slice-badge slice-badge--released">released {{ summary.released }}</span>{% endif %}
{%- if summary.built and summary.built > 0 %} · <span class="slice-badge slice-badge--built">built {{ summary.built }}</span>{% endif %}
{%- if summary.development and summary.development > 0 %} · <span class="slice-badge slice-badge--development">development {{ summary.development }}</span>{% endif %}
{%- if summary.concept and summary.concept > 0 %} · <span class="slice-badge slice-badge--concept">concept {{ summary.concept }}</span>{% endif %}
{%- if summary.retired and summary.retired > 0 %} · <span class="slice-badge slice-badge--retired">retired {{ summary.retired }}</span>{% endif %}

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
| [{{ s.name | default: s.repo }}]({{ s.url }}) | {{ s.summary | default: "—" }} | <span class="slice-badge slice-badge--{{ s.status }}">{{ s.status }}</span> | {% if s.hw_gen_current %}G{{ s.hw_gen_current }}{% else %}—{% endif %} | {% if s.tags and s.tags.size > 0 %}{{ s.tags | join: ", " }}{% else %}—{% endif %} |
{% endfor %}

</div>

{% endif %}
{% endfor %}

{% else %}

{: .warning }
Slice index not yet generated. It is built automatically on each site deployment.

{% endif %}
