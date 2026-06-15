---
layout: page
title: 수업
nav_title: 수업
permalink: /teaching/
description: 강의, 세미나, 튜토리얼 자료를 모아둔 공간입니다.
nav: true
nav_order: 5
---

{% assign visible_teachings = site.teachings | where_exp: "teaching", "teaching.hide != true" %}
{% assign sorted_teachings = visible_teachings | sort: "importance" %}

{% if sorted_teachings.size > 0 %}
<div class="publications">
  <ol class="bibliography">
    {% for teaching in sorted_teachings %}
      <li>
        <div class="row">
          <div class="col-sm-2 abbr">
            {% if teaching.term %}
              <abbr class="badge rounded w-100">{{ teaching.term }}</abbr>
            {% elsif teaching.date %}
              <abbr class="badge rounded w-100">{{ teaching.date | date: "%Y" }}</abbr>
            {% endif %}
          </div>
          <div class="col-sm-8">
            <div class="title">
              {% if teaching.url %}
                <a href="{{ teaching.url | relative_url }}">{{ teaching.title }}</a>
              {% else %}
                {{ teaching.title }}
              {% endif %}
            </div>
            {% if teaching.venue or teaching.role %}
              <div class="author">
                {% if teaching.role %}{{ teaching.role }}{% endif %}
                {% if teaching.role and teaching.venue %}, {% endif %}
                {% if teaching.venue %}{{ teaching.venue }}{% endif %}
              </div>
            {% endif %}
            {% if teaching.description %}
              <div class="periodical">
                {{ teaching.description }}
              </div>
            {% endif %}
            <div class="links">
              {% if teaching.website %}
                <a href="{{ teaching.website }}" class="btn btn-sm z-depth-0" role="button" rel="external nofollow noopener" target="_blank">Website</a>
              {% endif %}
              {% if teaching.slides %}
                <a href="{{ teaching.slides | relative_url }}" class="btn btn-sm z-depth-0" role="button">Slides</a>
              {% endif %}
              {% if teaching.repository %}
                <a href="{{ teaching.repository }}" class="btn btn-sm z-depth-0" role="button" rel="external nofollow noopener" target="_blank">Code</a>
              {% endif %}
              {% if teaching.materials %}
                <a href="{{ teaching.materials | relative_url }}" class="btn btn-sm z-depth-0" role="button">Materials</a>
              {% endif %}
            </div>
          </div>
        </div>
      </li>
    {% endfor %}
  </ol>
</div>
{% else %}
아직 등록된 수업이 없습니다.
{% endif %}
