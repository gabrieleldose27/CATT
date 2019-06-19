#!/bin/bash

outcsv(){
    echo "\"${1}\", ${2}" >> "datasets.csv"
}

for img in dsets/*; do
    prefix=$(cut -d'_' -f1 <<< $(basename "$img"))
    case "$prefix" in
        "hotter")
            # 42 - 40.6
            randomizer=$(seq 38.2 .1 38.9 | shuf | head -n1)
            outcsv $img $randomizer
            ;;
        "hot")
            # 40.6 - 39.2
            randomizer=$(seq 37.5 .1 38.2 | shuf | head -n1)
            outcsv $img $randomizer
            ;;
        "normal")
            # 39.2 - 37.8 36.5 37.5
            randomizer=$(seq 36.8 .1 37.5 | shuf | head -n1)
            outcsv $img $randomizer
            ;;
        "cold")
            # 37.8 - 36.4
            randomizer=$(seq 36.1 .1 36.8 | shuf | head -n1)
            outcsv $img $randomizer
            ;;
        "colder")
            # 36.4 - 35
            randomizer=$(seq 35.4 .1 36.1 | shuf | head -n1)
            outcsv $img $randomizer
            ;;
    esac
done
