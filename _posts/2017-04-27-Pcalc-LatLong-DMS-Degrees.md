---
layout: post
title: PCalc functions for converting between for latitude/longitude formats
---

I needed a way to convert Latitude/Longitude coordinates between Degrees+Decimal to Degrees Minutes Seconds notation. I created some user functions within the excellent PCalc app that can do this inline in PCalc.


# Pcalc and "User" functions

PCalc has an entire programmable interface for running calculator routines.

the Degrees-Minutes-Seconds (DMS) notation is as follows.  In the number `123.4532`, in the places after the decimal point, the `45` represents minutes, and the `32` represents seconds.

Showing the formula and including the "saved" files from PCalc is simplest way to reveal the function.

## D.dddddd -> D.MS

![decimal to DMS](/images/Ddddd_TO_DMS_Pcalc_function.png)



## D.MS -> D.dddddd

![DMS to decimal](/images/DMS_TO_Ddddd_Pcalc_function.png)


## User functions in PCalc

![User functions menu](/images/Pcalc_user_functions_dropdown.png)

When you run these functions, the results are returned directly into X input.

![Pcalc display](/images/latlong_Pcalc_display.png)


# Pcalc files

I "saved" these functions on PCalc (Mac) and share them here. I think it should be possible to load them within the app rather than recreating the formulas.

 - [Decimal Degrees to Degrees Minutes Seconds (D > DMS)](/images/Decimal Degrees to Degrees Minutes Seconds (D > DMS).pcalcfunctions)
 - [Degrees Minutes Seconds to Decimal Degrees (DMS > D)](/images/Degrees Minutes Seconds to Decimal Degrees (DMS > D).pcalcfunctions)
