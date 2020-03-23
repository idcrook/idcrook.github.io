---
layout: post
title: Raytracing In One Weekend Series in C++, CUDA, and OptiX
date: 2020-03-21
mathjax: False
comments: False
image: /images/{imagepath}
---

One day, I found Peter Shirley's [Ray Tracing In One Weekend](https://github.com/RayTracing/raytracing.github.io) Book Series. I was able to implement my [own copy](https://github.com/idcrook/weeker_raytracer/tree/master/src/Cpp) of the code from his books, eventually also incorporating some versions using [CUDA](https://github.com/idcrook/weeker_raytracer/tree/master/src/Cuda) and Nvidia's [Optix 6.5](https://github.com/idcrook/weeker_raytracer/tree/master/src/OptiX) ray-tracing frameworks.

![Optix ROL final image](/images/rol-optix-final-alum_10k.png) Low-noise render from the OptiX implementation

## Building


The Cpp version is in portable, non-modern (that's a GOOD thing for the first descriptor) C++. That is what Shirley's reference code uses. See the README in the repo hosted on GitHub at  [https://github.com/idcrook/weeker_raytracer](https://github.com/idcrook/weeker_raytracer). The same repo contains all the versions described below (C++, CUDA, and OptiX 6.5).


I switched to Cmake from a generic Makefile early on. I had never used CMake before. The last time I used C++ for a project was over twenty years ago.  That is not an exaggeration; it was in a [Data Structures](https://cs.illinois.edu/courses/profile/CS225) class taken in the late 1990's. C++ itself has come quite a long way in that time.

CMake is adequate for nested project builds, but I spent more time dinking with CMake settings to get them to do what I wanted and learning about its commands than I did coding (also not an exaggeration). I have not tested any builds on Windows, but the code compiles (and runs, if all required pre-reqs are installed) on macOS and Linux.

The `Cpp` subdirectory, found at `/src/Cpp` in the repo is a faithful reproduction of the In One Weekend code, meaning it doesn't use any fancy intrinsics for SIMD calculations and it is single-threaded. So even on a CPU clocked at 4 GHz, runtimes are measured in hours for the more [advanced scenes](https://github.com/idcrook/weeker_raytracer/blob/master/README.md#image-renders-c-single-thread-cpu).

## CUDA

CUDA is a C++ environment where code can be written to target running on an Nvidia GPU alongside, or instead of, just a CPU.  To develop with it, a [toolkit from Nvidia](https://developer.nvidia.com/cuda-toolkit) is needed. To run CUDA device code, a supported Nvidia graphics card is needed. And that also means calculations, by nature, can run across a large number of graphics cores in parallel. The [final scene](https://github.com/idcrook/weeker_raytracer/blob/master/README.md#image-renders-cuda) from In One Weekend in CUDA version [rendered in seconds](https://github.com/idcrook/weeker_raytracer/blob/master/README.md#early-performance-comparisons) (versus minutes in the CPU single-threaded version).

I am a novice to Cuda programming. Like, [I had never used CUDA code before](https://github.com/idcrook/weeker_raytracer/tree/master/notes/cuda), and used [another person's repo](https://github.com/rogerallen/raytracinginoneweekendincuda) as reference. The part where I fell down and couldn't get back up was adapting the Bounded Volume Hierarchies (BVH-s) tree data structure for use on the CPUs. The [person](https://github.com/rogerallen) I drafted off of also ran into this. I didn't have a sophisticated enough understand on how to pass data structures back and forth between CPU <-> GPU. Nor did I have relevant experience to convert the data structures to generate and traverse on "device"-only. It is "device" (GPU) as opposed to "host" (CPU) in CUDA parlance.

CUDA stands for "Compute Unified Device Architecture", so it should be possible to figure out something. I stopped at the BVHs which appear early in the second book of the three part book series. I hope to finish out the books in CUDA some day.


## OptiX

OptiX is another Nvidia SDK that has been around for a while, launching first version in 2010. In recent hardware, notably starting with RTX branded cards, there is hardware support especially for raytracing operations.

To download SDKs, you must be a member of the NVIDIA Developer Program. With OptiX 7, it was re-architected and isn't backwards compatible with earlier version of the API. The most recent on the previous API is [Optix 6.5](https://developer.nvidia.com/designworks/optix/download), which is what the code in this repo uses.

OptiX contains special primitives and features for raytracing and a C++ wrapper library in the SDK. I closely followed in the path of [one person](https://github.com/trevordblack/OptixInOneWeekend) and [another person](https://github.com/joaovbs96/OptiX-Path-Tracer) who had done the In One Weekend series in OptiX.

The implementations are [blazing fast](https://github.com/idcrook/weeker_raytracer/blob/master/README.md#image-renders-optix-gpu) for renders and because of that, much larger scenes or sample quality can be obtained.

Another interested feature is that pieces of the ray-tracing process can be written in shader modules in CUDA code.  Here's a snippet from the repo for [calculating intersections with a sphere primitive](https://github.com/idcrook/weeker_raytracer/blob/master/src/OptiX/RestOfLife/geometry/sphere.cu#L39-L71) :

```c++
// The sphere intersection program
//   this function calls rtReportIntersection if an intersection occurs
//   As above, pid refers to a specific primitive, is ignored
RT_PROGRAM void intersection(int pid)
{
    float3 oc = theRay.origin - center;
    float a = optix::dot(theRay.direction, theRay.direction);
    float b = optix::dot(oc, theRay.direction);
    float c = optix::dot(oc, oc) - radius*radius;
    float discriminant = b*b - a*c;

    if (discriminant < 0.0f) return;

    float t = (-b - sqrtf(discriminant)) / a;
    if (t < theRay.tmax && t > theRay.tmin)
        if (rtPotentialIntersection(t))
        {
            hitRecord.point = rtTransformPoint(RT_OBJECT_TO_WORLD,  theRay.origin + t*theRay.direction);
            hitRecord.normal = optix::normalize(rtTransformNormal(RT_OBJECT_TO_WORLD, (hitRecord.point - center)/radius));
            get_sphere_uv(hitRecord.normal);
            rtReportIntersection(0);
        }

    t = (-b + sqrtf(discriminant)) / a;
    if (t < theRay.tmax && t > theRay.tmin)
        if (rtPotentialIntersection(t))
        {
            hitRecord.point = rtTransformPoint(RT_OBJECT_TO_WORLD,  theRay.origin + t*theRay.direction);
            hitRecord.normal = optix::normalize(rtTransformNormal(RT_OBJECT_TO_WORLD, (hitRecord.point - center)/radius));
            get_sphere_uv(hitRecord.normal);
            rtReportIntersection(0);
        }
}
```


## Nvidia installers and g++ 8 on Ubuntu

To get the default system compiler to be `g++-8` (the latest supported by the CUDA 10.1 toolkit I had installed), early on I made [some tweaks](https://github.com/idcrook/weeker_raytracer/blob/master/notes/optix/install.md) to my Ubuntu system software.


#### Installing on Ubuntu Linux x64 19.10

Download SDK from Nvidia developer site.

Have gone with placing all manually installed Nvidia toolkits into `/usr/local/nvidia/`

```shell
# make it to be writeable by user
sudo mkdir -p /usr/local/nvidia/
sudo chown -R $(id -u):$(id -g) /usr/local/nvidia/
chmod +w /usr/local/nvidia/

sh NVIDIA-OptiX-SDK-6.5.0-linux64.sh --skip-license \
  --prefix=/usr/local/nvidia --include-subdir
```


#### configure gcc-8 to be the default

```
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 10
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 20

sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-8 10
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-9 20

sudo update-alternatives --config gcc
sudo update-alternatives --config g++
```
