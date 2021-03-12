---
layout: post
title: Secure Shellfish (Plus Textastic) on iPad Gets the Jobs Done
date: 2021-03-12
mathjax: False
comments: False
image: /images/shellfish_textastic_SBS.PNG
---

[Secure ShellFish](https://secureshellfish.app) is an iOS/iPadOS terminal + file sharing app by [Anders Borum](https://apps.apple.com/us/app/secure-shellfish-ssh-client/id1336634154). It has a few interesting features that make it a compelling tool to put in your iOS toolbox for  SSH-backed work.

## Terminal clients on iOS

I have been using [Blink.sh](https://blink.sh) on iOS for some time. It has improved hardware keyboard support and natively supports `mosh` mobile shell, which is handy for flaky SSH sessions. Originally using it built from source (see its [GitHub repo](https://github.com/blinksh/blink)), I eventually purchased Blink.sh from the AppStore.  It is reliable, but recently some of its limitations came to light, such as some native iOS integrations.

The rest of this post is about exploring *Secure Shellfish* as a terminal (SSH client) and its all-around iOS network and file-system capabilities.

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Important Features of Secure ShellFish](#important-features-of-secure-shellfish)
- [Demonstrating a Workflow, Including Screenshots](#demonstrating-a-workflow-including-screenshots)
    - [Open the (Remote) File Directly in iOS Editor (Textastic)](#open-the-remote-file-directly-in-ios-editor-textastic)
    - [(Re-)Generate the Blog Site](#re-generate-the-blog-site)
    - [Previewing Edits to the Blog Post](#previewing-edits-to-the-blog-post)
- [Conclusion](#conclusion)

<!-- markdown-toc end -->

## Important Features of Secure ShellFish

Here are a couple of the things that Secure Shellfish can do to make "Terminal Life" better on iOS:

Files.app compatibility
: Server directories appear in the Files app. Modern iOS apps can open files and directories in-place.  This is a **HUGE** feature over a typical SSH terminal app.

iOS integration with your shell
: As examples, from at a shell prompt in its terminal, you can access [Shortcuts](https://twitter.com/ShellFishApp/status/1174740782479290371?s=20), open webpages, and copy to pasteboard, all coordinating with native iOS apps or features.

*Secure Shellfish* has many other features that improve the iOS terminal experience. There's a way to always connect to a `tmux` session in a terminal startup configuration. Or iCloud can be used to sync SSH keys.
Edit a file on the server using [‎Textastic Code Editor 9 on the App Store](https://apps.apple.com/us/app/id1049254261?mt=8). And, it can be given permission to keep SSH sessions open in the "background", meaning it will keep an SSH session running even if you switch away from its app on iOS.

## Demonstrating a Workflow, Including Screenshots

I have this blog as a jekyll-based GitHub (User) Pages [repository on GitHub](https://github.com/idcrook/idcrook.github.io). Adding a new post involves adding a markdown file which contains the content of the post.

To preview edits as they are being made to the blog post, I can run `jekyll` as a server locally. For this demonstration, a Ubuntu virtual machine running on a QNAP NAS which lives on my home LAN is our "server".  The VM is configured to have an SSH server (which is how *Secure ShellFish* does most of its magic). It also has a container runtime (Docker) installed, which makes it convenient to run `jekyll` from a container.

Following is how this blog post was made by leveraging *Secure ShellFish* on an iPad.

### Open the (Remote) File Directly in iOS Editor (Textastic)

First, I opened the markdown file I wanted to edit. The following command opens the file (which resides on SSH server) in the Textastic app. The file I was editing is actually the markdown file for this post you are reading!

Installing its officially supported shell integration (for BASH, zsh, etc.) provides a built-in `textastic <<FILE>>` that works to open a file (via the SSH session, directly for a file on the server) in Textastic editor, and all right at a shell prompt in ssh terminal.

```console
$ textastic _posts/2021-03-10-secure-shellfish-plus-textastic-on-ipad-gets-the-jobs-done.md
```

For `textastic` command to work, it relies on installing *Secure Shellfish's* native shell integration. "Installing" involves sourcing its [shell helper file](https://github.com/idcrook/i-dotfiles/blob/main/shell/.shellfishrc) from shell startup files. The app even provides a way to automatically detect your shell and install its helper file from within an active ssh terminal session.

### (Re-)Generate the Blog Site

After opening the file to edit, I wanted to run Jekyll on the server, so that I could preview edits that were being made to the file. This was done using a `jekyll` docker image, and I started the docker container interactively.

Using the same terminal shell session that was used to launch iOS editor, the running `jekyll` server polls the filesystem to detect changes and then regenerates the blog. This (docker container) runs on the same virtual machine where we are (1) SSH-ed into for our terminal and (2) which has been exposed to iOS (by *Secure ShellFish*) the file we are editting.

![Shellfish Terminal next to Textastic](/images/shellfish_textastic_SBS.PNG)

If you look closely, you may even notice the `tmux` bottom bar in the terminal screen. I configured the server connection in *Secure ShellFish* this way. This means even if we lose connection to SSH session, the docker container will continue running and we can re-attach to same `tmux` session later.

### Previewing Edits to the Blog Post

I was able to use iPadOS multi-tasking to swap in `Safari.app` to view a previews of the regenerated pages after edits were made.  This is as simple as opening the web page the `jekyll` server was hosting on the VM on my local network.

![Preview in Safari next to Textastic](/images/safariPreview_textastic_SBS.PNG)

Note that even though *Secure ShellFish* was not a foreground application, it was still running `jekyll` in its SSH session (using its background running feature).

## Conclusion

I actually had purchased the Pro version of *Secure ShellFish* some time ago, but had usually used Blink.sh and before that [‎Prompt 2 on the App Store](https://apps.apple.com/us/app/prompt-2/id917437289?ign-mpt=uo%3D4) as my "iOS SSH app". So, this exploration of Secure ShellFish was a recent endeavor.

I was pleased to find *Secure ShellFish*'s tool chest of capabilities and features that enabled some seamless workflows that I hadn't realized were even possible on iOS.  I'd recommend you too try out *Secure ShellFish*.

I am also a fan of another of [Anders Borum](https://apps.apple.com/us/developer/anders-borum/id343532883)'s apps, the excellent [‎Working Copy - Git client on the App Store](https://apps.apple.com/us/app/working-copy/id896694807?ign-mpt=uo%3D6).
