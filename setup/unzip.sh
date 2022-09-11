#!/bin/bash

for f in *.tar.gz; do
  d=`basename "$f" .tar.gz`
  mkdir "$d-csv"
  (cd "$d-csv" && tar xf "../$f")
done
