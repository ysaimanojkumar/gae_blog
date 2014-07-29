from google.appengine.api import mail
from google.appengine.ext import deferred

from base import FormController, renderIfCachedNoErrors

from lib.gae_validators import validateString, validateRequiredString, validateRequiredText, validateRequiredEmail
from gae_blog import model


class ContactController(FormController):
    """ handles request for the contact page of the site """

    FIELDS = {"author": validateRequiredString, "email": validateRequiredEmail, "subject": validateString, "body": validateRequiredText}

    @renderIfCachedNoErrors
    def get(self):

        blog = self.blog

        if not blog or not blog.contact:
            return self.renderError(403)

        sent = self.session.pop("blog_contact_sent", False)

        authors = [author for author in blog.authors if author.email]

        form_data, errors = self.errorsFromSession()

        return self.cacheAndRenderTemplate('contact.html', sent=sent, authors=authors, form_data=form_data, errors=errors, page_title="Contact")

    def post(self, sent=False):

        blog = self.blog
        if blog and blog.contact:
            
            bot = self.botProtection('/contact')
            if bot:
                self.session["blog_contact_sent"] = True
                return

            # validation and handling
            form_data, errors, valid_data = self.validate()

            if "author" not in errors:
                authors = []
                if valid_data["author"] == "all":
                    authors = [author for author in blog.authors if author.email]
                else:
                    author = model.BlogAuthor.get_by_id(valid_data["author"], parent=blog.key)
                    if author and author.email:
                        authors = [author]

                if not authors:
                    errors["author"] = True

            if errors:
                return self.redisplay(form_data, errors, self.blog_url + '/contact')

            if blog.title:
                subject = blog.title + " - Contact Form Message: " + valid_data["subject"]
            else:
                subject = "Blog - Contact Form Message: " + valid_data["subject"]

            if blog.admin_email:
                for author in authors:
                    deferred.defer(sendContactEmail, blog.admin_email, author.name + " <" + author.email + ">", subject,
                        valid_data["body"], valid_data["email"], _queue=blog.mail_queue)

        self.session["blog_contact_sent"] = True
        return self.redirect(self.blog_url + '/contact')


def sendContactEmail(sender, to, subject, body, reply_to):
    mail.send_mail(sender=sender, to=to, subject=subject, body=body, reply_to=reply_to)
