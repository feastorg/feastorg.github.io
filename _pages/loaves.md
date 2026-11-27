---
layout: default
title: Loaf Registry
parent: Projects
nav_order: 2
has_children: true
permalink: /loaves/
---

# Loaf Registry

All BREADS-compatible Loaves, auto-generated from each repo's `loaf.yaml` manifest.

A **Loaf** is the attachment and interconnect layer that lets Slices operate together as
one BREAD. A `backplane` provides Slice attachment; a `controller` provides the controller
interface and chains onto a backplane, with no Slice slots of its own.

{% assign loaves = site.data['loaf-index'].loaves %}
{% assign summary = site.data['loaf-index'].summary %}
{% assign generated = site.data['loaf-index'].generated %}
{% assign total = site.data['loaf-index'].total %}

{% if loaves %}

**{{ total }} loaves** · Generated {{ generated | slice: 0, 10 }}
{%- if summary.released and summary.released > 0 %} · <span class="slice-badge slice-badge--released">released {{ summary.released }}</span>{% endif %}
{%- if summary.built and summary.built > 0 %} · <span class="slice-badge slice-badge--built">built {{ summary.built }}</span>{% endif %}
{%- if summary.development and summary.development > 0 %} · <span class="slice-badge slice-badge--development">development {{ summary.development }}</span>{% endif %}
{%- if summary.concept and summary.concept > 0 %} · <span class="slice-badge slice-badge--concept">concept {{ summary.concept }}</span>{% endif %}
{%- if summary.retired and summary.retired > 0 %} · <span class="slice-badge slice-badge--retired">retired {{ summary.retired }}</span>{% endif %}

---

{% assign roles = "backplane,hybrid,controller" | split: "," %}

{% for role in roles %}
{% assign role_loaves = loaves | where: "role", role %}
{% if role_loaves.size > 0 %}

## {{ role | capitalize }}

<div class="slice-registry" markdown="block">

| Loaf | Summary | Slots | Bus | Status | HW | Tags |
|---|---|---|---|---|---|---|
{% for l in role_loaves -%}
| [{{ l.name | default: l.repo }}]({{ l.url }}) | {{ l.summary | default: "—" }} | {{ l.slice_slots }} | {{ l.bus_type | default: "—" }} | <span class="slice-badge slice-badge--{{ l.status }}">{{ l.status }}</span> | {% if l.hw_gen_current %}G{{ l.hw_gen_current }}{% else %}—{% endif %} | {% if l.tags and l.tags.size > 0 %}{{ l.tags | join: ", " }}{% else %}—{% endif %} |
{% endfor %}

</div>

{% endif %}
{% endfor %}

{% else %}

_No Loaf manifests found. The index is regenerated daily from `loaf.yaml` in each
`Loaf_*` repo._

{% endif %}
