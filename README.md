# sphinxcontrib-partable
Sphinx extension for parameter tables

## usage

Define one or more tables using the *partable* directive:

    .. partable:: Overview of available keywords related to morphology
    
       dryslp
         :description: Critical avalanching slope above water (dz/dx and dz/dy)
         :default:     1.0
         :range:       0.1 - 2.0
         :units:       \-
       dzmax
         :advanced:
         :description: Maximum bed level change due to avalanching
         :default:     0.05
         :range:       0.0 - 1.0
         :units:       m/s/m
       depfile
         :required:
         :description: Name of the input bathymetry file
         :units:       <file>

Supported properties to describe a parameter are currently:

* description
* default
* range
* units
* required (does not take an argument, but marks the parameter with a *)
* advanced (does not take an argument, but marks the parameter with a +)

Parameter tables can be referenced using individual parameters with the *par* role:

    The user can limit the maximum bed level change due to avalanching using the keyword :par:`dzmax`.
