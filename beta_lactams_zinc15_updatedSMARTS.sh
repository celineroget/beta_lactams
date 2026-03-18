#!/bin/bash
#SBATCH --job-name=beta_lactams_zin15_newSMARTS
#SBATCH --array=1-10
#SBATCH --output=/network/scratch/r/rogetc/logs/%x_%j_%A_%a.out
#SBATCH --error=/network/scratch/r/rogetc/logs/%x_%j_%A_%a.err
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G


# ---------------------------
# Load modules / activate env
# ---------------------------
module load OpenSSL libffi
source $HOME/scratch/envs/chemprop_db/bin/activate
echo "Virtual environment activated."
which python

# ---------------------------
# Print RDKit version
# ---------------------------
python -c "import rdkit; print('RDKit version:', rdkit.__version__)"
cd /network/scratch/r/rogetc/beta_lactam
# Directory to store group files
BASE_DIR=/network/scratch/r/rogetc/beta_lactam/data/ZINC/ZINC
GROUP_DIR=/network/scratch/r/rogetc/beta_lactam/data/ZINC/zinc_groups
GROUP_FILE=$(ls $GROUP_DIR/group_* | sed -n "${SLURM_ARRAY_TASK_ID}p")
OUTPUT_FILE=/network/scratch/r/rogetc/beta_lactam/data/ZINC/zinc_out_newSMARTS/zinc_out_${SLURM_ARRAY_TASK_ID}.csv

python /network/scratch/r/rogetc/beta_lactam/beta_lactams_screening.py \
--zinc_file_list $GROUP_FILE \
--zinc_output $OUTPUT_FILE \
--zinc_base_dir $BASE_DIR \
--n_cpus 8

#sbatch /network/scratch/r/rogetc/beta_lactam/beta_lactams_zinc15_updatedSMARTS.sh
