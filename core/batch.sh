#!/bin/bash

# Copyleft 2019 ThermoMed
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# ( CopyLeft License ) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
outcsv(){
    echo "${1}"
    echo "\"${1}\", ${2}" >> "dsets.csv"
}

for img in dsets/*; do
    prefix=$(cut -d'_' -f1 <<< $(basename "$img"))
    case "$prefix" in
        "hotter")
            randomizer=$(seq 38.25 .1 39.3 | shuf | head -n1)
            outcsv $img $randomizer
            ;;
        "hot")
            randomizer=$(seq 37.7 .1 38.5 | shuf | head -n1)
            outcsv $img $randomizer
            ;;
        "normal")
            randomizer=$(seq 36.8 .1 37.6 | shuf | head -n1)
            outcsv $img $randomizer
            ;;
        "cold")
            randomizer=$(seq 35.9 .1 36.7 | shuf | head -n1)
            outcsv $img $randomizer
            ;;
        "colder")
            randomizer=$(seq 35.0 .1 35.8 | shuf | head -n1)
            outcsv $img $randomizer
            ;;
    esac
done
