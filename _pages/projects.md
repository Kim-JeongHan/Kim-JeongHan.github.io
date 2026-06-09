---
layout: page
title: Selected Projects
nav_title: Projects
permalink: /projects/
description: Selected robotics, HRI, and autonomy projects.
nav: true
nav_order: 3
display_categories: [research, robotics, software]
---

<div class="publications">
{% if site.enable_project_categories and page.display_categories %}
  {% for category in page.display_categories %}
    {% assign categorized_projects = site.projects | where: "category", category %}
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
        <li>
          <div class="row">
            <div class="col col-sm-2 abbr">
              <abbr class="badge rounded w-100" style="background-color:{{ badge_color }}">{{ project.category | upcase }}</abbr>
            </div>
            <div id="{{ project.title | slugify }}" class="col-sm-8">
              <div class="title">
                <a href="{{ project.url | relative_url }}">{{ project.title }}</a>
              </div>
              <div class="author">{{ project.description }}</div>
              <div class="periodical">
                <em>{{ project_summary }}</em>
              </div>
              <div class="links">
                <a href="{{ project.url | relative_url }}" class="btn btn-sm z-depth-0" role="button">Details</a>
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
  {% assign sorted_projects = site.projects | sort: "importance" %}
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
      <li>
        <div class="row">
          <div class="col col-sm-2 abbr">
            <abbr class="badge rounded w-100" style="background-color:{{ badge_color }}">{{ project.category | upcase }}</abbr>
          </div>
          <div id="{{ project.title | slugify }}" class="col-sm-8">
            <div class="title">
              <a href="{{ project.url | relative_url }}">{{ project.title }}</a>
            </div>
            <div class="author">{{ project.description }}</div>
            <div class="periodical">
              <em>{{ project_summary }}</em>
            </div>
            <div class="links">
              <a href="{{ project.url | relative_url }}" class="btn btn-sm z-depth-0" role="button">Details</a>
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
