---
layout: default
title: Modules
parent: Grain Registry
grand_parent: Projects
nav_order: 4
permalink: /grains/module/
---

# Module Grains

{% assign grains = site.data['grain-index'].grains | where: "category", "module" %}
{% if grains.size > 0 %}

<div class="slice-registry" markdown="block">

| Module | Summary | Status | Related Slices |
|---|---|---|---|
{% for g in grains -%}
| [{{ g.name | default: g.repo }}]({{ g.url }}) | {{ g.summary | default: "—" }} | <span class="slice-badge slice-badge--{{ g.status }}">{{ g.status }}</span> | {% if g.related_slices and g.related_slices.size > 0 %}{{ g.related_slices | join: ", " }}{% else %}—{% endif %} |
{% endfor %}

</div>

{% else %}
No module Grains indexed yet.
{% endif %}
