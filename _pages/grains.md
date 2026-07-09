---
layout: default
title: Grain Registry
parent: Projects
nav_order: 2
has_children: true
permalink: /grains/
---

# Grain Registry

FEAST-adjacent PCB hardware modules: shields, cards, adapters, and support
boards that may be used in or alongside a BREAD without implementing the
BREADS Slice interface.

{% assign grains = site.data['grain-index'].grains %}
{% assign summary = site.data['grain-index'].summary %}
{% assign generated = site.data['grain-index'].generated %}
{% assign total = site.data['grain-index'].total %}

{% if grains and total > 0 %}

**{{ total }} grain{% if total != 1 %}s{% endif %}** · Generated {{ generated | slice: 0, 10 }}
{%- if summary.released and summary.released > 0 %} · <span class="slice-badge slice-badge--released">released {{ summary.released }}</span>{% endif %}
{%- if summary.prototype and summary.prototype > 0 %} · <span class="slice-badge slice-badge--prototype">prototype {{ summary.prototype }}</span>{% endif %}
{%- if summary.concept and summary.concept > 0 %} · <span class="slice-badge slice-badge--concept">concept {{ summary.concept }}</span>{% endif %}
{%- if summary.deprecated and summary.deprecated > 0 %} · <span class="slice-badge slice-badge--deprecated">deprecated {{ summary.deprecated }}</span>{% endif %}

---

<div class="slice-registry" markdown="block">

| Module | Category | Summary | Status | Related Slices |
|---|---|---|---|---|
{% for g in grains -%}
| [{{ g.name | default: g.repo }}]({{ g.url }}) | {{ g.category | default: "—" }} | {{ g.summary | default: "—" }} | <span class="slice-badge slice-badge--{{ g.status }}">{{ g.status }}</span> | {% if g.related_slices and g.related_slices.size > 0 %}{{ g.related_slices | join: ", " }}{% else %}—{% endif %} |
{% endfor %}

</div>

{% else %}

{: .warning }
Grain index not yet generated. It is built automatically on each site deployment.

{% endif %}
