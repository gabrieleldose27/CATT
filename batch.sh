#!/bin/bash

outcsv(){
    echo "${pwd}/${1}, ${2}" >> "datasets.csv"
}

CLASSES=("hotter" "hot" "normal" "cold" "colder")
for class in datasets/*; do
    cls=${class##*/}
    for img in $class/*; do
        case "$cls" in
            "hotter")
                # 42 - 40.6
                randomizer=$(seq 40.6 .01 42 | shuf | head -n1)
                mv ${img} "${img%.*}-${randomizer}-${img##*.}"
                outcsv "${img%.*}-${randomizer}-${img##*.}" $randomizer
                ;;
            "hot")
                # 40.6 - 39.2
                randomizer=$(seq 30.2 .01 40.6 | shuf | head -n1)
                mv ${img} "${img%.*}-${randomizer}-${img##*.}"
                outcsv "${img%.*}-${randomizer}-${img##*.}" $randomizer
                ;;
            "normal")
                # 39.2 - 37.8
                randomizer=$(seq 37.8 .01 39.2 | shuf | head -n1)
                mv ${img} "${img%.*}-${randomizer}-${img##*.}"
                outcsv "${img%.*}-${randomizer}-${img##*.}" $randomizer
                ;;
            "cold")
                # 37.8 - 36.4
                randomizer=$(seq 36.4 .01 37.8 | shuf | head -n1)
                mv ${img} "${img%.*}-${randomizer}-${img##*.}"
                outcsv "${img%.*}-${randomizer}-${img##*.}" $randomizer
                ;;
            "colder")
                # 36.4 - 35
                randomizer=$(seq 35 .01 36.4 | shuf | head -n1)
                mv ${img} "${img%.*}-${randomizer}-${img##*.}"
                outcsv "${img%.*}-${randomizer}-${img##*.}" $randomizer
                ;;
        esac
    done
done
