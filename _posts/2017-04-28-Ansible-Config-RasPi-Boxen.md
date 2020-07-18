---
layout: post
title: Using Ansible to customize a box full of Raspberry Pis
---

I have been using Raspberry Pis for quite some time. Some are IoT apps like sensor logging or Airplay speakers. I've also provided a box full in various hands-on demos in the community. Accumulating a large collection of late-model Raspberry Pi's, I invested in ansible tasks to automate config and maintenance.

# What I Used to Do

I still use "DHCP reservations" to assign IP addresses to computers on personal networks.  That way, SSH configurations using IP addresses can be used, assigning "arbitrary" host names. Also, in demos ([] and []), I even bring my own pre-configured Wi-Fi router with me so that there's one less dependency to worry about. Anyone who's tried to give a live, hands-on demonstration across diverse groups in an arbitrary venue can appreciate why.

## Managing with SSH and csshx

Anyway, the configuration and maintenance of close to a dozen "identical" machines used to be performed using utility named [csshx](https://github.com/brockgr/csshx). It allows streaming inputs (over SSH sessions) identically to multiple target machines. Basically, a set of commands and steps that you could perform on one machine gets run on tens of machines.  On macOS, using [Homebrew](https://brew.sh/), you can install with:

```shell
brew install csshx
```

`csshx` is adequately functional. However, it takes interactive time and long-running operations are not easily pipelinable.

## Enter ansible

There are other shortfalls with the interactive SSH approach too.  What if you discovered later that an intermediate step you had performed was wrong, or needed to be slightly differently on each target, and it in turn affects subsequent configuration? Do you want to run the whole set of operations manually again across all the machines?

A better way is to use Ansible tool to perform the configuration and other operations. The machine configuration is contained in ansible playbooks and roles that are a type of specification for the operations to be performed. And even better, ansible performs it's magic over SSH into target machines, just like we had been doing manually.


# Ansible playbooks for Raspberry Pi

I have ansible roles for Raspberry Pi deployment, configuration, and maintenance, shared in a repository on GitHub: [raspberry-pi-rotary-phone](https://github.com/idcrook/raspberry-pi-rotary-phone). I Forget exactly why I named the repo that way but I think it was partly based on a auto-generated suggested name GitHub put forth at a New Repo creation.

Along with configuration of the operating system, I have added language support (node.js, e.g.), git repos that my demos use, and trimming image and memory footprints so that the first generation, single-core Raspberry Pi that I have still work great **even five years after their launch**!

## Using the ansible playbooks

I've shared the code on that repo, and used across many Raspbian based installations. The README's [Getting Started](https://github.com/idcrook/raspberry-pi-rotary-phone#getting-started) section covers pre-reqs and details on re-using the code.  At a high-level, you need imaged Pis, known IP address, SSH access, ansible installed, and clone of the GitHub repo. Further details are in the [README](https://github.com/idcrook/raspberry-pi-rotary-phone/blob/main/README.md#getting-started).
