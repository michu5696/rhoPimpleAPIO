#!/bin/bash
noline_orig=($(cat orig.out | grep -n "Start" | awk -F":" '{print $1}' ))
noline_orig+=($(cat orig.out | wc -l))

iterno_orig=()
for i in $(seq 0 $((${#noline_orig[@]}-2)));do iterno_orig+=($(sed -n "${noline_orig[$i]},${noline_orig[$i+1]}p" orig.out | grep -c "ExecutionTime")) ;done

echo ${iterno_orig[@]} | tr " " "\n" > iterno_orig.dat

noline_apio=($(cat apio.out | grep -n "Start" | awk -F":" '{print $1}' ))
noline_apio+=($(cat apio.out | wc -l))

iterno_apio=()
for i in $(seq 0 $((${#noline_apio[@]}-2)));do iterno_apio+=($(sed -n "${noline_apio[$i]},${noline_apio[$i+1]}p" apio.out | grep -c "ExecutionTime")) ;done

echo ${iterno_apio[@]} | tr " " "\n" > iterno_apio.dat

