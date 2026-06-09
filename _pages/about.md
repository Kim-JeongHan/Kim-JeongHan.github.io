---
layout: about
title: about
permalink: /
subtitle: Robotics Software Engineer | Motion Planning and Control

profile:
  align: right
  image: me.jpg
  image_circular: false
  more_info: >
    <p>Motion Algorithm Team</p>
    <p>Roboe Technologies</p>

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
---

I am a robotics software engineer at Roboe Technologies, where I work on motion planning, robot control, and collision-aware motion execution for industrial robot systems.

Before joining Roboe, I worked on autonomous mobile robot software at Gole Robotics. During my undergraduate years at Hanyang University, I also worked on HRI and robotics research through projects such as Snapbot and a separable drone-mobile robot patrol system.

I am interested in real-time robot path and motion planning for high-dimensional, constraint-rich environments, especially methods that can move from theory into reliable real-world robot deployment.

<div class="mb-4">
  <a class="btn btn-sm btn-outline-primary mb-2 mr-2" href="{{ '/cv/' | relative_url }}">CV</a>
  <a class="btn btn-sm btn-outline-primary mb-2 mr-2" href="{{ '/publications/' | relative_url }}">Publications</a>
  <a class="btn btn-sm btn-outline-primary mb-2 mr-2" href="{{ '/projects/' | relative_url }}">Projects</a>
  <a class="btn btn-sm btn-outline-primary mb-2 mr-2" href="https://github.com/Kim-JeongHan" target="_blank" rel="noopener noreferrer">GitHub</a>
  <a class="btn btn-sm btn-outline-primary mb-2" href="https://www.linkedin.com/in/jeonghan-kim-bb1013274" target="_blank" rel="noopener noreferrer">LinkedIn</a>
</div>

## [News]({{ '/news/' | relative_url }})

{% include news.liquid limit=true %}

## [Selected Publications]({{ '/publications/' | relative_url }})

{% include selected_papers.liquid %}

## Selected Projects

- [Snapbot]({{ '/projects/snapbot/' | relative_url }}) - manipulator-based HRI and computational photography system published at ACM/IEEE HRI 2024.
- [Separable Drone-Mobile Robot System]({{ '/projects/separable-drone-mobile-robot/' | relative_url }}) - drone-mobile robot platform for energy-efficient unmanned patrol, awarded at ICROS 2023.
- [Planning - Python 3D Path Planning Library]({{ '/projects/planning-python/' | relative_url }}) - open-source path-planning library for sampling-based planning and visualization.
