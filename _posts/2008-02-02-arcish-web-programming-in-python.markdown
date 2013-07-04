---
layout: post
---

There seems to be little more sanity coming to the Arc discussion. Some people
are still paniced about HTML generation, but I&#8217;m not sure that you
really have to use that if you don&#8217;t like it. Others are just
disappointed because they were hoping for &#8230; I don&#8217;t know what,
some sort of Holy Grail, but it&#8217;s, *y'know*, just a programming
language.

The terseness it brings to common web expressions is quite pleasant though,
and I wanted to be able to have a similar level of power and terseness in
Python if possible. I spent a little time putting together
&#8220;pyflow&#8221; (named for both the nicer control-flow primitives and,
hopefully, a state of mind for its users). The &#8220;<a
href="http://arclanguage.org/item?id=722">Arc Challenge</a>&#8221; code looks
like:

{% highlight python %}
@opapp
def said(req):
    def result(foo):
        cede(link(text("you said: " + foo),
                  "click here"))
    cede(aform(result, input("foo")))
{% endhighlight %}

It&#8217;s 19 tokens (which is 4 more than the Arc version), but I still find
it nice to read. I prefer &#8220;foo&#8221; being passed as a real parameter
(vs. (arg _ &#8220;foo&#8221;) in Arc), but the cede()&#8217;s are somewhat
less pleasant on the Python side.

Moving to a reimplementation of  blog.arc, pyflow fares better.

{% highlight python %}
Posts = getstorelist("posts")
BlogTitle = "A Blog"

def blogPage(body):
    return defpage(fixed600(
                    tag("h1", link("blog", BlogTitle)),
                    body,
                    withsepbull(link("archive"), link("newpost", "new post"))),
                   title=BlogTitle)

def permalink(p): return "viewpost?id=%d" % p["id"]
def notfound(): return blogPage(div("spacedp", "No such post."))

def displayPost(p, user):
    head = tag("h2", link(permalink(p), p["title"]))
    user = " " + link("editpost?id=" + str(p["id"]), "[edit]") if user else ""
    return head + user + div("spacedp", markdown(p["body"]))
    
@opapp
def blog(req):
    user = getUser(req)
    return blogPage(flat([displayPost(p, user) for p in reversed(Posts[-5:])]))
    
@op
def archive(req):
    links = []
    for p in reversed(Posts):
        links.append(tag("li", link(permalink(p), p["title"])))
    return blogPage(ul(*links))

@op
def viewpost(req):
    id = req.getint('id')
    user = getUser(req)
    if id and id     else: return notfound()

@oplogin
def newpost(req):
    def res(t, b):
        p = {'id': len(Posts), 'title': t, 'body': b}
        Posts.append(p)
        commit()
        cede(redir(permalink(p)))
    cede(defpage(
            aform(res, withsepbr(
                input("t", "", 60),
                textarea("b", "", 10, 80) + br())),
            title="new post"))
        
@oplogin
def editpost(req):
    id = req.getint('id')
    def res(t, b):
        Posts[id]['title'] = t
        Posts[id]['body'] = b
        commit()
        cede(redir(permalink(Posts[id])))
    cede(defpage(
        aform(res, withsepbr(
            input("t", Posts[id]["title"], 60),
            textarea("b", Posts[id]["body"], 10, 80) + br())),
        title="edit post"))
{% endhighlight %}

Kind of long for Wordpress&#8217;s asinine (non-)code handling, but quite
short given the functionality that&#8217;s in there. (I got lazy on editpost,
it should really share code with newpost). Wins over the Arc code include:

**Simple persistent list/dict built in**. A lot of the fiddling in the Arc
code is to load/store/iterate over numbered files in the &#8216;posts&#8217;
directory. pyflow includes a simple transactional dict/list store for simple
storage (that also happens to work when there&#8217;s concurrent users, which
I don&#8217;t think blog.arc would do right now).

**Python functionality that&#8217;s somewhat terser than Arc**. For
example, the main entry point &#8220;/blog&#8221; looks like this in
blog.arc:

{% highlight cl %}
(defop blog req
  (let user (get-user req)
    (blogpage
      (for i 0 4
        (awhen (posts* (- maxid* i))
          (display-post user it)
          (br 3))))))
{% endhighlight %}

vs. in pyflow, it looks like:

{% highlight python %}
@opapp
def blog(req):
    user = getUser(req)
    return blogPage(flat([displayPost(p, user) for p in reversed(Posts[-5:])]))
{% endhighlight %}

List comprehension work nicely here to keep the number of tokens down.

**CSS**: Some of the layout-y (e.g. (br 3)) code that ends up being code in
Arc is in a default.css which also allows for snazzing things up pretty
easily. Although, I got lazy so there&#8217;s some formatting in the code in
pyflow that could be tidied up and shortened.

I don&#8217;t mean to imply the blog code couldn&#8217;t be squished down more
in Arc (I&#8217;m sure it could), or that I don&#8217;t like Arc&#8217;s
approach, but I think it&#8217;s worth exploring how similar idioms can be
expressed in various languages to try to improve everyone&#8217;s end
solution. Perhaps when Paul releases &#8220;news&#8221;, I&#8217;ll have a
chance to see if Arc is more of a win on larger and more production-quality
code bases.

Anyhow, I think the discussion surrounding Arc is the best thing that&#8217;s
happening right now. So, if you&#8217;re contributing, keep it up. Lots of
interesting stuff coming out. If anyone has any suggestions on how the pyflow
example code could be simplified with new idioms, please fire
away.
