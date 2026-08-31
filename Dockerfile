FROM ruby:3.3.5

RUN apt-get update \
  && apt-get install --yes --no-install-recommends nodejs \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /srv/jekyll

COPY Gemfile Gemfile.lock ./
RUN bundle install

ENV BUNDLE_USER_HOME=/tmp/bundler

EXPOSE 4000

ENTRYPOINT ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0", "--port", "4000", "--force_polling", "--disable-disk-cache", "--destination", "/tmp/jekyll-site"]
