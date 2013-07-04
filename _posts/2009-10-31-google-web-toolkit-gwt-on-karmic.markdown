---
layout: post
title: Google Web Toolkit (GWT) on Karmic
---

I wanted to try out a more recent version of GWT, it's supposed to have
support for mobile browsers as well as some other shiny stuff.

I installed Eclipse on Ubuntu 9.10 (Karmic), which is the most recent version
(3.5.1). Google's got a nice plugin that you can install in one place and it
sets up templates, and installs the AppEngine SDK and the GWT SDK.

So far so good.

Unfortunately, when I try to run any application in Eclipse, I get this lovely
message:

    ** Unable to load Mozilla for hosted mode **
    java.lang.UnsatisfiedLinkError: /home/sgraham/.eclipse/org.eclipse.platform_3.5.0_155965261/
    plugins/com.google.gwt.eclipse.sdkbundle.linux_1.7.1.v200909221731/gwt-linux-1.7.1/
    mozilla-1.7.12/libxpcom.so:
    libstdc++.so.5: cannot open shared object file: No such file or directory

I guess there's some binary version of Mozilla they're using internally, but
it's built against an old shared stdc++ library that Karmic doesn't ship
anymore. libstdc++5 isn't installable from the repos, but I just grabbed the
`.deb` from the Jaunty page
[here](http://packages.ubuntu.com/jaunty/i386/libstdc++5/download) and
installed it.

And... all seems well now. I don't really know if that has any adverse effects, but I
haven't noticed anything yet.
