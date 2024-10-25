#!/bin/bash  -l
#SBATCH -N 1 --partition=gpu --ntasks-per-node=6 
#SBATCH --gres=gpu:1
#SBATCH --time=6:00:00		# Walltime
#SBATCH --job-name=phip-0.6-L-75.0
cd $SLURM_SUBMIT_DIR

######################################
inputfile=run.in
outputfile=run.out
######################################
/bin/hostname

# Fetch the device ID for the GPU that has been assigned to the job
GPUDEV=`cat $SLURM_GPUFILE | awk '{print $1}'`
if [ -z $GPUDEV ]; then
  echo "ERROR finding $SLURM_GPUFILE; using default GPU deviceid=0"
  GPUDEV=0
fi

# Prepare the run by substituting the CUDA select device line
# Check whether the line exists first
grep "CUDA_[Ss]elect[Dd]evice" ${inputfile} > /dev/null
if [ $? -ne 0 ]; then
  echo "CUDA_SelectDevice line not found in $inputfile"
  exit 1
fi
sed -i "s/\(CUDA_[Ss]elect[Dd]evice\).*/\1 = ${GPUDEV}/g" ${inputfile}

/home/tquah/PolyFTS_ALL_github/PolyFTS/bin/Release/PolyFTSGPU.x ${inputfile} > ${outputfile}


exit 0
