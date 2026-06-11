---
layout: page
title: Projects
nav_title: Projects
permalink: /projects/
description: Robotics, HRI, and autonomy projects.
nav: true
nav_order: 3
display_categories: [research, robotics, software]
---

<div class="publications">
{% if site.enable_project_categories and page.display_categories %}
  {% for category in page.display_categories %}
    {% assign categorized_projects = site.projects | where: "category", category | where_exp: "project", "project.hide_from_projects != true" %}
    {% assign sorted_projects = categorized_projects | sort: "importance" %}
    {% if sorted_projects.size > 0 %}
      <h2 class="bibliography" id="{{ category }}">{{ category }}</h2>
      <ol class="bibliography">
      {% for project in sorted_projects %}
        {% case project.category %}
          {% when "research" %}
            {% assign badge_color = "#6f42c1" %}
          {% when "robotics" %}
            {% assign badge_color = "#0b7285" %}
          {% when "software" %}
            {% assign badge_color = "#2f9e44" %}
          {% else %}
            {% assign badge_color = "#6c757d" %}
        {% endcase %}
        {% assign project_summary = project.content | markdownify | split: "</p>" | first | strip_html | strip %}
        {% assign project_link = project.url | relative_url %}
        {% assign project_link_external = false %}
        {% if project.website %}
          {% assign project_link = project.website %}
          {% if project.website contains '://' %}
            {% assign project_link_external = true %}
          {% endif %}
        {% endif %}
        <li>
          <div class="row">
            <div class="col col-sm-2 abbr">
              {% include project_preview.liquid project=project badge_color=badge_color %}
            </div>
            <div id="{{ project.title | slugify }}" class="col-sm-8">
              <div class="title">
                <a href="{{ project_link }}" {% if project_link_external %}target="_blank" rel="external nofollow noopener"{% endif %}>{{ project.title }}</a>
              </div>
              <div class="author">{{ project.description }}</div>
              <div class="periodical">
                <em>{{ project_summary }}</em>
              </div>
              <div class="links">
                <a href="{{ project_link }}" class="btn btn-sm z-depth-0" role="button" {% if project_link_external %}target="_blank" rel="external nofollow noopener"{% endif %}>Details</a>
                {% if project.github %}
                  <a href="{{ project.github }}" class="btn btn-sm z-depth-0" role="button" rel="external nofollow noopener" target="_blank">Code</a>
                {% endif %}
              </div>
            </div>
          </div>
        </li>
      {% endfor %}
      </ol>
    {% endif %}
  {% endfor %}
{% else %}
  {% assign visible_projects = site.projects | where_exp: "project", "project.hide_from_projects != true" %}
  {% assign sorted_projects = visible_projects | sort: "importance" %}
  <ol class="bibliography">
    {% for project in sorted_projects %}
      {% case project.category %}
        {% when "research" %}
          {% assign badge_color = "#6f42c1" %}
        {% when "robotics" %}
          {% assign badge_color = "#0b7285" %}
        {% when "software" %}
          {% assign badge_color = "#2f9e44" %}
        {% else %}
          {% assign badge_color = "#6c757d" %}
      {% endcase %}
      {% assign project_summary = project.content | markdownify | split: "</p>" | first | strip_html | strip %}
      {% assign project_link = project.url | relative_url %}
      {% assign project_link_external = false %}
      {% if project.website %}
        {% assign project_link = project.website %}
        {% if project.website contains '://' %}
          {% assign project_link_external = true %}
        {% endif %}
      {% endif %}
      <li>
        <div class="row">
          <div class="col col-sm-2 abbr">
            {% include project_preview.liquid project=project badge_color=badge_color %}
          </div>
          <div id="{{ project.title | slugify }}" class="col-sm-8">
            <div class="title">
              <a href="{{ project_link }}" {% if project_link_external %}target="_blank" rel="external nofollow noopener"{% endif %}>{{ project.title }}</a>
            </div>
            <div class="author">{{ project.description }}</div>
            <div class="periodical">
              <em>{{ project_summary }}</em>
            </div>
            <div class="links">
              <a href="{{ project_link }}" class="btn btn-sm z-depth-0" role="button" {% if project_link_external %}target="_blank" rel="external nofollow noopener"{% endif %}>Details</a>
              {% if project.github %}
                <a href="{{ project.github }}" class="btn btn-sm z-depth-0" role="button" rel="external nofollow noopener" target="_blank">Code</a>
              {% endif %}
            </div>
          </div>
        </div>
      </li>
    {% endfor %}
  </ol>
{% endif %}
</div>
