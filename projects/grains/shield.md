---
layout: default
title: Shields
parent: Grain Registry
grand_parent: Projects
nav_order: 1
permalink: /grains/shield/
---

# Shield GRAINs

{% assign grains = site.data['grain-index'].grains | where: "category", "shield" %}
{% if grains.size > 0 %}

<div class="slice-registry" markdown="block">

| Module | Summary | Status | Related Slices |
|---|---|---|---|
{% for g in grains -%}
| [{{ g.name | default: g.repo }}]({{ g.url }}) | {{ g.summary | default: "—" }} | <span class="slice-badge slice-badge--{{ g.status }}">{{ g.status }}</span> | {% if g.related_slices and g.related_slices.size > 0 %}{{ g.related_slices | join: ", " }}{% else %}—{% endif %} |
{% endfor %}

</div>

{% else %}
No shield GRAINs indexed yet.
{% endif %}
