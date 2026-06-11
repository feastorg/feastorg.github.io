---
layout: default
title: Integrated
parent: Slice Registry
grand_parent: Projects
nav_order: 3
permalink: /slices/integrated/
---

# Integrated Slices

{% assign slices = site.data['slice-index'].slices | where: "category", "integrated" %}
{% if slices.size > 0 %}

<div class="slice-registry" markdown="block">

| Module | Summary | Status | HW | Tags |
|---|---|---|---|---|
{% for s in slices -%}
| [{{ s.name | default: s.repo }}]({{ s.url }}) | {{ s.summary | default: "—" }} | <span class="slice-badge slice-badge--{{ s.status }}">{{ s.status }}</span> | {% if s.hw_version %}v{{ s.hw_version }} (gen {{ s.hw_gen_current }}){% else %}—{% endif %} | {% if s.tags and s.tags.size > 0 %}{{ s.tags | join: ", " }}{% else %}—{% endif %} |
{% endfor %}

</div>

{% else %}
No integrated slices indexed yet.
{% endif %}
