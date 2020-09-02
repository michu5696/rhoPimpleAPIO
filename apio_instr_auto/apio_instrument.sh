#!/bin/bash

workdir=$(pwd)


case=$(pwd | awk -F'/' '{print $NF}')
main=$case.C
Eqns=$(ls|grep "Eqn")

exe=${case}

sed -i "1 s/^.*$/${main}/" Make/files
sed -i "s/^EXE.*/EXE = \$(FOAM_USER_APPBIN)\/${case}/g" Make/files
sed -i '/^$/d' $main
for eq in ${Eqns};do
  sed -i '/^$/d' $eq
done


echo "Introducing event calls to check for field updates ..."

fb="init"
for f in $( cat fields);do
  if [ $fb = "init" ];then
    s=$(grep -n "while (runTime" $main | awk -F':' '{print $1}')
    sed -n "1,${s}p" $main > tmp1
    sed "1,${s}d" $main | awk -v s="$s" -v f="$f" -v main="$main" '{print $0} /#include|.*;/{print "\n","if (mesh.getObjectPtr<regIOobject>(word(\""f"\"),false))\n { Info << \""NR+s"-event-"f"-"main": \"<< mesh.getObjectPtr<regIOobject>(word(\""f"\"),false)->eventNo() << endl;}"}' > tmp2
    cat tmp2 >> tmp1 
    mv tmp1 $main
    rm tmp2
    for eq in $Eqns;do
      awk -v s="$s" -v f="$f" -v eq="$eq" '{print $0} /#include|.*;/{print "\n","if (mesh.getObjectPtr<regIOobject>(word(\""f"\"),false))\n { Info << \""NR"-event-"f"-"eq": \"<< mesh.getObjectPtr<regIOobject>(word(\""f"\"),false)->eventNo() << endl;}"}' $eq > awk_tmp && mv awk_tmp $eq
    done
    fb=$f 
  else
    awk -F'-|"' -v f="${f}" -v main="$main" -v fb="${fb}" -v fb_="-${fb}-" '{print $0} $0 ~ /event-/ && $0 ~ fb_ && $0 ~ main  {print "\n","if (mesh.getObjectPtr<regIOobject>(word(\""f"\"),false)) \n{Info << \""$2"-event-"f"-"main": \"<< mesh.getObjectPtr<regIOobject>(word(\""f"\"),false)->eventNo() << endl;}"}' $main > awk_tmp && mv awk_tmp $main
    for eq in $Eqns;do  
      awk -F'-|"' -v f="${f}" -v eq="$eq" -v fb="${fb}" -v fb_="-${fb}-" '{print $0} $0 ~ /event-/ && $0 ~ fb_ && $0 ~ eq  {print  "\n","if (mesh.getObjectPtr<regIOobject>(word(\""f"\"),false)) \n{Info << \""$2"-event-"f"-"eq": \"<< mesh.getObjectPtr<regIOobject>(word(\""f"\"),false)->eventNo() << endl;}"}' $eq > awk_tmp && mv awk_tmp $eq
    done
  fi
  fb=$f
done


echo "Compiling ..."
 wmake &> log.compilation 

cd $1

sed -i "s/^stopAt.*/stopAt writeNow;/g" system/controlDict

blockMesh &> $workdir/log.blockMesh
echo "Running ..."
${exe} > $workdir/log.run


echo "Introducing APIO function calls ..."

for f in $(cat $workdir/fields);do
  sed -n "/^.*-event-${f}-/p" $workdir/log.run  > $workdir/tmp_$f
done

cd $workdir 

for file in tmp_*;do
     awk -F'-' 'last != $1; {last = $1}' $file > awk_tmp && mv awk_tmp $file
done

sed -i "/event-\|if (mesh.getObjectPtr/d" $main
sed -i '/^$/d' $main

for eq in ${Eqns};do
  sed -i "/event-\|if (mesh.getObjectPtr/d" $eq
  sed -i '/^$/d' $eq
done


f_0=($(awk -F '_' '{if ($2 == 0) print $1}' fields))

for f in $(cat fields);do

if [[ $f != *_0 ]];then

     awk -F '-|:' 'NR==1{prev=$5}{if ($5 != prev) print $1,$4,$3; prev=$5}' tmp_$f > post_tmp_$f
    (head -n 1 post_tmp_$f; grep -xc "$(head -n 1 post_tmp_$f)" post_tmp_$f;echo "WAIT" ) | fmt >> post_wait
    (tail -n 1 post_tmp_$f; grep -xc "$(tail -n 1 post_tmp_$f)" post_tmp_$f; echo "WRITE" ) | fmt >> post_write

fi
done

sed -i '$a END' post_wait

sed -i '$a END' post_write

sort -o post_write post_write
sort -o post_wait post_wait  

(awk 'BEGIN{OFS=":"}NR==1{len=0;line=$1;file=$2;reps=$4;fields[len++]=$3;action=$5}NR!=1{if ($1!=line || file!=$2) {print "="line,file,reps,action":";if (len>1) {for (i in fields) print fields[i]","} else {print fields[0]}len=0}line=$1;file=$2;reps=$4;fields[len++]=$3;action=$5}' post_wait | tr -d "\n"|tr "=" "\n"; printf "\n")|sed 's/\(.*\),/\1 /'| sed '/^$/d' > awk_tmp && mv awk_tmp post_wait_2

(awk 'BEGIN{OFS=":"}NR==1{len=0;line=$1;file=$2;reps=$4;fields[len++]=$3;action=$5}NR!=1{if ($1!=line || file!=$2) {print "="line,file,reps,action":";if (len>1) {for (i in fields) print fields[i]","} else {print fields[0]}len=0}line=$1;file=$2;reps=$4;fields[len++]=$3;action=$5}' post_write | tr -d "\n"|tr "=" "\n"; printf "\n")|sed 's/\(.*\),/\1 /'| sed '/^$/d' > awk_tmp && mv awk_tmp post_write_2

cp post_wait_2 post_DEF_1
cat post_write_2 >> post_DEF_1

cat post_DEF_1 | sort -t ':' -k2,2 -k1,1 > post_DEF

for f in $(cat fields);do
if [[ " ${f_0[@]} " =~ " ${f} " ]];then
    sed -i "s/:$f,/:${f},${f}_0,/g" post_DEF
    sed -i "s/,$f,/,${f},${f}_0,/g" post_DEF
    sed -i "s/,$f$/,${f},${f}_0/g" post_DEF
    sed -i "s/:$f$/:${f},${f}_0/g" post_DEF

fi
done

LW=$(wc -l post_DEF | cut -d' ' -f 1)

file0=$(head -n 1 post_DEF | cut -d':' -f 2)
xtra=0
for i in $(seq 1 $LW);do   
   thisline=$(head -n $i post_DEF | tail -n 1)
   line=$(echo $thisline | cut -d':' -f 1)
   file=$(echo $thisline | cut -d':' -f 2)
   reps=$(echo $thisline | cut -d':' -f 3)
   action=$(echo $thisline | cut -d':' -f 4)
   fields=$(echo $thisline | cut -d':' -f 5)

   if [[ $file != $file0 ]];then
       xtra=0
   fi 

   if [[ $reps > 1 ]] && [[ $action == "WAIT" ]]; then
      sed -i "$(($line +$xtra))i	if(wait_${line}_loop == $(($reps-1))) \n { \n	Iwait({$(echo "&f_${fields}" | sed 's/,/,\&f_/g') }); \n 	wait_${line}_loop=0; \n }\nelse\n {\n	wait_${line}_loop++;\n }" $file
      xtra=$(($xtra + 9))
      echo "int wait_${line}_loop = 0;" >> $workdir/apio_init.H
  elif [[ $reps == 1 ]] && [[ $action == "WAIT" ]];then
      sed -i "$(($line +$xtra))i  Iwait({$(echo "&f_${fields}" | sed 's/,/,\&f_/g') });" $file
      xtra=$(($xtra +1))
  elif [[ $reps > 1 ]] && [[ $action == "WRITE" ]]; then
      sed -i "$(($line +$xtra))a        if(write_${line}_loop == $(($reps-1)) && runTime.outputTime()) \n { \n   Iwrite({$(echo "&f_${fields}" | sed 's/,/,\&f_/g')}, cv_worker, queue); \n        write_${line}_loop=0; \n }\nelse if(runTime.outputTime())\n {\n   write_${line}_loop++;\n }" $file
      xtra=$(($xtra + 9))
      echo "int write_${line}_loop = 0;" >> $workdir/apio_init.H
  elif [[ $reps == 1 ]]  && [[ $action == "WRITE" ]];then
      sed -i "$(($line +$xtra))a	if(runTime.outputTime()) \n { \n	Iwrite({$(echo "&f_${fields}" | sed 's/,/,\&f_/g')}, cv_worker, queue); \n }" $file
      xtra=$(($xtra +4))
  fi

  file0=$file
done

sed -i '/int main(/i #include "apio.H"' $main
sed -i '/while (runTime/i #include "apio_init.H"' $main

sed -i '/return 0;/i #include "apio_terminate.H"' $main

sed -i "s/runTime.write()/\/\/runTime.write()/g" $main

echo "DONE!"

rm log.*

rm tmp_*
rm post_*



