case=$(pwd | awk -F'/' '{print $NF}')
main=$case.C

Eqns=$(ls|grep "Eqn")

sed -i "/Iwrite(\|Iwait(/d" $main
sed -i "/if(write_\|if(wait_/,+8d" $main
sed -i "/if(runTime.outputTime())/,+3d" $main

for eq in ${Eqns};do
  sed -i "/Iwrite(\|Iwait(/d" $eq
  sed -i "/if(write_\|if(wait_/,+8d" $eq
  sed -i "/if(runTime.outputTime())/,+3d" $eq
done

sed -i '/#include "apio.H"/d' $main
sed -i '/#include "apio_init.H"/d' $main

sed -i '/#include "apio_terminate.H"/d' $main

sed -i "s/\/\/runTime.write()/runTime.write()/g" $main


sed -i "/^int write_\|^int wait_/d" apio_init.H

sed -i "s/^EXE.*/EXE = \$(FOAM_USER_APPBIN)\/${case}/g" Make/files

