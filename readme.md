Copyright &copy; 2016, [Sai Manoj Kumar Yadlapati](http://www.ysaimanojkumar.com/)  
Licensed under the [MIT license](http://www.opensource.org/licenses/MIT)

Permission is hereby granted, free of charge, to any person obtaining a 
copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the 
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included 
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
IN THE SOFTWARE.

GAE Blog is a project to provide a bare-bones blogging solution for Google App
Engine that makes no assumptions, and is easy to integrate with existing apps.


## Setup for Integrating with Your Project

In your pre-existing application add this project as a submodule, like so:

```bash
git submodule add git://github.com/bdoms/gae_blog.git gae_blog
```

Next, you need to initialize and update the submodule to get all the submodules
that exist within the gae_blog project:

```bash
cd gae_blog
git submodule init
git submodule update
```

Then repeat for your project:

```bash
cd ..
git submodule init
git submodule update
```

Finally, you need to merge the libraries and handlers from the example GAE Blog
`app.yaml` into your project's top level `app.yaml`. After doing that, starting
the development server and going to `/blog` will be handled by `gae_blog`.

Before deploying to production, be sure to replace the `secret_key` in the
`blog.py` script with randomized output for security. It's recommended that you
copy this file into your own project so that you can modify it and commit the
changes. Note that this script is also the place where you need to define your
URL routes.

Go to `/blog/admin` to configure your blog, post to it, and moderate comments.


## Setup for Using As a Parent Project

If you just want the blog to be the only part of your website, the process is
fairly similar. Just clone (or fork) the repository and you should be good.


## Managing Multiple Blogs

If you want to use GAE Blog for multiple blogs within the same project/domain,
you just have to decide on a relative URL for each one (`/blog` by default)
and modify these things:

 * add handlers for it to your `app.yaml` as mentioned above
 * add it to the `BLOG_URLS` list in `blog.py`
 * create each blog with its respective URL from `/blog/admin`


## Using a Custom Base Template

You can obviously modify the included base template as much as you want, but in
order to avoid redundancy, if you have one that you'd like to use, then
all you have to do is modify the "Base Template" configuration option on
the blog admin page (at `/blog/admin`) with a path relative to your project (i.e.
the parent directory of the `gae_blog` folder). For example, if your directory
structure looks like this:

 - your_project
   - gae_blog
   - your_templates
     - your_base_template.html

You would enter "your_templates/your_base_template.html" as the relative path.
However, if you leave that option blank, then the `default_base.html` file will
be used instead.

## Running Tests

Make sure that the path to the App Engine SDK is in the `PYTHONPATH`
environment variable. Then, running tests is simple:

```bash
python tests
```

## Scheduling Posts for the Future

There is some support for scheduling posts to be published in the future.
As noted on the admin post page, this is accomplished simply by checking the
"published" checkbox and entering a future timestamp. However, please note
that it is possible for pages including a yet-to-be-published post - such as
the index page, author pages (if enabled), and the RSS feed - to be put into
memcache after the post has been saved but before it has been published.
It is therefore recommended that you manually flush the cache if the post
appearing in those places is time sensitive.
