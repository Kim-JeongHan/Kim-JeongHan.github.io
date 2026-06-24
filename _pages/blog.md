---
layout: default
permalink: /blog/
title: blog(kr)
nav: true
nav_order: 4
pagination:
  enabled: true
  collection: posts
  permalink: /page/:num/
  per_page: 10
  sort_field: date
  sort_reverse: true
  trail:
    before: 1 # The number of links before the current page
    after: 3 # The number of links after the current page
---

<div class="post">

{% assign blog_name_size = site.blog_name | size %}
{% assign blog_description_size = site.blog_description | size %}
{% assign latest_post = site.posts | first %}

{% if blog_name_size > 0 or blog_description_size > 0 %}

  <div class="header-bar">
    {% if blog_name_size > 0 %}
      <h1>{{ site.blog_name }}</h1>
    {% endif %}
    {% if blog_description_size > 0 %}
      <h2>{{ site.blog_description }}</h2>
    {% endif %}
    <div class="blog-index-stats" aria-label="Blog summary">
      <span><strong>{{ site.posts.size }}</strong> 글</span>
      <span><strong>{{ site.categories.size }}</strong> 카테고리</span>
      {% if latest_post %}
        <span>최근 <strong>{{ latest_post.date | date: '%Y.%m.%d' }}</strong></span>
      {% endif %}
    </div>
  </div>
  {% endif %}

<div class="blog-index-mobile-nav">
  <details class="blog-category-details">
    <summary class="blog-category-summary">
      <span>카테고리</span>
      <i class="fa-solid fa-chevron-down fa-sm"></i>
    </summary>
    {% include blog_category_browser.liquid active_all=true %}
  </details>
</div>

<div class="blog-index-layout">
  <div class="blog-index-feed">

{% assign featured_posts = site.posts | where: "featured", "true" %}
{% if featured_posts.size > 0 %}
<section class="blog-index-section" aria-labelledby="featured-notes-heading">
  <h2 id="featured-notes-heading" class="blog-section-title">추천 글</h2>
  <div class="blog-featured-grid">
    {% for post in featured_posts %}
      {% include blog_post_card.liquid post=post featured=true %}
    {% endfor %}
  </div>
</section>

{% endif %}

  <section class="blog-index-section" aria-labelledby="latest-notes-heading">
    <h2 id="latest-notes-heading" class="blog-section-title">최신 글</h2>
    <div class="blog-post-list">

    {% if page.pagination.enabled %}
      {% assign postlist = paginator.posts %}
    {% else %}
      {% assign postlist = site.posts %}
    {% endif %}

    {% for post in postlist %}
      {% include blog_post_card.liquid post=post %}

    {% endfor %}

    </div>
  </section>

{% if page.pagination.enabled %}
{% include pagination.liquid %}
{% endif %}

  </div>

  <aside class="blog-index-sidebar">
    {% include blog_category_browser.liquid active_all=true %}
  </aside>
</div>

</div>
