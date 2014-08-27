from google.appengine.api import memcache

from base import FormController, renderIfCachedNoErrors

from gae_blog.lib.gae_validators import validateString, validateText, validateRequiredUrl
from gae_blog import model


class TrackbackController(FormController):

    FIELDS = {"title": validateString, "excerpt": validateText, "url": validateRequiredUrl, "blog_name": validateString}

    def get(self, post_slug):

        return self.renderError(405)

    def post(self, post_slug):

        ip_address = self.request.remote_addr
        blog = self.blog
        error = ''

        if not blog:
            error = 'There is no blog at this URL.'
        elif not blog.enable_comments or ip_address in blog.blocklist:
            error = 'This blog does not have trackbacks enabled.'
        elif not post_slug:
            error = 'Missing post ID.'
        else:
            post = model.BlogPost.get_by_id(post_slug, parent=blog.key)
            # only allow trackbacking to a post if it's actually published
            if not post or not post.published:
                error = 'There is no post with ID ' + post_slug
            else:
                form_data, errors, valid_data = self.validate()

                if valid_data["excerpt"]:
                    # strip out all HTML to be on the safe side
                    excerpt = model.stripHTML(valid_data["excerpt"])

                    if excerpt:
                        # turn URL's into links
                        excerpt = model.linkURLs(excerpt)
                        # finally, replace linebreaks with HTML linebreaks
                        excerpt = excerpt.replace("\r\n", "<br/>")

                if errors:
                    error = 'Invalid request.'
                else:
                    # look for a previously approved comment from this URL address on this blog
                    url = valid_data["url"]
                    query = blog.comments.filter(model.BlogComment.url == url)
                    query = query.filter(model.BlogComment.trackback == True)
                    approved = query.filter(model.BlogComment.approved == True)

                    comment = model.BlogComment(url=url, trackback=True, ip_address=ip_address, parent=post.key)

                    if valid_data["title"]:
                        comment.name = valid_data["title"]
                    if valid_data["excerpt"]:
                        comment.body = excerpt
                    if valid_data["blog_name"]:
                        comment.blog_name = valid_data["blog_name"]

                    if approved.count():
                        comment.approved = True
                        memcache.delete(self.request.path)
                    elif blog.moderation_alert and blog.admin_email:
                        # send out an email to the author of the post if they have an email address
                        # informing them of the comment needing moderation
                        author = post.author.get()
                        if author.email:
                            if blog.title:
                                subject = blog.title + " - Trackback Awaiting Moderation"
                            else:
                                subject = "Blog - Trackback Awaiting Moderation"
                            comments_url = self.request.host_url + self.blog_url + "/admin/comments"
                            body = "A trackback on your post \"" + post.title + "\" is waiting to be approved or denied at " + comments_url
                            self.deferEmail(author.name + " <" + author.email + ">", subject, body)

                    comment.put()

        self.renderTemplate('trackback.xml', error=error)