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
    <p>Software Engineer, Motion Algorithm Team</p>
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

I am a robotics software engineer on the Motion Algorithm Team at Roboe Technologies. My work focuses on motion planning, robot control, collision-aware motion execution, and optimization tooling for industrial robot systems.

Before joining Roboe Technologies, I worked on autonomous mobile robot software at Gole Robotics and conducted undergraduate HRI research at RAISE Lab, Hanyang University. Across these roles, I have built ROS/ROS2 systems, sensor benchmarking tools, manipulator control modules, mobile robot patrol software, and robot perception/planning pipelines.

My research direction is real-time robot path and motion planning for high-dimensional, constraint-rich environments. I am especially interested in optimization-based planning, diffusion-based planners, and constraint-aware control methods that can move from theory into reliable robot deployment.

## [News]({{ '/news/' | relative_url }})

{% include news.liquid limit=true %}

## Selected Projects

- [Snapbot]({{ '/projects/snapbot/' | relative_url }}) - manipulator-based HRI and computational photography system published at ACM/IEEE HRI 2024.
- [Separable Drone-Mobile Robot System]({{ '/projects/separable-drone-mobile-robot/' | relative_url }}) - drone-mobile robot platform for energy-efficient unmanned patrol, awarded at ICROS 2023.
- [Planning - Python 3D Path Planning Library]({{ '/projects/planning-python/' | relative_url }}) - open-source path-planning library for sampling-based planning and visualization.

## [Selected Publications]({{ '/publications/' | relative_url }})

{% include selected_papers.liquid %}
