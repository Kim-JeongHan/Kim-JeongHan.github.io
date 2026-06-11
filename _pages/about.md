---
layout: about
title: about
permalink: /
subtitle: Robotics Software Engineer | Motion Planning and Control

profile:
  align: right
  image: me.jpg
  image_circular: false

selected_papers: false
social: true

announcements:
  enabled: false
  scrollable: true
  limit: 3

latest_posts:
  enabled: false
  scrollable: true
  limit: 5

display_categories: [research, robotics, open-source]
---

I am a robotics software engineer on the Motion Algorithm Team at Roboe Technologies, where I work on motion planning and control.

Before joining Roboe, I worked on autonomous mobile robot software at Gole Robotics. I received my B.S. degree from Hanyang University.

I am interested in real-time robot path and motion planning for high-dimensional, constraint-rich environments.

<div class="mb-4">
  <a class="btn btn-sm btn-outline-primary mb-2 mr-2" href="{{ '/cv/' | relative_url }}">CV</a>
  <a class="btn btn-sm btn-outline-primary mb-2 mr-2" href="{{ '/publications/' | relative_url }}">Publications</a>
  <a class="btn btn-sm btn-outline-primary mb-2" href="{{ '/projects/' | relative_url }}">Projects</a>
</div>

<div class="clearfix"></div>

## [News]({{ '/news/' | relative_url }})

{% include news.liquid limit=true %}

## Work Experience

{% include work_experience.liquid %}

## [Publications]({{ '/publications/' | relative_url }})

{% include selected_papers.liquid %}

## [Projects]({{ '/projects/' | relative_url }})

{% include projects_list.liquid display_categories=page.display_categories %}
