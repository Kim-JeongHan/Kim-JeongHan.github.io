# frozen_string_literal: true

require "open3"
require "pathname"
require "time"

module GitLastModifiedAt
  def self.apply(site)
    documents = site.collections.values.flat_map(&:docs)
    pages = site.pages

    documents.each do |entry|
      next unless entry.respond_to?(:path)
      next unless File.file?(entry.path)

      set_created_date(site.source, entry)
      set_last_modified_at(site.source, entry)
    end

    pages.each do |entry|
      next unless entry.respond_to?(:path)
      next unless File.file?(entry.path)

      set_last_modified_at(site.source, entry)
    end

    site.posts.docs.sort! if site.respond_to?(:posts) && site.posts
  end

  def self.set_created_date(site_source, entry)
    return unless entry.respond_to?(:collection)
    return unless entry.collection&.label == "posts"
    return if front_matter_key?(entry.path, "date")

    created_at = git_created_at(site_source, entry.path) || File.mtime(entry.path)
    entry.data["date"] = created_at if created_at
  end

  def self.set_last_modified_at(site_source, entry)
    return if entry.data["sitemap"] == false

    modified_at = git_last_modified_at(site_source, entry.path) || File.mtime(entry.path)
    entry.data["last_modified_at"] = modified_at if modified_at
  end

  def self.front_matter_key?(path, key)
    lines = File.readlines(path, chomp: true)
    return false unless lines.first == "---"

    lines[1..].to_a.each do |line|
      break if line == "---" || line == "..."

      return true if line.match?(/\A#{Regexp.escape(key)}\s*:/)
    end

    false
  rescue StandardError
    false
  end

  def self.git_created_at(site_source, absolute_path)
    relative_path = relative_path(site_source, absolute_path)
    stdout, _stderr, status = Open3.capture3("git", "-C", site_source, "log", "--follow", "--format=%cI", "--", relative_path)
    return nil unless status.success?

    stdout.lines.map(&:strip).reject(&:empty?).last&.then { |date| Time.parse(date) }
  rescue StandardError
    nil
  end

  def self.git_last_modified_at(site_source, absolute_path)
    git_log(site_source, absolute_path, "-1", "--format=%cI")
  end

  def self.git_log(site_source, absolute_path, *args)
    relative_path = relative_path(site_source, absolute_path)
    stdout, _stderr, status = Open3.capture3("git", "-C", site_source, "log", *args, "--", relative_path)
    return nil unless status.success?

    value = stdout.strip
    return nil if value.empty?

    Time.parse(value)
  rescue StandardError
    nil
  end

  def self.relative_path(site_source, absolute_path)
    path = Pathname.new(absolute_path)
    return path.to_s unless path.absolute?

    path.relative_path_from(Pathname.new(site_source)).to_s
  end

  Jekyll::Hooks.register :site, :post_read do |site|
    GitLastModifiedAt.apply(site)
  end
end
