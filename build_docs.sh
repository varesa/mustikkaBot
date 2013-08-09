#!/bin/sh

if [ `command -v sphinx-build` ]; then 
    sphinxcmd=sphinx-build
elif [ `command -v sphinx-build-3.3` ]; then
    sphinxcmd=sphinx-build-3.3
fi

$sphinxcmd docs_src/ docs_build/
