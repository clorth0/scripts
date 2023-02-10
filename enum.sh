#!/bin/bash

echo "Enter Target(s):"
read target

echo "Enter timing (1-5, with 5 being the fastest and most aggressive):"
read timing

echo "Enter scan type (T for TCP, U for UDP, or S for a stealth scan):"
read scan_type

echo "Enter output type (N for normal, X for XML, G for grepable, J for JSON, A for all formats, or none):"
read output_type

echo "Enter verbosity (0 for normal, 1 for verbose, 2 for very verbose, and so on...):"
read verbosity

scan_type=$(echo $scan_type | tr '[:lower:]' '[:upper:]')
output_type=$(echo $output_type | tr '[:lower:]' '[:upper:]')

if [ "$scan_type" == "T" ]; then
  scan_option="-sT"
elif [ "$scan_type" == "U" ]; then
  scan_option="-sU"
elif [ "$scan_type" == "S" ]; then
  scan_option="-sS"
else
  echo "Invalid scan type. Please enter T, U, or S."
  exit 1
fi

scan_option="$scan_option -T$timing -sV"

if [ "$output_type" == "A" ]; then
  nmap $scan_option -v$verbosity -oN normal_output -oX xml_output -oG grepable_output -oJ json_output $target
elif [ "$output_type" == "N" ]; then
  nmap $scan_option -v$verbosity -oN $target
elif [ "$output_type" == "X" ]; then
  nmap $scan_option -v$verbosity -oX $target
elif [ "$output_type" == "G" ]; then
  nmap $scan_option -v$verbosity -oG $target
elif [ "$output_type" == "J" ]; then
  nmap $scan_option -v$verbosity -oJ $target
elif [ "$output_type" == "NONE" ]; then
  nmap $scan_option -v$verbosity $target
else
  echo "Invalid output type. Please enter N, X, G, J, A, or none."
  exit 1
fi
