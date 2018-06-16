---
layout: post
mathjax: true
comments: false
title: Adding MathJAX with LaTeX and MathML support to Jekyll
date: 2018-06-15
image: /images/mathjax-post-examples.png
---

Pages, Numbers, and Keynote gots updates today with [LaTeX and MathML support](https://support.apple.com/en-us/HT202501), and it reminded me that I wanted to add to my blog here. I always wanted to do this ever since I saw what was I think [Dr. Drang's MathJax](http://www.leancrew.com/all-this/2009/12/mathjax-equations-on-the-web/) post. Enter [MathJax](https://www.mathjax.org)!
![Powered by MathJax>](https://www.mathjax.org/badge/mj_logo.png "Powered by MathJax"){: border=0}

## Configuring jekyll

Heavily borrowing from
[Adding MathJax to a GitHub Pages Jekyll Blog](http://sgeos.github.io/github/jekyll/2016/08/21/adding_mathjax_to_a_jekyll_github_pages_blog.html), it was a quick task to add. The main changes to repo:

```
_includes/mathjax.html
assets/js/MathJaxLocal.js
_layouts/posts.html
```

The first two are new files[^1]^,[^2] including the necessary javascript code and [customization](http://docs.mathjax.org/en/latest/configuration.html#using-a-local-configuration-file-with-a-cdn) for [MathJax](https://www.mathjax.org).  And the `_layouts/posts.html` edit is to embed the javascript into the jekyll-rendered post page.


```diff
modified   _layouts/post.html
@@ -2,6 +2,8 @@
 layout: default
 ---

+{{ "{% include mathjax.html " }}%}
+

 <article class="post">
   <h1>{{ page.title }}</h1>
```

And in the Front Matter of `post` markdowns, on posts where mathjax is to be enabled:

```
[...]
mathjax: true
[...]
---
```







## Examples

These are my favorite part.


#### [Newton's law of universal gravitation](https://en.wikipedia.org/wiki/Newton's_law_of_universal_gravitation)


$$ F = G \frac{m_1 m_2} {r^2} $$

```
$$ F = G \frac{m_1 m_2} {r^2} $$
```

#### [Einstein field equations](https://en.wikipedia.org/wiki/Einstein_field_equations)

$$ R_{\mu \nu} - \frac{1} {2}Rg_{\mu \nu} + \Lambda g_{\mu \nu} = \frac{8\pi G} {c^4}T_{\mu \nu} $$

```
$$ R_{\mu \nu} - \frac{1} {2}Rg_{\mu \nu} + \Lambda g_{\mu \nu} = \frac{8\pi G} {c^4}T_{\mu \nu} $$
```

[^1]: [mathjax.html](https://github.com/idcrook/idcrook.github.io/blob/master/_includes/mathjax.html){: target="_blank"}
[^2]: [MathJaxLocal.js](https://github.com/idcrook/idcrook.github.io/blob/master/assets/js/MathJaxLocal.js){: target="_blank"}
