---
layout: about
title: about
permalink: /

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

I am a robotics researcher and software engineer focused on path planning for high-dimensional robotic systems under complex constraints.

Most recently, I was a Visiting Student Researcher at the University of Michigan, advised by [Prof. Kang G. Shin](https://web.eecs.umich.edu/~kgshin/), where I worked on generative path planning and offline decision-making. Previously, I developed motion-planning software for industrial manipulators at Roboe Technologies and autonomous mobile robot software at Gole Robotics.

I received my B.S. degree in Robot Engineering from Hanyang University ERICA, where I conducted undergraduate research at RAISE Lab. I am grateful to [Prof. Youngmoon Lee](https://sites.google.com/umich.edu/youngmoonlee/home) for his mentorship and guidance during this period.

<div class="mb-4">
  <a class="btn btn-sm btn-outline-primary mb-2 mr-2" href="{{ '/cv/' | relative_url }}">CV</a>
  <a class="btn btn-sm btn-outline-primary mb-2 mr-2" href="{{ '/publications/' | relative_url }}">Publications</a>
  <a class="btn btn-sm btn-outline-primary mb-2" href="{{ '/projects/' | relative_url }}">Projects</a>
</div>

<div class="clearfix"></div>

## [News]({{ '/news/' | relative_url }})

{% include news.liquid limit=true %}

## Experience

{% include work_experience.liquid %}

## [Publications]({{ '/publications/' | relative_url }})

{% include selected_papers.liquid %}

## [Projects]({{ '/projects/' | relative_url }})

{% include projects_list.liquid display_categories=page.display_categories %}
