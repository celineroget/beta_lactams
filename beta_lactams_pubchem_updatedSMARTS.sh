#!/bin/bash
#SBATCH --job-name=beta_lactams_pubchem_newSMARTS
#SBATCH --output=/network/scratch/r/rogetc/logs/%x_%j.out
#SBATCH --error=/network/scratch/r/rogetc/logs/%x_%j.err
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


python /network/scratch/r/rogetc/beta_lactam/beta_lactams_screening.py \
    --pubchem_input /network/scratch/r/rogetc/beta_lactam/data/pubchem/pubchem-canonical/CID-SMILES-CANONICAL.smi \
    --pubchem_output /network/scratch/r/rogetc/beta_lactam/data/pubchem/beta_lactams_pubchem_newSMARTS.csv \
    --n_cpus 8

#sbatch /network/scratch/r/rogetc/beta_lactam/beta_lactams_pubchem_updatedSMARTS.sh