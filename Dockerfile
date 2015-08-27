FROM dpcrook/trusty-jekyll

RUN gem install public_suffix -v 1.4.6

RUN gem install github-pages -v 33

ADD . /tmp

RUN jekyll build --trace -s /tmp -d /usr/share/nginx/html
