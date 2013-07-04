---
layout: post
title: git branch in cmd.exe prompt
---

I really wanted the current git branch name in the prompt on Windows. It
turns out that getting this was ... somewhat non-trivial.

I thought at first that some wrappers around git commands might be
sufficient, but in practice that doesn't work because there's many ways
to change the current branch, and they're not all going to go through
the wrappers. And so it doesn't work consistently, which makes it almost
worse than not having it at all (because you can't trust it).

Poking around in cmd.exe's `prompt /?`, I found the variable `$M`. This
"displays the remote name associated with the current drive letter".
Windbg'ing cmd.exe showed that functionality is implemented by calling
[WNetGetConnection](http://msdn.microsoft.com/en-us/library/windows/desktop/aa385453.aspx)
This returned string gets embedded into the prompt which is similar to
what I want, and since I didn't even know about `$M`, I probably wouldn't
miss the original functionality...

Helpfully, there's only one call to `WNetGetConnectionW` too, so the
original functionality doesn't need to be conditionally maintained. So,
I tried IAT patching `WNetGetConnectionW` to replace it with a hardcoded
string as a test. Unfortunately the call to that function is guarded by
a call to `GetDriveType` (to check that the drive is actually a remote
drive). `GetDriveType` is a bit trickier; it's used for a variety of
different reasons in many places, so it can't be unconditionally
replaced without breaking other functionality.

The final solution looks like this (eliding a few complexities for
differences between the Windows 7 and Windows 8 binaries):

1. Loader exe uses `CreateRemoteThread()` with a ThreadProc of `LoadLibrary`
   to inject a DLL into the running cmd.exe.
2. (Now inside the injected DLL during attach) Push a PROMPT variable
   into the environment that contains the `$M` variable.
3. Overwrite the first instruction of `kernel32!GetDriveType` with a HLT,
   and install a vectored exception handler to trap that instruction.
4. Almost right away we'll try to render that prompt which will call
   `GetDriveType` in the `$M` handling code, which will fault. In the fault
   handler, walk up the stack, and if the code at the callsite matches
   the disassembly that we're expecting (a comparison with `DRIVE_REMOTE`,
   a particular form of jmp), then patch the comparison to compare to
   `DRIVE_FIXED` instead. This allows us to get to the `WNetGetConnectionW`
   call.
5. Restore the original operation of `GetDriveType`, and remove the
   vectored exception handler.
6. Patch the import address table for `WNetGetConnectionW` and have it
   jump to our "get git branch information" function instead.
7. Implement the actual git-related functionality via libgit2.

Because we don't have control over the working directory and don't want
to affect the normal cmd.exe operation too much, I did a little extra
packaging of the various binaries and dlls into one big exe that
extracts to TEMP and runs from there, and uses various path and DLL
functions to avoid DLL loading problems.

Also, I use Console2 to wrap cmd.exe. It's x86-only and so the cmd.exe
that I end up running is x86. Because of that and step #4 above, the
patching code currently only works on C:\Windows\SysWOW64\cmd.exe (that
is, the x86 version). It should be easy to extend to x64 though. And of
course, step #4 is generally just crazy-hacky, so it almost surely
doesn't work on versions of Windows that I haven't tried it on (fully
patched Windows 7 and Windows 8).

Anyway, after all that morally questionable mucking around, the end
result makes me happy. From an existing cmd.exe:

    d:\src\cmdEx>out\cmdEx.exe
    [master] d:\src\cmdEx>

Or, a bit more fancy during a conflicted rebase:

    [refs/heads/wps_impl 1/3|REBASE] d:\src\cr3\src>

meaning rebasing in-progress on step 1 of 3 on the named branch.

Code is at [github](https://github.com/sgraham/cmdEx/).
