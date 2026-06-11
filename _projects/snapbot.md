---
layout: page
title: Snapbot
description: Enabling dynamic human-robot interactions for real-time computational photography.
importance: 1
category: research
github: https://github.com/Plan-Real/Snapbot
hide_from_projects: true
_styles: |
  .snapbot-page {
    --snapbot-accent: #2563eb;
    --snapbot-muted: var(--global-text-color-light, #6c757d);
    --snapbot-panel: var(--global-card-bg-color, #fff);
    --snapbot-soft: var(--global-bg-color, #f8f9fa);
    --snapbot-border: var(--global-divider-color, #dee2e6);
    max-width: 980px;
    margin: 0 auto;
  }

  .snapbot-page img {
    display: block;
    width: 100%;
    border-radius: 8px;
  }

  .snapbot-page section {
    margin-top: 2.5rem;
  }

  .snapbot-meta {
    text-align: center;
    margin-top: -0.25rem;
  }

  .snapbot-authors {
    color: var(--snapbot-muted);
    font-size: 1rem;
    line-height: 1.6;
  }

  .snapbot-venue {
    color: var(--snapbot-muted);
    font-weight: 600;
    margin-top: 0.35rem;
  }

  .snapbot-links {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    justify-content: center;
    margin: 1.1rem 0 1.6rem;
  }

  .snapbot-link {
    align-items: center;
    border: 1px solid var(--snapbot-border);
    border-radius: 6px;
    color: var(--global-text-color) !important;
    display: inline-flex;
    font-size: 0.92rem;
    font-weight: 600;
    gap: 0.4rem;
    line-height: 1;
    padding: 0.62rem 0.85rem;
    text-decoration: none;
  }

  .snapbot-link:hover {
    border-color: var(--snapbot-accent);
    color: var(--snapbot-accent) !important;
    text-decoration: none;
  }

  .snapbot-figure {
    margin: 0;
  }

  .snapbot-caption {
    color: var(--snapbot-muted);
    font-size: 0.95rem;
    line-height: 1.55;
    margin: 0.75rem auto 0;
    max-width: 820px;
    text-align: center;
  }

  .snapbot-section-title {
    font-size: 1.65rem;
    font-weight: 700;
    letter-spacing: 0;
    margin: 0 0 1rem;
  }

  .snapbot-lead {
    font-size: 1.05rem;
    line-height: 1.75;
  }

  .snapbot-panel {
    background: var(--snapbot-soft);
    border: 1px solid var(--snapbot-border);
    border-radius: 8px;
    padding: 1.15rem;
  }

  .snapbot-columns {
    display: grid;
    gap: 1rem;
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .snapbot-card {
    background: var(--snapbot-panel);
    border: 1px solid var(--snapbot-border);
    border-radius: 8px;
    padding: 1rem;
  }

  .snapbot-card h3 {
    font-size: 1rem;
    font-weight: 700;
    margin: 0 0 0.45rem;
  }

  .snapbot-card p,
  .snapbot-card li {
    color: var(--snapbot-muted);
    font-size: 0.95rem;
    line-height: 1.6;
    margin-bottom: 0;
  }

  .snapbot-pipeline {
    display: grid;
    gap: 1rem;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .snapbot-pipeline figure {
    border: 1px solid var(--snapbot-border);
    border-radius: 8px;
    margin: 0;
    overflow: hidden;
  }

  .snapbot-pipeline figcaption {
    color: var(--snapbot-muted);
    font-size: 0.9rem;
    line-height: 1.45;
    padding: 0.75rem;
  }

  .snapbot-video {
    position: relative;
    width: 100%;
    padding-bottom: 56.25%;
    border-radius: 8px;
    overflow: hidden;
    background: #000;
  }

  .snapbot-video iframe {
    border: 0;
    height: 100%;
    left: 0;
    position: absolute;
    top: 0;
    width: 100%;
  }

  .snapbot-results {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.93rem;
  }

  .snapbot-results th,
  .snapbot-results td {
    border: 1px solid var(--snapbot-border);
    padding: 0.55rem;
    text-align: center;
  }

  .snapbot-results th {
    background: var(--snapbot-soft);
    font-weight: 700;
  }

  .snapbot-results td:first-child,
  .snapbot-results th:first-child {
    text-align: left;
  }

  @media (max-width: 760px) {
    .snapbot-columns,
    .snapbot-pipeline {
      grid-template-columns: 1fr;
    }

    .snapbot-links {
      align-items: stretch;
      flex-direction: column;
    }

    .snapbot-link {
      justify-content: center;
    }
  }
---

<div class="snapbot-page">
  <div class="snapbot-meta">
    <div class="snapbot-authors">
      Chanyeok Choi, <strong>Jeonghan Kim</strong>, Yunjae Nam, Youngmoon Lee
    </div>
    <div class="snapbot-venue">ACM/IEEE HRI 2024 Late-Breaking Report</div>
    <div class="snapbot-links">
      <a class="snapbot-link" href="https://dl.acm.org/doi/pdf/10.1145/3610978.3640712" target="_blank" rel="external nofollow noopener">
        <i class="fa-solid fa-file-pdf" aria-hidden="true"></i>
        <span>Paper</span>
      </a>
      <a class="snapbot-link" href="https://doi.org/10.1145/3610978.3640712" target="_blank" rel="external nofollow noopener">
        <i class="fa-solid fa-link" aria-hidden="true"></i>
        <span>ACM DL</span>
      </a>
      <a class="snapbot-link" href="https://github.com/Plan-Real/Snapbot" target="_blank" rel="external nofollow noopener">
        <i class="fa-brands fa-github" aria-hidden="true"></i>
        <span>Code</span>
      </a>
      <a class="snapbot-link" href="https://drive.google.com/file/d/13aQ0mCv9reuY-JInxXiSdqex67w7G5Ey/view" target="_blank" rel="external nofollow noopener">
        <i class="fa-solid fa-video" aria-hidden="true"></i>
        <span>Demo</span>
      </a>
    </div>
  </div>

  <section>
    <figure class="snapbot-figure">
      <img src="{{ '/assets/img/projects/snapbot/snapbot_teaser.jpg' | relative_url }}" alt="Snapbot dynamically tracks a moving person and adjusts camera composition with a UR3 manipulator">
      <figcaption class="snapbot-caption">
        Snapbot couples a UR3 manipulator and computational photography pipeline to keep a moving human subject in frame, select high-quality shots, and enhance the final photo in real time.
      </figcaption>
    </figure>
  </section>

  <section>
    <h2 class="snapbot-section-title">Abstract</h2>
    <p class="snapbot-lead">
      Snapbot is a human-robot interaction system for robotic photography. Instead of treating photography as a static portrait problem, it combines perception, manipulator control, image scoring, and enhancement so a camera mounted on a robot arm can respond to a moving person and produce a polished image.
    </p>
    <p>
      My contribution focused on the robot software side: estimating the transform between the person and camera, implementing closed-loop inverse-kinematics control, filtering the control input for stable tracking, and integrating the manipulation stack with the end-to-end HRI pipeline.
    </p>
  </section>

  <section>
    <h2 class="snapbot-section-title">How Snapbot Works</h2>
    <figure class="snapbot-figure">
      <img src="{{ '/assets/img/projects/snapbot/snapbot_overview.png' | relative_url }}" alt="Snapbot system overview showing perception, control, and computational photography stages">
    </figure>
    <div class="snapbot-columns" style="margin-top: 1rem;">
      <div class="snapbot-card">
        <h3>Perception</h3>
        <p>Detects a face and estimates pose cues used for exposure, focus, and camera composition.</p>
      </div>
      <div class="snapbot-card">
        <h3>Control</h3>
        <p>Maps the subject pose into a desired camera pose and drives the UR3 arm with damped inverse kinematics.</p>
      </div>
      <div class="snapbot-card">
        <h3>Photography</h3>
        <p>Scores burst shots and applies enhancement so the selected photo is ready for the user-facing experience.</p>
      </div>
    </div>
  </section>

  <section>
    <h2 class="snapbot-section-title">Dynamic Camera Composition</h2>
    <figure class="snapbot-figure">
      <img src="{{ '/assets/img/projects/snapbot/snapbot_composition.png' | relative_url }}" alt="Dynamic camera composition simulation for a moving human subject">
      <figcaption class="snapbot-caption">
        The camera pose is re-solved as the person moves and turns, while workspace limits keep the manipulator inside a reachable region.
      </figcaption>
    </figure>
  </section>

  <section>
    <h2 class="snapbot-section-title">Interactive Photo Studio Pipeline</h2>
    <p>
      Around the robot pipeline, the project also built an event-facing photo studio workflow. Visitors could be photographed by the robot, choose a stylized result, select a frame, and receive a printed photo on site.
    </p>
    <div class="snapbot-pipeline">
      <figure>
        <img src="{{ '/assets/img/projects/snapbot/pipeline_tracking.jpg' | relative_url }}" loading="lazy" alt="UR3 robot arm tracking a person in real time">
        <figcaption>1. Robot arm tracks the subject.</figcaption>
      </figure>
      <figure>
        <img src="{{ '/assets/img/projects/snapbot/pipeline_stylize.jpg' | relative_url }}" loading="lazy" alt="Photo selection screen with AI stylized variants">
        <figcaption>2. Candidate photos are scored and stylized.</figcaption>
      </figure>
      <figure>
        <img src="{{ '/assets/img/projects/snapbot/pipeline_frame.jpg' | relative_url }}" loading="lazy" alt="Frame selection screen for the final printed photo">
        <figcaption>3. Visitor selects a frame.</figcaption>
      </figure>
      <figure>
        <img src="{{ '/assets/img/projects/snapbot/pipeline_print.jpg' | relative_url }}" loading="lazy" alt="Photo printer producing the final enhanced image">
        <figcaption>4. The final image is printed.</figcaption>
      </figure>
    </div>
  </section>

  <section>
    <h2 class="snapbot-section-title">Results</h2>
    <figure class="snapbot-figure">
      <img src="{{ '/assets/img/projects/snapbot/snapbot_comparison.jpg' | relative_url }}" loading="lazy" alt="Snapbot ablation result comparing focus, composition, scoring, and enhancement stages">
    </figure>
    <div class="snapbot-panel" style="margin-top: 1rem; overflow-x: auto;">
      <table class="snapbot-results">
        <thead>
          <tr>
            <th></th>
            <th>Score</th>
            <th>Balancing</th>
            <th>DoF</th>
            <th>Light</th>
            <th>Object</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>AVA Dataset</td>
            <td>0.5189</td>
            <td>0.0341</td>
            <td>0.1152</td>
            <td>0.0568</td>
            <td>0.0941</td>
          </tr>
          <tr>
            <td><strong>Snapbot</strong></td>
            <td><strong>0.7852</strong></td>
            <td><strong>0.8085</strong></td>
            <td><strong>0.7318</strong></td>
            <td><strong>0.7799</strong></td>
            <td><strong>0.6360</strong></td>
          </tr>
          <tr>
            <td>w/o EIGM</td>
            <td>0.5521</td>
            <td>0.7002</td>
            <td>0.5910</td>
            <td>0.5832</td>
            <td>0.4217</td>
          </tr>
          <tr>
            <td>w/o ISM, EIGM</td>
            <td>0.3544</td>
            <td>-0.062</td>
            <td>0.1144</td>
            <td>-0.1943</td>
            <td>-0.1030</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>

  <section>
    <h2 class="snapbot-section-title">Demo Video</h2>
    <div class="snapbot-video">
      <iframe src="https://drive.google.com/file/d/13aQ0mCv9reuY-JInxXiSdqex67w7G5Ey/preview" allow="autoplay; encrypted-media" allowfullscreen title="Snapbot demo video"></iframe>
    </div>
  </section>
</div>
