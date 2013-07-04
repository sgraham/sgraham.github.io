---
layout: post
title: Improve your App Launch in 4 hours
---

Picture a customer looking to solve her particular business problem.
Very occasionally, she might be looking to solve a problem in 5 minutes
or less, and simply be willing to choose the first thing that sort of
works that she runs across.

More likely though, she wants the **best solution for her**.

From experience, she knows that choosing the first half-assed solution
isn't going make for a **long-term victory**. Inevitably, it's going to
mean more hassle later on, because something won't work, or there will
be a migration cost, or the company will just be a pain to deal with.

### Evaluation

When a customer is performing evaluation of specific solutions, they
can't possibly have complete information. They're not going to have used
all the software for extended periods. Reviews and recommendations are
one method of pruning the search, but a review describes how well the
product fits the reviewer, not how well it will fit another specific
person.

### What does this mean to you?

Lacking complete information, a customer is looking for *signalling*
that tells them that **everything's going to be OK** if they go with
you.

- It's going solve their problem.
- They're not going to get hassled later.
- They're going to get good value for their money.

If you're reading this, you're clearly someone who **cares** about your
business, your application, and your customers. You are *hungry* and
*eager*. You are the polar *opposite* of the other half-assed company
that out-sourced development, design, and UX. You are the *opposite* of
the huge faceless corporation that can't really be bothered with smaller
customers, or solving their "trivial" problems.

***That you care deeply is what you must demonstrate to your customers.***

### Focusing resources

Of course, you're exhausted already. You're trying to launch here!
You're trying to cram all your launch features in, you're scrambling to
fix the blasted thing in IE. How are you going find time to actively
**demonstrate that you care** while you're too busy **actually caring**?

### Slice of Caring

The practical solution to this problem is what I awkwardly call a "Slice
of Caring".

Instead of trying to show off that you care in every aspect across your
whole business, you choose one particular slice to use as a
demonstration of your commitment.

Of course, you **do** actually care about the entire business, but the
effort involved in demonstrating this is huge, so pick something more
manageable.

In particular, you probably want to **pick something flashy** because
that's where users will look first. Flashy depends on your application
and problem domain. It might mean supporting the newest gadget, or it
might mean integrating with Microsoft Outlook, or it might mean
streamlining their Basecamp workflow, or it might be some other
customization for a vertical-within-a-vertical-within-a-niche that a
specific type of lawyer will love.

I don't know what it will be for you, but you can definitely find
something.

In my case, I was launching DropPic, an application for [designers to
create galleries of comps and mockups](http://droppic.com/). A few
designers had mentioned that their clients were iPad-obsessed, and would
really like to review designs on the iPad.

So, I added a review mode, customized for the iPad. You can try it [here
if you're on an
iPad](http://droppic.com/reviewer/6671513f116a4f0ba8c9db5702a6b229).

(On a WebKit-based desktop browser, you can add `?forcemob=1` to the
 preview page to see it. It doesn't work properly, but you can get the
 general idea.)

My customers are **thrilled** because they know their clients will love
it, and what they want is **happy, paying clients**.

**This took me 4 hours**, from deciding to do it, to figuring out that
Sencha Touch was probably the fastest way to get it done, to
implementation. It involved no changes to the backend, and is only about
200 lines of code. This is the sort of flashy feature you're looking
for.

It's important that you *not dig yourself a maintenance hole*. Pick
something that's both a slice to show you care, and also a standalone
column of functionality that isn't going to break every time you change
your application.

In my case, I'm using the same API for communication, so it's strictly a
different UI. If you were, for example, pulling contacts from Outlook,
you'd want to make sure that the "slice" was tool that talked
to Outlook, got data, and stuffed it through your regular
contact-importing-procedure, whatever that might be. Don't
create exceptions and special cases for extra features,
because that'll definitely come back to haunt you.

### Do it now

This is of key importance.

Demonstrating that you care is difficult. Caring is one thing, but
before they've used your great product, or experienced your outstanding
customer support, prospective customers won't really know if you care.
They therefore won't know whether they're going to be happy with your
product.

You must expend **additional** effort to show them that you care about the
big picture, the little details, and everything in between.

Without the extra effort, they're never going to experience the
excellence you have to offer.

But you can find something that will only take you 4 hours, be suitable
for signalling, and will [improve your
launch](http://news.ycombinator.com/item?id=1773398).

