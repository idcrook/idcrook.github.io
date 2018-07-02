---
layout: post
mathjax: false
comments: false
title: Kubernetes 1.11 on Ubuntu 18.04 bare-metal single host
date: 2018-07-02
image: /images/kubernetes-1.11-system-pods.png
---

My Kubernetes 1.10 went down after some system updates and I couldn't bring it back.  It looked like incompatible `kubelet` versions and kubernetes tools updating underneath it from `1.10` to `1.11` was at least part of the problem alongside a `docker` upgrade. So I brought it back up quickly again using `kubeadm`, as described below.

Adapted from my earlier post:

 - [Kubernetes 1.10 on Ubuntu 18.04 bare-metal single host](https://idcrook.github.io/Kubernetes-Ubuntu-18.04-Bare-Metal-Single-Host/)

If you want to see how to include a monitoring dashboard (including with the required RBAC cluster service account) in the cluster, refer to that post.

## Install docker and kubernetes executables

```shell
sudo apt install docker.io
sudo systemctl enable docker

sudo apt-get update \
  && sudo apt-get install -y apt-transport-https \
  && curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
# bionic 18.04 repo still not yet available, so use 16.04 (xenial)
echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" \
  | sudo tee -a /etc/apt/sources.list.d/kubernetes.list \
  && sudo apt-get update
sudo apt install -y  kubeadm kubelet kubernetes-cni

# turn off swap
sudo swapoff -a
sudo rm -f /swapfile
sudo vi /etc/fstab
sudo swapon --summary
cat /proc/swaps
```

## Initialize kubernetes (single-host) cluster

Since I had already done the above steps previously, there was no need to repeat them, and I started here

```bash
IP_ADDR=$(ip addr show eno1 | grep -Po 'inet \K[\d.]+')
echo $IP_ADDR
sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address=${IP_ADDR} --kubernetes-version
```

## Setup cluster with flannel network fabric

See [https://github.com/coreos/flannel/blob/master/Documentation/kubernetes.md](https://github.com/coreos/flannel/blob/master/Documentation/kubernetes.md)

```shell
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/k8s-manifests/kube-flannel-rbac.yml
```

## Allow single node (master) cluster

Since there is only one node (and a master node) in our cluster, it has to be allowed

```shell
kubectl taint nodes --all node-role.kubernetes.io/master-
```

## Check that it is working and run some services!

```
kubectl get all --namespace=kube-system
kubectl get all --namespace=kube-system -o wide
```

I maintain in a Git repository my [homespun configs](https://github.com/idcrook/kubernetes-homespun) for a kubernetes cluster I run on my home network. [RUN.md](https://github.com/idcrook/kubernetes-homespun/blob/master/RUN.md) there shows the services I use.

I am a fan of [traefik](https://traefik.io/) a "cloud native edge router" which has Let's Encrypt support for HTTPS and great kubernetes support built-in. It let's me easily expose services to Internet over HTTPS. Definitely recommend.
